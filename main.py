import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if __name__ == "__main__":
    # Initialize ChromeDriver and suppress logging
    service = Service("./chromedriver.exe")
    service.creation_flags = 0x8000000  # Suppress logs
    driver = webdriver.Chrome(service = service)
    driver.get("https://wd10.myworkday.com/ubc/d/home.htmld")

    # Wait until exactly the course registration time (in 24-hour time)
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    second = 0
    microsecond = 0
    ### MODIFY TO MATCH YOUR COURSE REGISTRATION TIME ###
    hour = #
    minute = #
    ### MODIFY TO MATCH YOUR COURSE REGISTRATION TIME ###

    input(f"\nWelcome to UBC Course Sniper!\nInstructions:\n 1. ⭐ ENSURE YOUR COURSE REGISTRATION TIME IS SET CORRECTLY! ⭐\n    Your course registration time is {hour:02}:{minute:02}.\n 2. ⭐ SYNC YOUR COMPUTER TIME! ⭐\n 3. Manually log in to UBC Workday with your CWL\n 4. Open the Saved Schedule you want to register\n 5. Press `Enter` in the terminal to start the script")

    target_time = datetime.datetime.now().replace(year, month, day, hour, minute, second, microsecond)
    now = datetime.datetime.now()
    if now > target_time:
            print(f"It is past {hour:02}:{minute:02}.")
    else:
        wait_seconds = (target_time - now).total_seconds() + 0.005
        print(f"Waiting {wait_seconds:.3f} seconds until {hour:02}:{minute:02}.\nDO NOT TOUCH YOUR COMPUTER except to ensure that it does not fall asleep.")
        time.sleep(wait_seconds)

    # Refresh the page at the target time
    driver.refresh()
    print("Refreshing the page...")

    try:
        register_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Start Registration')]")))
        register_button.click()
        print("Clicked 'Start Registration'")

        confirm_register_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Register')]")))
        confirm_register_button.click()
        print("Clicked 'Register'")

        time.sleep(999999) # Keep Chrome open (for ~11 days)
    except Exception as e:
        print("ERROR: Could not find or click the registration button(s).")

    # Cleanup (optional)
    # driver.quit()