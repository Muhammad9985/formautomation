import os
from datetime import datetime
from typing import Optional
from playwright.sync_api import Page

class ScreenshotManager:
    def __init__(self, base_path: str = "screenshots"):
        self.base_path = base_path

    def _get_date_folder(self) -> str:
        date_str = datetime.now().strftime("%Y-%m-%d")
        folder = os.path.join(self.base_path, date_str)
        os.makedirs(folder, exist_ok=True)
        return folder

    def save_screenshot(self, page: Page, submission_id: int, suffix: str = "") -> str:
        folder = self._get_date_folder()
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"submission_{submission_id:04d}_{timestamp}{suffix}.png"
        path = os.path.join(folder, filename)
        page.screenshot(path=path, full_page=False)
        return path

    def get_screenshot_paths(self, date: Optional[str] = None) -> list:
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        folder = os.path.join(self.base_path, date)
        if not os.path.exists(folder):
            return []
        return sorted([os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".png")])
