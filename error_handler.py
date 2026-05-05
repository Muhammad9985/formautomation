import time
from typing import Callable, Optional
from playwright.sync_api import TimeoutError as PlaywrightTimeout

class FormError(Exception):
    pass

class ValidationError(FormError):
    pass

class CaptchaDetectedError(FormError):
    pass

class FormStructureChangedError(FormError):
    pass

class ErrorHandler:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.max_retries = config.max_retries_per_submission
        self.retry_delay = config.retry_delay

    def retry_on_error(self, func: Callable, *args, **kwargs):
        last_error: Optional[Exception] = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except CaptchaDetectedError as e:
                self.logger.log_submission(
                    kwargs.get("submission_id", 0),
                    kwargs.get("form_url", ""),
                    "captcha_detected",
                    {},
                    0,
                    str(e)
                )
                raise
            except (ValidationError, FormStructureChangedError) as e:
                last_error = e
                time.sleep(self.retry_delay * (attempt + 1))
            except PlaywrightTimeout as e:
                last_error = e
                time.sleep(self.retry_delay * (attempt + 1))
            except Exception as e:
                last_error = e
                time.sleep(self.retry_delay * (attempt + 1))
        if last_error:
            raise last_error
        raise RuntimeError("Unknown error in retry_on_error")

    @staticmethod
    def detect_validation_errors(page) -> list:
        error_selectors = [
            "div[role='alert']",
            "span[class*='error']",
            "div[class*='error']",
            ".v-error-message"
        ]
        errors = []
        for selector in error_selectors:
            elements = page.locator(selector).all()
            for el in elements:
                try:
                    text = el.inner_text().strip()
                    if text:
                        errors.append(text)
                except Exception:
                    continue
        return errors

    @staticmethod
    def detect_captcha(page) -> bool:
        captcha_selectors = [
            "iframe[src*='recaptcha']",
            "iframe[src*='captcha']",
            "div.g-recaptcha",
            "div[class*='captcha']"
        ]
        for selector in captcha_selectors:
            if page.locator(selector).count() > 0:
                return True
        return False

    @staticmethod
    def wait_for_submission_confirmation(page, timeout: int = 10000) -> bool:
        confirmation_selectors = [
            "text='Your response has been recorded'",
            "text='Response recorded'",
            "div[role='heading']:has-text('Response')",
            ".freebirdFormviewerViewResponseConfirmContent"
        ]
        for selector in confirmation_selectors:
            try:
                page.wait_for_selector(selector, timeout=timeout)
                return True
            except Exception:
                continue
        return False
