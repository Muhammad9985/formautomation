import random
import time
from typing import Optional
from playwright.sync_api import Page, Locator

class HumanBehavior:
    def __init__(self, config):
        self.config = config
        self.typing_delay_range = config.get_typing_delay_range()

    def random_delay(self, min_sec: float, max_sec: float) -> None:
        time.sleep(random.uniform(min_sec, max_sec))

    def human_type(self, locator: Locator, text: str, page: Optional[Page] = None) -> None:
        """Type text with human-like variable speed and occasional mistakes."""
        locator.click()
        if page:
            page.wait_for_timeout(random.randint(100, 300))

        for i, char in enumerate(text):
            delay = random.randint(*self.typing_delay_range)
            locator.press_sequentially(char, delay=delay)

            # 15% chance to backspace 1-3 characters and retype
            if i > 2 and random.random() < 0.15:
                backspaces = random.randint(1, min(3, i))
                for _ in range(backspaces):
                    locator.press("Backspace")
                if page:
                    page.wait_for_timeout(random.randint(100, 300))
                for j in range(i - backspaces + 1, i + 1):
                    delay = random.randint(*self.typing_delay_range)
                    locator.press_sequentially(text[j], delay=delay)

        if page:
            page.wait_for_timeout(random.randint(200, 500))

    def human_click(self, locator: Locator, page: Page) -> None:
        """Click with human-like mouse movement."""
        if random.random() < 0.3:
            self._random_scroll(page)
        box = locator.bounding_box()
        if box:
            start_x, start_y = random.randint(100, 800), random.randint(100, 600)
            end_x = int(box['x'] + box['width'] / 2 + random.randint(-5, 5))
            end_y = int(box['y'] + box['height'] / 2 + random.randint(-5, 5))
            page.mouse.move(start_x, start_y)
            page.wait_for_timeout(random.randint(50, 150))
            points = self._generate_curve(start_x, start_y, end_x, end_y)
            for px, py in points:
                page.mouse.move(px, py)
                page.wait_for_timeout(random.randint(5, 15))
        locator.click()
        page.wait_for_timeout(random.randint(200, 500))

    def _generate_curve(self, start_x: int, start_y: int, end_x: int, end_y: int, steps: int = 10) -> list:
        points = []
        for i in range(1, steps + 1):
            t = i / steps
            offset_x = (end_x - start_x) * t + random.randint(-8, 8) * (1 - abs(2*t - 1))
            offset_y = (end_y - start_y) * t + random.randint(-8, 8) * (1 - abs(2*t - 1))
            points.append((int(start_x + offset_x), int(start_y + offset_y)))
        return points

    def _random_scroll(self, page: Page) -> None:
        scroll_amount = random.randint(-300, 300)
        page.mouse.wheel(0, scroll_amount)
        page.wait_for_timeout(random.randint(300, 600))

    def tab_navigation(self, page: Page, count: int = 1) -> None:
        for _ in range(count):
            page.keyboard.press("Tab")
            page.wait_for_timeout(random.randint(100, 300))

    def pause_between_fields(self) -> None:
        self.random_delay(
            self.config.delay_between_fields_min,
            self.config.delay_between_fields_max
        )

    def pause_between_submissions(self) -> None:
        self.random_delay(
            self.config.delay_between_submissions_min,
            self.config.delay_between_submissions_max
        )
