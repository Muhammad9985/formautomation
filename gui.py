from tkinter import messagebox, filedialog, ttk
import tkinter as tk
import threading
from PIL import Image, ImageTk
from config import Config
from logger import SubmissionLogger
from screenshot_manager import ScreenshotManager
from form_filler import FormFiller
import datetime

class FormAutomationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Google Forms Automation Tool")
        self.root.geometry("1000x800")
        self.root.configure(bg="gray20")

        messagebox.showinfo(
            "Ethical Use Disclaimer",
            "This tool is for legitimate form testing purposes only.\n"
            "Do not use for spam, unauthorized submissions, or illegal activity.\n"
            "Respect Google Forms' Terms of Service and rate limits."
        )

        self.config = Config.load("config.json")
        self.logger = SubmissionLogger(self.config.log_path)
        self.screenshot_mgr = ScreenshotManager(self.config.screenshot_base_path)
        self.stop_flag = False
        self.automation_thread = None
        self.success_count = 0
        self.fail_count = 0

        self._setup_widgets()

    def _setup_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg="gray20")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # URL Section
        url_frame = tk.Frame(main_frame, bg="gray20")
        url_frame.pack(fill="x", pady=(0, 10))
        tk.Label(url_frame, text="Form URL:", font=("Arial", 12, "bold"), bg="gray20", fg="white").pack(side="left", padx=5)
        self.url_entry = tk.Entry(url_frame, font=("Arial", 11))
        self.url_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.url_entry.bind("<Control-v>", self._paste_url)

        # Settings Section
        settings_frame = tk.Frame(main_frame, bg="gray20")
        settings_frame.pack(fill="x", pady=(0, 10))

        # Left column
        left_col = tk.Frame(settings_frame, bg="gray20")
        left_col.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(left_col, text="Submissions:", font=("Arial", 11), bg="gray20", fg="white").pack(anchor="w", padx=5, pady=(5, 0))
        self.submission_count = ttk.Combobox(left_col, values=[str(i) for i in [1, 5, 10, 25, 50, 100, 200, 300, 500, 1000]], height=20)
        self.submission_count.set("300")
        self.submission_count.pack(fill="x", padx=5, pady=5)

        tk.Label(left_col, text="Delay Between Fields (s):", font=("Arial", 11), bg="gray20", fg="white").pack(anchor="w", padx=5, pady=(5, 0))
        self.field_delay = ttk.Scale(left_col, from_=0.5, to=10.0)
        self.field_delay.set(self.config.delay_between_fields_max)
        self.field_delay.pack(fill="x", padx=5, pady=(0, 5))
        self.field_delay_label = tk.Label(left_col, text=f"{self.config.delay_between_fields_max:.1f}s", bg="gray20", fg="white")
        self.field_delay_label.pack(anchor="e", padx=5)

        # Right column
        right_col = tk.Frame(settings_frame, bg="gray20")
        right_col.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(right_col, text="Delay Between Submissions (s):", font=("Arial", 11), bg="gray20", fg="white").pack(anchor="w", padx=5, pady=(5, 0))
        self.sub_delay = ttk.Scale(right_col, from_=5, to=60)
        self.sub_delay.set(self.config.delay_between_submissions_max)
        self.sub_delay.pack(fill="x", padx=5, pady=(0, 5))
        self.sub_delay_label = tk.Label(right_col, text=f"{self.config.delay_between_submissions_max:.0f}s", bg="gray20", fg="white")
        self.sub_delay_label.pack(anchor="e", padx=5)

        self.headless_var = tk.BooleanVar(value=self.config.headless)
        self.headless_check = tk.Checkbutton(right_col, text="Headless Mode", variable=self.headless_var, bg="gray20", fg="white", selectcolor="gray20")
        self.headless_check.pack(anchor="w", padx=5, pady=5)

        # Buttons
        btn_frame = tk.Frame(main_frame, bg="gray20")
        btn_frame.pack(fill="x", pady=(0, 10))

        self.start_btn = tk.Button(btn_frame, text="Start", command=self.start_automation, height=2, font=("Arial", 12, "bold"), bg="green", fg="white")
        self.start_btn.pack(side="left", padx=5, fill="x", expand=True)

        self.stop_btn = tk.Button(btn_frame, text="Stop", command=self.stop_automation, height=2, font=("Arial", 12, "bold"), bg="red", fg="white", state="disabled")
        self.stop_btn.pack(side="left", padx=5, fill="x", expand=True)

        self.reset_btn = tk.Button(btn_frame, text="Reset", command=self.reset_form, height=2, font=("Arial", 12))
        self.reset_btn.pack(side="left", padx=5, fill="x", expand=True)

        self.export_btn = tk.Button(btn_frame, text="Export CSV", command=self.export_csv, height=2, font=("Arial", 12))
        self.export_btn.pack(side="left", padx=5, fill="x", expand=True)

        # Progress
        progress_frame = tk.Frame(main_frame, bg="gray20")
        progress_frame.pack(fill="x", pady=(0, 10))

        self.progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress.pack(fill="x", padx=5, pady=5)
        self.progress['value'] = 0

        self.progress_label = tk.Label(progress_frame, text="0 / 0", font=("Arial", 11), bg="gray20", fg="white")
        self.progress_label.pack(padx=5)

        # Status and Stats
        status_frame = tk.Frame(main_frame, bg="gray20")
        status_frame.pack(fill="x", pady=(0, 10))

        self.status_label = tk.Label(status_frame, text="Ready", anchor="w", font=("Arial", 12), bg="gray20", fg="lightblue")
        self.status_label.pack(side="left", fill="x", expand=True, padx=5)

        self.success_label = tk.Label(status_frame, text="Success: 0", fg="lightgreen", font=("Arial", 12, "bold"), bg="gray20")
        self.success_label.pack(side="left", padx=10)

        self.fail_label = tk.Label(status_frame, text="Fail: 0", fg="lightcoral", font=("Arial", 12, "bold"), bg="gray20")
        self.fail_label.pack(side="left", padx=10)

        # Content area with screenshot and error log
        content_frame = tk.Frame(main_frame, bg="gray20")
        content_frame.pack(fill="both", expand=True)

        # Screenshot preview
        screenshot_frame = tk.Frame(content_frame, bg="gray20")
        screenshot_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        tk.Label(screenshot_frame, text="Latest Screenshot:", font=("Arial", 11, "bold"), bg="gray20", fg="white").pack(pady=(5, 0))
        self.screenshot_label = tk.Label(screenshot_frame, text="No screenshot yet", width=50, height=20, bg="gray30")
        self.screenshot_label.pack(padx=5, pady=5, fill="both", expand=True)

        # Error Log
        log_frame = tk.Frame(content_frame, bg="gray20")
        log_frame.pack(side="left", fill="both", expand=True, padx=(5, 0))

        tk.Label(log_frame, text="Error Log:", font=("Arial", 11, "bold"), bg="gray20", fg="white").pack(pady=(5, 0), anchor="w", padx=5)

        self.error_log = tk.Text(log_frame, height=12, font=("Consolas", 10))
        self.error_log.pack(fill="both", expand=True, padx=5, pady=5)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def _paste_url(self, event=None):
        try:
            url = self.root.clipboard_get()
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, url)
        except Exception:
            pass
        return "break"

    def _log_error(self, msg):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {msg}\n"
        self.error_log.insert("end", formatted)
        self.error_log.see("end")
        try:
            with open("error_log.txt", "a", encoding="utf-8") as f:
                f.write(formatted)
        except Exception:
            pass

    def _update_status(self, msg, is_error=False):
        color = "lightcoral" if is_error else "lightblue"
        self.root.after(0, lambda: self.status_label.configure(text=msg, fg=color))

    def _update_progress(self, current, total):
        self.root.after(0, lambda: self.progress.configure(value=(current / total) * 100))
        self.root.after(0, lambda: self.progress_label.configure(text=f"{current} / {total}"))

    def _update_screenshot(self, path):
        def _update():
            try:
                img = Image.open(path)
                img.thumbnail((350, 250))
                photo = ImageTk.PhotoImage(img)
                self.screenshot_label.configure(image=photo, text="")
                self.screenshot_label.image = photo
            except Exception:
                self.screenshot_label.configure(text="Screenshot load error", image=None)
        self.root.after(0, _update)

    def start_automation(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a Google Form URL")
            return

        self.success_count = 0
        self.fail_count = 0
        self.success_label.configure(text="Success: 0")
        self.fail_label.configure(text="Fail: 0")
        self.error_log.delete("1.0", "end")

        self.config.headless = self.headless_var.get()
        self.config.delay_between_fields_min = 0.5
        self.config.delay_between_fields_max = self.field_delay.get()
        self.config.delay_between_submissions_min = 5.0
        self.config.delay_between_submissions_max = self.sub_delay.get()

        count = int(self.submission_count.get())
        self.progress['maximum'] = count
        self.progress['value'] = 0
        self.progress_label.configure(text=f"0 / {count}")

        self.stop_flag = False
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")

        self.automation_thread = threading.Thread(
            target=self._run_automation, args=(url, count), daemon=True
        )
        self.automation_thread.start()

    def _run_automation(self, form_url, count):
        filler = FormFiller(self.config, self.logger, self.screenshot_mgr)
        for i in range(1, count + 1):
            if self.stop_flag:
                self._update_status("Stopped by user", is_error=True)
                self._log_error("Automation stopped by user")
                break

            self._update_status(f"Submitting {i}/{count}...")
            try:
                filler.fill_submission(form_url, i)
                self.success_count += 1
                self.root.after(0, lambda sc=self.success_count: self.success_label.configure(text=f"Success: {sc}"))
                self._update_progress(i, count)
                paths = self.screenshot_mgr.get_screenshot_paths()
                if paths:
                    self._update_screenshot(paths[-1])
            except Exception as e:
                self.fail_count += 1
                import traceback
                error_detail = traceback.format_exc()
                error_short = f"{type(e).__name__}: {str(e)[:100]}"
                self.root.after(0, lambda fc=self.fail_count: self.fail_label.configure(text=f"Fail: {fc}"))
                self._log_error(f"Submission {i} FAILED")
                self._log_error(f"  Error: {error_short}")
                self._log_error("  See error_log.txt for full traceback")
                self._update_status(f"{error_short[:50]}...", is_error=True)
                try:
                    with open("error_log.txt", "a", encoding="utf-8") as f:
                        f.write(f"\n{'='*60}\n")
                        f.write(f"SUBMISSION {i} ERROR at {datetime.datetime.now()}\n")
                        f.write(f"{'='*60}\n")
                        f.write(error_detail)
                        f.write("\n")
                except Exception:
                    pass
            self._update_status(f"Completed {i}/{count}")

        filler._close_browser()
        final_msg = f"Done. {self.success_count} Success, {self.fail_count} Fail"
        self._update_status(final_msg)
        self._log_error(final_msg)
        self.root.after(0, lambda: self.start_btn.configure(state="normal"))
        self.root.after(0, lambda: self.stop_btn.configure(state="disabled"))

    def stop_automation(self):
        self.stop_flag = True
        self._update_status("Stopping...", is_error=True)
        self._log_error("Stop requested")

    def reset_form(self):
        self.url_entry.delete(0, "end")
        self.submission_count.set("1")
        self.progress.configure(value=0)
        self.progress_label.configure(text="0 / 0")
        self._update_status("Ready")
        self.screenshot_label.configure(image=None, text="No screenshot yet")
        self.error_log.delete("1.0", "end")
        self.stop_flag = False
        self.success_count = 0
        self.fail_count = 0
        self.success_label.configure(text="Success: 0")
        self.fail_label.configure(text="Fail: 0")
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]
        )
        if path:
            self.logger.export_csv(path)
            messagebox.showinfo("Success", f"Exported to {path}")
