import time
import random
from pathlib import Path
from typing import Dict, List, Optional
from playwright.sync_api import sync_playwright, Page
from form_detector import FormDetector, FormField
from dynamic_data_generator import DynamicDataGenerator, FormAnalyzer, FormProfile
from human_behavior import HumanBehavior
from error_handler import ErrorHandler, ValidationError, CaptchaDetectedError, FormStructureChangedError
from screenshot_manager import ScreenshotManager
from logger import SubmissionLogger
from config import Config
from utils import load_cookies, get_proxy_config, RateLimiter

class FormFiller:
    def __init__(self, config: Config, logger: SubmissionLogger, screenshot_mgr: ScreenshotManager):
        self.config = config
        self.logger = logger
        self.screenshot_mgr = screenshot_mgr
        self.error_handler = ErrorHandler(config, logger)
        self.rate_limiter = RateLimiter(config.rate_limit_per_minute, config.rate_limit_per_hour)
        self.human = HumanBehavior(config)
        self.data_gen = DynamicDataGenerator()
        self.form_analyzer = FormAnalyzer()
        self._browser = None
        self._context = None
        self._page = None
        self._current_profile: Optional[FormProfile] = None

    def _create_browser(self):
        self._playwright = sync_playwright().start()
        launch_args = {"headless": self.config.headless}
        proxy = get_proxy_config(self.config.proxy)
        if proxy:
            launch_args["proxy"] = proxy

        self._browser = self._playwright.chromium.launch(**launch_args)
        context_args = {
            "user_agent": self.config.get_random_user_agent(),
            "viewport": {"width": 1280, "height": 720}
        }
        cookies = load_cookies(self.config.cookie_path)
        self._context = self._browser.new_context(**context_args)
        if cookies:
            self._context.add_cookies(cookies)

        self._page = self._context.new_page()

    def _close_browser(self):
        if self._browser:
            self._browser.close()
            self._playwright.stop()
            self._browser = None
            self._context = None
            self._page = None

    def fill_submission(self, form_url: str, submission_id: int) -> Dict:
        start_time = time.time()
        submitted_data: Dict = {}

        try:
            self.rate_limiter.wait_if_needed()
            if not self._page:
                self._create_browser()

            assert self._page is not None
            page = self._page
            page.goto(form_url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(random.randint(1000, 3000))

            # Dismiss "Sign in to continue" modal if present
            self._dismiss_signin_modal(page)

            if self.error_handler.detect_captcha(page):
                raise CaptchaDetectedError("CAPTCHA detected on form")

            # Analyze form to determine context
            form_title = self._extract_form_title(page)
            detector = FormDetector(page)

            max_pages = 20  # Safety limit for multi-page forms
            current_page = 1
            form_analyzed = False
            persona = None

            while current_page <= max_pages:
                # Detect fields on current page
                fields = detector.detect_fields()
                if not fields:
                    raise FormStructureChangedError(f"No form fields detected on page {current_page}")

                # Analyze form context once using first page fields
                if not form_analyzed:
                    field_labels = [f.label for f in fields if f.label != "Unknown Field"]
                    self._current_profile = self.form_analyzer.analyze_form(form_title, field_labels)
                    print(f"[INFO] Form Context: {self._current_profile.context.value}")
                    print(f"[INFO] Topic: {self._current_profile.topic}")
                    print(f"[INFO] Industry: {self._current_profile.industry}")
                    print(f"[INFO] Keywords: {', '.join(self._current_profile.detected_keywords[:5])}")
                    # Generate a consistent persona for this submission
                    persona = self.data_gen.generate_persona(self._current_profile, submission_id)
                    form_analyzed = True

                # Fill all fields on current page
                for field in fields:
                    value = self.data_gen.generate_contextual_value(
                        field.label,
                        field.field_type,
                        self._current_profile,
                        submission_id,
                        persona=persona
                    )
                    field.value = value
                    submitted_data[f"Page {current_page} - {field.label}"] = value

                    if field.field_type in ["text", "email"]:
                        self.human.human_type(field.element, str(value), page)
                    elif field.field_type == "date":
                        field.element.fill(str(value))
                    elif field.field_type == "radio":
                        self._select_radio(field, value, page)
                    elif field.field_type == "checkbox":
                        self._select_checkbox(field, value, page)
                    elif field.field_type == "dropdown":
                        self._select_dropdown(field, value, page)
                    elif field.field_type == "linear_scale":
                        self._select_linear_scale(field, value, page)
                    elif field.field_type == "file_upload":
                        self._handle_file_upload(field, page)

                    self.human.pause_between_fields()

                # Check for Submit button first (form might end on this page)
                submit_btn = detector.get_submit_button()
                if submit_btn:
                    self.human.human_click(submit_btn, page)
                    page.wait_for_timeout(random.randint(2000, 4000))

                    if not self.error_handler.wait_for_submission_confirmation(page):
                        errors = self.error_handler.detect_validation_errors(page)
                        if errors:
                            raise ValidationError(f"Validation errors: {errors}")
                    break  # Form submitted successfully

                # Check for Next button to go to next page
                if detector.has_next_section():
                    next_btn = page.locator("button:has-text('Next'), div[role='button']:has-text('Next')").first
                    if next_btn.count() > 0 and next_btn.is_visible():
                        self.human.human_click(next_btn, page)
                        page.wait_for_timeout(random.randint(1500, 3000))
                        current_page += 1
                        # Clear fields for next page detection
                        detector.fields = []
                        continue
                    else:
                        raise FormStructureChangedError("Next button not clickable")
                else:
                    # No Submit or Next button found - might be end of form
                    break

            if current_page > max_pages:
                raise FormStructureChangedError(f"Form has more than {max_pages} pages, stopped for safety")

            _ = self.screenshot_mgr.save_screenshot(page, submission_id)
            duration = time.time() - start_time
            self.logger.log_submission(submission_id, form_url, "success", submitted_data, duration)
            return submitted_data

        except CaptchaDetectedError:
            raise
        except Exception as e:
            import traceback
            duration = time.time() - start_time
            error_detail = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
            self.logger.log_submission(submission_id, form_url, "failed", submitted_data, duration, error_detail)
            raise

    def _is_other_option(self, element) -> bool:
        """Check if an element is an 'Other' option with or without input field."""
        try:
            label = element.inner_text().strip()
            label_lower = label.lower().rstrip(':').rstrip()

            # Check for "Other" text - be very aggressive
            if label_lower == "other":
                return True
            if label_lower.startswith("other"):
                return True
            if "other:" in label_lower:
                return True
            if "other (" in label_lower:
                return True

            # Check if there's an input field inside (definite "Other" with text)
            try:
                if element.locator("input").count() > 0:
                    # Even if text doesn't say "Other", if it has an input, it's likely "Other"
                    return True
            except Exception:
                pass
        except Exception:
            pass
        return False

    def _select_radio(self, field: FormField, value: str, page: Page):
        """Select a random radio button option, skipping 'Other' and similar."""
        options = field.element.locator("div[role='radio']").all()
        if not options:
            return

        # Filter out "Other" option with robust detection
        valid_options = []
        for opt in options:
            if self._is_other_option(opt):
                continue  # Skip "Other" options
            valid_options.append(opt)

        # If all options were filtered out, use all options as fallback
        if not valid_options:
            valid_options = options

        # Randomly select from valid options
        selected = random.choice(valid_options)
        self.human.human_click(selected, page)

    def _select_checkbox(self, field: FormField, value: str, page: Page):
        """Select ALL checkboxes except 'Other' (if configured to skip)."""
        # Try multiple ways to find checkboxes
        checkboxes = field.element.locator("div[role='checkbox']").all()
        if not checkboxes:
            checkboxes = field.element.locator("input[type='checkbox']").all()
        if not checkboxes:
            return

        for cb in checkboxes:
            # Skip "Other" options if configured
            if self.config.skip_other_options and self._is_other_option(cb):
                continue

            # Select all other checkboxes
            self.human.human_click(cb, page)
            page.wait_for_timeout(random.randint(200, 500))  # Small delay between selections

    def _select_dropdown(self, field: FormField, value: str, page: Page):
        """Select a random option from dropdown, skipping 'Other'."""
        field.element.click()
        page.wait_for_timeout(500)

        # Try to find options
        options = page.locator("div[role='option']").all()
        if not options:
            options = field.element.locator("option").all()
        if not options:
            return

        # Filter out "Other" options
        valid_options = []
        for opt in options:
            if self.config.skip_other_options and self._is_other_option(opt):
                continue  # Skip "Other" options
            valid_options.append(opt)

        if not valid_options:
            valid_options = options

        selected = random.choice(valid_options)
        self.human.human_click(selected, page)

    def _select_linear_scale(self, field: FormField, value: int, page: Page):
        try:
            field.element.fill(str(value))
        except Exception:
            field.element.click()

    def _handle_file_upload(self, field: FormField, page: Page):
        if not self.config.generate_file_uploads:
            return
        dummy_path = self._create_dummy_file()
        try:
            field.element.set_input_files(dummy_path)
            page.wait_for_timeout(1000)
        finally:
            try:
                Path(dummy_path).unlink()
            except Exception:
                pass

    def _extract_form_title(self, page: Page) -> str:
        """Extract the form title from the Google Form."""
        title_selectors = [
            "div[role='heading'][aria-level='1']",
            ".freebirdFormviewerViewHeaderTitle",
            "div[data-original-font-family]",
            "span[jsname='Yxmc6e']",
            "div.freebirdFormviewerViewHeaderTitleRow",
            "h1"
        ]

        for selector in title_selectors:
            try:
                element = page.locator(selector).first
                if element.count() > 0:
                    title = element.inner_text().strip()
                    if title and len(title) > 0:
                        return title
            except Exception:
                continue

        # Try to get title from page title
        try:
            page_title = page.title()
            if page_title and "Google Forms" not in page_title:
                return page_title
        except Exception:
            pass

        return "Untitled Form"

    def _dismiss_signin_modal(self, page: Page) -> None:
        """Dismiss the 'Sign in to continue' modal by clicking Cancel and removing blur."""
        try:
            # Wait up to 5s for modal heading to appear
            try:
                page.wait_for_selector("text='Sign in to continue'", timeout=5000, state="visible")
            except Exception:
                return  # No modal present

            # Click Cancel button using Playwright (more reliable than JS)
            cancel_selectors = [
                "div[role='button']:has-text('Cancel')",
                "div[role='button']:has-text('No thanks')",
                "button:has-text('Cancel')",
                "span:has-text('Cancel')"
            ]

            for selector in cancel_selectors:
                btn = page.locator(selector).first
                if btn.count() > 0:
                    try:
                        btn.click(force=True, timeout=2000)
                        page.wait_for_timeout(1000)
                        break
                    except Exception:
                        continue

            # Use JavaScript to remove blur/filter from page
            page.evaluate("""
                // Remove modal/backdrop elements
                var toRemove = [
                    "div[jsname='r4nke']", "div.pw1uU", "[role='dialog']",
                    ".R6Lfte.tOrNgd.qRUolc", ".OllbWe", ".XfpsVe.J9fJmf"
                ];
                toRemove.forEach(function(sel) {
                    var els = document.querySelectorAll(sel);
                    for (var i = 0; i < els.length; i++) {
                        var el = els[i];
                        if (el && el.parentNode) el.parentNode.removeChild(el);
                    }
                });

                // Remove blur/filter from all elements
                var all = document.querySelectorAll("*");
                for (var j = 0; j < all.length; j++) {
                    var el = all[j];
                    var cs = window.getComputedStyle(el);
                    if (cs.filter && cs.filter !== 'none') {
                        el.style.setProperty('filter', 'none', 'important');
                        el.style.setProperty('-webkit-filter', 'none', 'important');
                    }
                    if (cs.pointerEvents === 'none') {
                        el.style.setProperty('pointer-events', 'auto', 'important');
                    }
                    if (el.getAttribute('aria-hidden') === 'true') {
                        el.removeAttribute('aria-hidden');
                    }
                }

                // Force body/html to be interactive
                document.body.style.filter = 'none';
                document.body.style.pointerEvents = 'auto';
                document.documentElement.style.filter = 'none';
            """)

            page.wait_for_timeout(2000)

            # Verify modal is gone
            try:
                page.wait_for_selector("text='Sign in to continue'", state="detached", timeout=3000)
            except Exception:
                pass  # Modal might already be gone

            page.wait_for_timeout(1000)  # Let form re-render
        except Exception as e:
            print(f"Error in _dismiss_signin_modal: {e}")
            pass
        except Exception:
            pass
        except Exception:
            pass

    def _create_dummy_file(self) -> str:
        path = "dummy_upload.txt"
        with open(path, "w") as f:
            f.write("This is a dummy file for form upload testing.\n")
        return path

    def run_multiple(self, form_url: str, count: int, status_callback=None) -> List[Dict]:
        results = []
        for i in range(1, count + 1):
            if status_callback:
                status_callback(f"Submitting {i}/{count}...")
            try:
                result = self.fill_submission(form_url, i)
                results.append(result)
            except CaptchaDetectedError:
                if status_callback:
                    status_callback("CAPTCHA detected! Stopping.")
                break
            except Exception as e:
                if status_callback:
                    status_callback(f"Submission {i} failed: {str(e)[:50]}...")
            self.human.pause_between_submissions()
        self._close_browser()
        return results
