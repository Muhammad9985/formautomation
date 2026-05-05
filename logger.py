import csv
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class SubmissionLogger:
    def __init__(self, log_path: str = "exports/submissions.csv"):
        self.log_path = log_path
        self.submissions: List[Dict] = []
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self._ensure_csv_header()

    def _ensure_csv_header(self) -> None:
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "submission_id", "form_url", "status",
                    "error", "duration_seconds", "data_json"
                ])

    def log_submission(
        self,
        submission_id: int,
        form_url: str,
        status: str,
        data: Dict,
        duration: float,
        error: Optional[str] = None
    ) -> None:
        record = {
            "timestamp": datetime.now().isoformat(),
            "submission_id": submission_id,
            "form_url": form_url,
            "status": status,
            "error": error or "",
            "duration_seconds": round(duration, 2),
            "data_json": json.dumps(data, ensure_ascii=False)
        }
        self.submissions.append(record)
        with open(self.log_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=record.keys())
            writer.writerow(record)

    def export_csv(self, export_path: str) -> None:
        flattened = []
        for sub in self.submissions:
            row = {
                "timestamp": sub["timestamp"],
                "submission_id": sub["submission_id"],
                "form_url": sub["form_url"],
                "status": sub["status"],
                "error": sub["error"],
                "duration_seconds": sub["duration_seconds"],
            }
            data = json.loads(sub["data_json"])
            for k, v in data.items():
                row[f"field_{k}"] = v
            flattened.append(row)

        if not flattened:
            return
        with open(export_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=flattened[0].keys())
            writer.writeheader()
            writer.writerows(flattened)

    def get_summary_stats(self) -> Dict:
        total = len(self.submissions)
        if total == 0:
            return {"total": 0, "success_rate": 0, "avg_duration": 0}
        successful = sum(1 for s in self.submissions if s["status"] == "success")
        durations = [s["duration_seconds"] for s in self.submissions if s["status"] == "success"]
        avg_duration = sum(durations) / len(durations) if durations else 0
        return {
            "total": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": round(successful / total * 100, 2),
            "avg_duration_seconds": round(avg_duration, 2)
        }
