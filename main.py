import time as time_obj
from datetime import datetime, time
from zoneinfo import ZoneInfo
from threading import Timer
import subprocess
import sys
import ctypes
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def set_chrome_settings():
    chrome_options = Options()
    args = [
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-sync",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-client-side-phishing-detection",
        "--disable-default-apps",
        "--disable-hang-monitor",
        "--disable-popup-blocking",
        "--disable-prompt-on-repost",
        "--disable-translate",
        "--disable-infobars",
        "--metrics-recording-only",
        "--no-first-run",
        "--safebrowsing-disable-auto-update",
        "--mute-audio",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage"
    ]

    for arg in args:
        chrome_options.add_argument(arg)

    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.fonts": 2,
        "profile.managed_default_content_settings.plugins": 2,
        "profile.managed_default_content_settings.popups": 2,
        "profile.managed_default_content_settings.geolocation": 2,
        "profile.managed_default_content_settings.notifications": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    chrome_service = Service("./chromedriver.exe")
    chrome_service.creation_flags = 0x8000000  # Suppress logs

    return chrome_service, chrome_options

def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("This script needs to be run as Administrator. Re-launching with elevated privileges...")
        # Relaunch the script with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()  # Exit the original script

def sync_windows_time():
    try:
        # Start the Windows Time service if it's not running
        subprocess.run(["net", "start", "w32time"], shell = True, check = False)

        # Resync time
        subprocess.run(["w32tm", "/resync"], shell = True, check = True)
        print("Time successfully synchronized with Windows Time Server.")

    except subprocess.CalledProcessError as e:
        print("Error syncing time. Please run this program as Administrator.", e)

if __name__ == "__main__":
    # Running the script as Administrator is required for syncing the time
    run_as_admin()

    # Get screen dimensions
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    # Initialize ChromeDriver with optimizations
    chrome_service, chrome_options = set_chrome_settings()
    driver = webdriver.Chrome(service = chrome_service, options = chrome_options)
    driver.set_window_size(screen_width / 2, screen_height)
    driver.get("https://wd10.myworkday.com/ubc/d/home.htmld")

    # Wait until exactly the course registration time in PST (24-hour time)
    pst_tz = ZoneInfo("America/Los_Angeles")
    year = datetime.now(pst_tz).year
    month = datetime.now(pst_tz).month
    day = datetime.now(pst_tz).day
    second = 0
    microsecond = 0
    ### MODIFY TO MATCH YOUR COURSE REGISTRATION TIME IN PST (24-hour time) ###
    hour = #
    minute = #

    reg_time = time(hour, minute)
    form_reg_time = reg_time.strftime("%I:%M %p").lstrip("0").lower()  # Formatted as 12-hour time
    input(f"Welcome to UBC Course Sniper!\nInstructions:\n 1. ⭐ENSURE YOUR COURSE REGISTRATION TIME (PST) IS SET CORRECTLY!⭐\n    You have set your course registration time to {form_reg_time} PST.\n 2. Manually log in to UBC Workday with your CWL.\n 3. Open the Saved Schedule you want to register.\n 4. Press `Enter` in the terminal to start the script.")

    sync_windows_time()

    target_time = datetime(year, month, day, hour, minute, second, microsecond, pst_tz)
    now = datetime.now(pst_tz)
    if now > target_time:
        print(f"\nIt is past {form_reg_time}.")
    else:
        seconds_to_target = (target_time - now).total_seconds()
        Timer(seconds_to_target - 15.000, driver.refresh).start() # Preemptive refresh for caching
        wait_seconds = seconds_to_target - 0.150  # Decreased wait time to ensure scripts starts as close to the opening time as possible
        print(f"\nWaiting {wait_seconds:.3f} seconds until {form_reg_time}.\nThe page will refresh 15 seconds before the target time.\nDO NOT TOUCH YOUR COMPUTER except to ensure that it does not fall asleep.")
        time_obj.sleep(wait_seconds)

    # Refresh the page at the target time
    print("\nTarget time reached. Refreshing the page...")
    driver.refresh()

    try:
        register_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Start Registration')]")))
        register_button.click()
        print("\nClicked 'Start Registration'")

        confirm_register_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Register')]")))
        confirm_register_button.click()
        print("\nClicked 'Register'")

        print("\nCourse registration successful. Close Chrome and the terminal to exit.")

    except Exception as e:
        print("\nERROR FINDING/CLICKING REGISTRATION BUTTON(S). Close Chrome and the terminal to exit.\n", e)

    time_obj.sleep(999999) # Keep Chrome open (for ~11 days)

    # Cleanup (optional)
    # driver.quit()