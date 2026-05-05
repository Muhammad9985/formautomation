# Google Forms Automation Tool 🤖

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.40+-green.svg)](https://playwright.dev/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A powerful, fully dynamic Google Forms automation tool that intelligently analyzes any form and fills it with realistic, context-aware data. Built with advanced form detection, persona-based data generation, and human-like interaction patterns.

## 🌟 Features

### Core Capabilities
- **Fully Dynamic Form Detection** - Automatically detects and analyzes ANY Google Form regardless of topic, language, or structure
- **Context-Aware Data Generation** - Analyzes form title and field labels to understand context (Medical, IT, Education, Business, Events, etc.)
- **Persona-Based Consistency** - Generates consistent user personas where email matches name, phone matches location, etc.
- **Pakistani Data Sets** - Uses realistic Pakistani names, cities, phone numbers, and addresses
- **Smart Field Detection** - Handles all Google Forms field types:
  - ✅ Text inputs (short/long answer)
  - ✅ Email fields
  - ✅ Radio buttons (with "Other" option skipping)
  - ✅ Checkboxes (selects ALL valid options)
  - ✅ Dropdown menus
  - ✅ Linear scales
  - ✅ Date pickers
  - ✅ File uploads

### Intelligence Features
- **Automatic "Other" Detection** - Skips "Other" options with input fields to prevent contamination
- **Multi-Page Form Support** - Automatically navigates through paginated forms
- **Form Context Analysis** - Detects form topic and generates relevant responses
- **Subjective Response Generation** - Creates context-aware feedback/comments

### Stealth & Human Simulation
- **Human-Like Typing** - Configurable WPM (words per minute) with natural variations
- **Random Delays** - Configurable pauses between fields and submissions
- **Rate Limiting** - Built-in rate limiting (per minute/hour) to avoid detection
- **User Agent Rotation** - Randomizes browser user agents
- **Proxy Support** - Optional proxy configuration
- **Cookie Management** - Load/save browser cookies

### Technical Features
- **Screenshot Capture** - Automatically saves screenshots of successful submissions
- **Detailed Logging** - CSV export of all submissions with timestamps
- **Error Handling** - Robust error handling with retry logic
- **CAPTCHA Detection** - Automatically detects and stops on CAPTCHA
- **Sign-in Modal Dismissal** - Handles Google's "Sign in to continue" popup

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Muhammad9985/formautomation.git
cd formautomation
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

## 📋 Usage

### Basic Usage (GUI)
```bash
python gui.py
```
The GUI provides an easy interface to:
- Enter Google Form URL
- Set number of submissions
- Configure settings
- Monitor progress
- View submission logs

### Advanced Usage (Programmatic)
```python
from form_filler import FormFiller
from config import Config
from logger import SubmissionLogger
from screenshot_manager import ScreenshotManager

# Load or create config
config = Config(
    headless=False,  # Set to True for headless mode
    typing_speed_min_wpm=50,
    typing_speed_max_wpm=150,
    delay_between_fields_min=1.0,
    delay_between_fields_max=3.0,
    rate_limit_per_minute=10,
    rate_limit_per_hour=100,
    skip_other_options=True,  # Skip "Other" options
)

# Initialize components
logger = SubmissionLogger()
screenshot_mgr = ScreenshotManager(config)

# Create filler and run
filler = FormFiller(config, logger, screenshot_mgr)
results = filler.run_multiple(
    form_url="https://docs.google.com/forms/d/e/YOUR_FORM_ID/viewform",
    count=50  # Number of submissions
)
```

## ⚙️ Configuration

Edit `config.py` or create a `config.json`:

```json
{
    "typing_speed_min_wpm": 50,
    "typing_speed_max_wpm": 150,
    "delay_between_fields_min": 1.0,
    "delay_between_fields_max": 3.0,
    "delay_between_submissions_min": 5.0,
    "delay_between_submissions_max": 15.0,
    "rate_limit_per_minute": 10,
    "rate_limit_per_hour": 100,
    "headless": false,
    "skip_other_options": true,
    "generate_file_uploads": true,
    "screenshot_base_path": "screenshots",
    "log_path": "exports/submissions.csv"
}
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `typing_speed_min_wpm` | Minimum typing speed (WPM) | 50 |
| `typing_speed_max_wpm` | Maximum typing speed (WPM) | 150 |
| `delay_between_fields_min` | Minimum delay between fields (seconds) | 1.0 |
| `delay_between_fields_max` | Maximum delay between fields (seconds) | 3.0 |
| `delay_between_submissions_min` | Minimum delay between submissions | 5.0 |
| `delay_between_submissions_max` | Maximum delay between submissions | 15.0 |
| `rate_limit_per_minute` | Max submissions per minute | 10 |
| `rate_limit_per_hour` | Max submissions per hour | 100 |
| `headless` | Run browser in headless mode | false |
| `skip_other_options` | Skip "Other" options with input fields | true |
| `generate_file_uploads` | Generate dummy files for upload fields | true |

## 🧠 How It Works

### 1. Form Analysis
The tool analyzes the form by:
- Extracting the form title
- Detecting all field labels and types
- Determining the form context (Medical, IT, Education, Business, etc.)
- Generating a consistent persona for each submission

### 2. Persona Generation
Each submission gets a unique persona with:
- Pakistani name (e.g., "Muhammad Ali", "Fatima Khan")
- Matching email (e.g., "muhammad.ali786@gmail.com")
- Pakistani phone number (+92 3xx format)
- Pakistani city and address
- Context-appropriate department, job title, education level

### 3. Form Filling
- **Text Fields**: Human-like typing with natural speed variations
- **Radio Buttons**: Randomly selects valid options (skips "Other")
- **Checkboxes**: Selects ALL valid options (skips "Other")
- **Dropdowns**: Randomly selects from valid options
- **Linear Scales**: Fills with appropriate values
- **Multi-page**: Automatically clicks "Next" and continues

## 📁 Project Structure

```
fromautomation/
├── form_filler.py          # Main form filling logic
├── form_detector.py        # Google Forms field detection
├── dynamic_data_generator.py # Context-aware data generation
├── human_behavior.py       # Human-like interaction simulation
├── config.py               # Configuration management
├── gui.py                  # Graphical user interface
├── logger.py               # Submission logging
├── screenshot_manager.py   # Screenshot capture
├── error_handler.py        # Error handling and retries
├── utils.py                # Utility functions
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── exports/               # Submission logs (CSV)
├── screenshots/           # Captured screenshots
└── README.md             # This file
```

## 🛠️ Technologies Used

- **Python 3.10+** - Core programming language
- **Playwright** - Browser automation and form interaction
- **Dataclasses** - Configuration and data structures
- **Type Hints** - Type checking with mypy
- **Ruff** - Fast Python linter
- **pytest** - Testing framework (if applicable)

## 📊 Example Output

```
[INFO] Form Context: survey
[INFO] Topic: Patient Satisfaction Survey
[INFO] Industry: Healthcare
[INFO] Keywords: patient, satisfaction, care, service
[INFO] Submitting 1/50...
[INFO] Submission 1 successful (Duration: 4.2s)
[INFO] Submitting 2/50...
[INFO] Submission 2 successful (Duration: 3.8s)
...
```

## ⚠️ Important Notes

1. **Terms of Service** - Ensure you have permission to automate form submissions. Respect website terms of service.
2. **Rate Limiting** - Use appropriate delays to avoid overwhelming servers.
3. **Data Privacy** - This tool generates FAKE data. Do not use with real personal information.
4. **CAPTCHA** - The tool will stop if CAPTCHA is detected. Manual intervention required.
5. **Testing** - Always test with a small number of submissions first.

## 🐛 Troubleshooting

### Form Fields Not Detected
- Make sure the form URL is correct (should be `/viewform` or `/edit` URL)
- Check if the form requires sign-in (tool tries to dismiss the modal)
- Try increasing delays in config

### Email/Name Mismatch
- The tool generates Pakistani names with matching emails
- Emails use @gmail.com only with variations (e.g., name123@gmail.com)

### "Other" Options Still Selected
- Verify `skip_other_options: true` in config
- The tool detects "Other:", "Other (please specify)", etc.

## 👤 Author

**Muhammad Rafique**
- Portfolio: [mr-software.online](https://mr-software.online/)
- GitHub: [@Muhammad9985](https://github.com/Muhammad9985/formautomation)
- LinkedIn: [muhammad-rafique](https://www.linkedin.com/in/muhammad-rafique-944b05159/)
- Email: [rafiqalbaloshi3@gmail.com](mailto:rafiqalbaloshi3@gmail.com)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Forms team for the platform
- Playwright team for the excellent automation library
- All contributors and testers

---

⭐ **Star this repository if you find it useful!** ⭐
