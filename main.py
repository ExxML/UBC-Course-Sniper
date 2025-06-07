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

    input("Welcome to UBC Course Sniper!\nPlease first follow these steps:\n 1. ⭐⭐⭐⭐⭐ SYNC YOUR COMPUTER TIME!⭐⭐⭐⭐⭐\n 2. Manually log in to UBC Workday with your CWL\n 3. Open the `Saved Schedule` page of the schedule you want to register\n 4. Once you are on the page, press `Enter` in the terminal to continue.")

    # Wait until exactly the course registration date (in 24-hour time)
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    second = 0
    microsecond = 0

    ### MODIFY TO MATCH YOUR COURSE REGISTRATION TIME ###
    hour = 17
    minute = 48
     ### MODIFY TO MATCH YOUR COURSE REGISTRATION TIME ###

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
    print("Refreshing the page.")

    try:
        register_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Start Registration')]")))
        register_button.click()
        print("Clicked 'Start Registration'")

        confirm_register_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Register')]")))
        confirm_register_button.click()
        print("Clicked 'Register'")
    except Exception as e:
        print("Could not find or click the registration button(s).", e)

    time.sleep(999999) # Keep chrome open (for ~11 days)

    # Cleanup (optional)
    # driver.quit()