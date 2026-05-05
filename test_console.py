import sys
import io

# Capture all output
old_stdout = sys.stdout
old_stderr = sys.stderr
sys.stdout = captured_out = io.StringIO()
sys.stderr = captured_err = io.StringIO()

try:
    print("Testing console for errors...", file=old_stderr)
    
    # Test imports
    print("1. Testing imports...")
    import config
    import logger
    import screenshot_manager
    import form_filler
    print("   All imports OK")
    
    # Test GUI creation
    print("2. Testing GUI...")
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    from gui import FormAutomationGUI
    app = FormAutomationGUI(root)
    print("   GUI created OK")
    print(f"   URL entry: {app.url_entry}")
    print(f"   Success label: {app.success_label.cget('text')}")
    print(f"   Fail label: {app.fail_label.cget('text')}")
    root.destroy()
    
    print("3. Testing FormFiller...")
    config_obj = config.Config()
    logger_obj = logger.SubmissionLogger()
    screenshot_obj = screenshot_manager.ScreenshotManager()
    filler = form_filler.FormFiller(config_obj, logger_obj, screenshot_obj)
    print("   FormFiller created OK")
    
    print()
    print("=== ALL TESTS PASSED ===")
    
except Exception as e:
    import traceback
    print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
    traceback.print_exc()
    
finally:
    # Restore and show output
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    
    print("=== CAPTURED OUTPUT ===")
    print("STDOUT:")
    print(captured_out.getvalue())
    print("STDERR:")
    print(captured_err.getvalue())
