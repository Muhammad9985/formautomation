from typing import List, Optional
from playwright.sync_api import Page, Locator

class FormField:
    def __init__(
        self,
        label: str,
        field_type: str,
        required: bool,
        element: Locator,
        options: Optional[List[str]] = None,
        section: int = 0
    ):
        self.label = label
        self.field_type = field_type
        self.required = required
        self.element = element
        self.options = options or []
        self.section = section
        self.value: Optional[str] = None

    def __repr__(self):
        return f"FormField(label='{self.label}', type='{self.field_type}', required={self.required})"

class FormDetector:
    def __init__(self, page: Page):
        self.page = page
        self.fields: List[FormField] = []
        self.sections: List[Locator] = []
        self.current_section = 0

    def detect_fields(self) -> List[FormField]:
        self.fields = []
        self._detect_all_fields()
        return self.fields

    def _detect_all_fields(self):
        # Wait for form to load
        self.page.wait_for_selector("form, div[role='form']", timeout=10000)

        # Find all question containers
        question_containers = self.page.locator("div[data-params]").all()
        if not question_containers:
            question_containers = self.page.locator("div.freebirdFormeditorViewItemcard").all()
        if not question_containers:
            question_containers = self.page.locator("div[jscontroller]").all()

        for container in question_containers:
            try:
                field = self._detect_field_in_container(container)
                if field:
                    self.fields.append(field)
            except Exception:
                continue

    def _get_label(self, container: Locator) -> str:
        # Try multiple approaches to get the field label

        # Method 1: Look for specific Google Forms title elements
        title_selectors = [
            ".M7ezyf",  # Primary title class in Google Forms
            ".vnumcf",  # Secondary title class
            "div[jsname='M7ezyf']",
            "span[jsname='M7ezyf']",
            "div[data-automation-id='text']",
            "span[role='heading']",
            ".freebirdFormviewerViewItemsTitle",
            "[class*='title']"
        ]

        for selector in title_selectors:
            try:
                el = container.locator(selector).first
                if el.count() > 0:
                    text = el.inner_text().strip()
                    if text and len(text) > 1:
                        # Remove trailing * for required fields
                        text = text.rstrip('*').strip()
                        return text
            except Exception:
                continue

        # Method 2: Get all text from container and extract question
        try:
            # Get all text elements in the container
            text_elements = container.locator("[class*='vnumcf'], [class*='M7ezyf'], span, div").all()
            for el in text_elements:
                try:
                    text = el.inner_text().strip()
                    # Skip very short text, options, and metadata
                    if text and len(text) > 5 and len(text) < 200:
                        # Check if it looks like a question
                        if '?' in text or any(keyword in text.lower() for keyword in
                            ['name', 'email', 'phone', 'address', 'age', 'gender', 'city', 'date']):
                            return text.rstrip('*').strip()
                except Exception:
                    continue
        except Exception:
            pass

        # Method 3: Get the full container text and parse
        try:
            full_text = container.inner_text().strip()
            lines = [line.strip() for line in full_text.split('\n') if line.strip()]

            # Look for lines that look like questions
            for line in lines[:5]:  # Check first 5 lines
                # Skip option text (usually short)
                if len(line) > 5 and len(line) < 300:
                    # Check if it contains question indicators
                    line_lower = line.lower()
                    question_keywords = [
                        'name', 'email', 'phone', 'age', 'gender', 'address', 'city',
                        'date', 'time', 'rate', 'satisfaction', 'feedback',
                        'comment', 'question', 'how', 'what', 'when', 'where',
                        'why', 'which', 'do you', 'are you', 'is your'
                    ]
                    if any(kw in line_lower for kw in question_keywords) or '?' in line:
                        return line.rstrip('*').strip()[:150]

            # Fallback: use first substantial line
            for line in lines:
                if len(line) > 10 and len(line) < 300:
                    return line.rstrip('*').strip()[:150]
        except Exception:
            pass

        return "Unknown Field"

    def _is_required(self, container: Locator) -> bool:
        try:
            required_marker = container.locator("span:has-text('*')").first
            return required_marker.is_visible()
        except Exception:
            return False

    def _detect_field_in_container(self, container: Locator) -> Optional[FormField]:
        label = self._get_label(container)
        required = self._is_required(container)
        section = self.current_section

        # Check for radio buttons FIRST (before text input, because "Other" has input field)
        radio_group = container.locator("div[role='radiogroup']").first
        if radio_group.count() > 0:
            options = [opt.inner_text().strip() for opt in radio_group.locator("div[role='radio']").all()]
            return FormField(label, "radio", required, radio_group, options, section=section)

        # Check for checkboxes SECOND
        checkbox_group = container.locator("div[role='group']").first
        if checkbox_group.count() == 0:
            checkbox_group = container.locator("div[jscontroller][jsaction*='click']").first
        if checkbox_group.count() > 0:
            checkboxes = checkbox_group.locator("div[role='checkbox']").all()
            if not checkboxes:
                checkboxes = container.locator("input[type='checkbox']").all()
            if checkboxes:
                options = [cb.inner_text().strip() for cb in checkboxes]
                return FormField(label, "checkbox", required, checkbox_group, options, section=section)

        # Text input (includes email fields) - check AFTER radio/checkbox
        text_input = container.locator("input[type='text'], input[type='email'], textarea, div[role='textbox']").first
        if text_input.count() > 0:
            # Skip if this is inside a radio/checkbox "Other" option
            parent_radio = container.locator("div[role='radio']").first
            parent_checkbox = container.locator("div[role='checkbox']").first
            if parent_radio.count() > 0 or parent_checkbox.count() > 0:
                # This is an "Other" option with input - skip it
                return None

            # Check if it's an email field by looking at label
            label_lower = label.lower()
            if any(word in label_lower for word in ["email", "e-mail", "mail"]):
                return FormField(label, "email", required, text_input, section=section)
            return FormField(label, "text", required, text_input, section=section)

        # Date input
        date_input = container.locator("input[type='date']").first
        if date_input.count() > 0:
            return FormField(label, "date", required, date_input, section=section)

        # Radio buttons (multiple choice)
        radio_group = container.locator("div[role='radiogroup']").first
        if radio_group.count() > 0:
            options = [opt.inner_text().strip() for opt in radio_group.locator("div[role='radio']").all()]
            return FormField(label, "radio", required, radio_group, options, section=section)

        # Checkboxes - try multiple selectors
        checkbox_group = container.locator("div[role='group']").first
        if checkbox_group.count() == 0:
            checkbox_group = container.locator("div[jscontroller][jsaction*='click']").first
        if checkbox_group.count() > 0:
            checkboxes = checkbox_group.locator("div[role='checkbox']").all()
            if not checkboxes:
                # Try alternative checkbox detection
                checkboxes = container.locator("input[type='checkbox']").all()
            if checkboxes:
                options = [cb.inner_text().strip() for cb in checkboxes]
                return FormField(label, "checkbox", required, checkbox_group, options, section=section)

        # Dropdown - try multiple selectors
        listbox = container.locator("div[role='listbox']").first
        if listbox.count() == 0:
            listbox = container.locator("select").first
        if listbox.count() == 0:
            # Look for clickable element that might open a dropdown
            listbox = container.locator("div[jsaction*='click']").first
        if listbox.count() > 0:
            return FormField(label, "dropdown", required, listbox, section=section)

        # Linear scale
        slider = container.locator("div[role='slider']").first
        if slider.count() > 0:
            return FormField(label, "linear_scale", required, slider, section=section)

        # File upload
        file_input = container.locator("input[type='file']").first
        if file_input.count() > 0:
            return FormField(label, "file_upload", required, file_input, section=section)

        return None

    def has_next_section(self) -> bool:
        next_button = self.page.locator("button:has-text('Next'), div[role='button']:has-text('Next')").first
        return next_button.count() > 0 and next_button.is_visible()

    def go_to_next_section(self) -> bool:
        next_button = self.page.locator("button:has-text('Next'), div[role='button']:has-text('Next')").first
        if next_button.count() > 0 and next_button.is_visible():
            next_button.click()
            self.page.wait_for_timeout(1000)
            self.current_section += 1
            self._detect_all_fields()
            return True
        return False

    def get_submit_button(self) -> Optional[Locator]:
        submit_selectors = [
            "button:has-text('Submit')",
            "div[role='button']:has-text('Submit')",
            "button[type='submit']"
        ]
        for selector in submit_selectors:
            btn = self.page.locator(selector).first
            if btn.count() > 0 and btn.is_visible():
                return btn
        return None

    def detect_captcha(self) -> bool:
        captcha_selectors = [
            "iframe[src*='recaptcha']",
            "iframe[src*='captcha']",
            "div.g-recaptcha",
            "div[class*='captcha']"
        ]
        for selector in captcha_selectors:
            if self.page.locator(selector).count() > 0:
                return True
        return False
