from dataclasses import dataclass, asdict, field
import json
from typing import List, Optional
import random

@dataclass
class Config:
    # Typing speed (WPM range)
    typing_speed_min_wpm: int = 50
    typing_speed_max_wpm: int = 150

    # Delays (seconds)
    delay_between_fields_min: float = 1.0
    delay_between_fields_max: float = 3.0
    delay_between_submissions_min: float = 5.0
    delay_between_submissions_max: float = 15.0
    retry_delay: float = 2.0

    # Retry settings
    max_retries_per_submission: int = 3

    # Rate limiting
    rate_limit_per_minute: int = 10
    rate_limit_per_hour: int = 100

    # Browser settings
    headless: bool = False
    user_agents: List[str] = field(default_factory=lambda: [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ])
    proxy: Optional[str] = None
    cookie_path: str = "cookies.json"

    # Data generation
    skip_other_options: bool = True
    generate_file_uploads: bool = True

    # Screenshots
    screenshot_base_path: str = "screenshots"
    screenshot_format: str = "png"

    # Logging
    log_path: str = "exports/submissions.csv"
    export_path: str = "exports"

    @classmethod
    def load(cls, path: str) -> "Config":
        try:
            with open(path, "r") as f:
                data = json.load(f)
            return cls(**data)
        except FileNotFoundError:
            return cls()

    def save(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=2)

    def get_random_user_agent(self) -> str:
        return random.choice(self.user_agents)

    def get_typing_delay_range(self) -> tuple:
        """Convert WPM to ms per character delay range (min, max)"""
        min_wpm = self.typing_speed_min_wpm
        max_wpm = self.typing_speed_max_wpm
        # 1 word = 5 chars, so chars per minute = wpm * 5
        # ms per char = 60000 / (wpm * 5)
        min_delay = int(60000 / (max_wpm * 5))  # Higher WPM → lower delay
        max_delay = int(60000 / (min_wpm * 5))
        return (min_delay, max_delay)
