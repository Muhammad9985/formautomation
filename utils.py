import time
import json
import random
import urllib.robotparser
from typing import Optional, Dict, List
from urllib.parse import urlparse

def check_robots_txt(form_url: str, timeout: int = 10) -> bool:
    """Check if form URL is allowed by robots.txt. Returns True if allowed."""
    try:
        parsed = urlparse(form_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch("*", form_url)
    except Exception:
        return True

class RateLimiter:
    def __init__(self, per_minute: int = 10, per_hour: int = 100):
        self.per_minute = per_minute
        self.per_hour = per_hour
        self.minute_timestamps: List[float] = []
        self.hour_timestamps: List[float] = []

    def wait_if_needed(self) -> None:
        now = time.time()
        self.minute_timestamps = [t for t in self.minute_timestamps if now - t < 60]
        self.hour_timestamps = [t for t in self.hour_timestamps if now - t < 3600]

        if len(self.minute_timestamps) >= self.per_minute:
            wait_time = 60 - (now - self.minute_timestamps[0]) + random.uniform(0.5, 2.0)
            if wait_time > 0:
                time.sleep(wait_time)
                now = time.time()

        if len(self.hour_timestamps) >= self.per_hour:
            wait_time = 3600 - (now - self.hour_timestamps[0]) + random.uniform(5.0, 15.0)
            if wait_time > 0:
                time.sleep(wait_time)
                now = time.time()

        self.minute_timestamps.append(now)
        self.hour_timestamps.append(now)

def load_cookies(path: str) -> Optional[Dict]:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_cookies(cookies: List[Dict], path: str) -> None:
    with open(path, "w") as f:
        json.dump(cookies, f, indent=2)

def get_proxy_config(proxy_url: Optional[str]) -> Optional[Dict]:
    if not proxy_url:
        return None
    return {"server": proxy_url}

def random_mouse_movement(start_x: int, start_y: int, end_x: int, end_y: int, steps: int = 10) -> List[tuple]:
    """Generate intermediate points for a natural mouse movement curve."""
    points = []
    for i in range(steps + 1):
        t = i / steps
        # Add slight curve using sine wave
        offset_x = (end_x - start_x) * t + random.randint(-10, 10) * (1 - abs(2*t - 1))
        offset_y = (end_y - start_y) * t + random.randint(-10, 10) * (1 - abs(2*t - 1))
        points.append((int(start_x + offset_x), int(start_y + offset_y)))
    return points
