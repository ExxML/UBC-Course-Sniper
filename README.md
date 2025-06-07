# UBC Course Sniper

UBC Course Sniper is a Python script for Windows that automates the process of registering for courses through a Saved Schedule on UBC Workday. It allows users to specify a target time and automatically clicks the registration buttons when the time arrives.

## Installation

1. Install Python 3.12.
2. Initialize a virtual environment and install the required dependencies by running:
```bash
pip install -r requirements.txt
```
3. **Find your version of Google Chrome and download the corresponding ChromeDriver version [here](https://googlechromelabs.github.io/chrome-for-testing/)**. 
4. Move `chromedriver.exe` into the project folder (at the same level as `main.py`).

## Usage

1. ⭐ **IMPORTANT:** Before running the program, go into `main.py` and modify the `hour` and `minute` variables to match your course registration time! These variables are marked with the comment: `### MODIFY TO MATCH YOUR REGISTRATION TIME ###`. ⭐
2. Run `main.py`. **You will be prompted to run the program as Administrator so that your computer time can be automatically synced.**
3. In the Chrome window that opens, log in to UBC Workday with your CWL.
4. Open the Saved Schedule you want to register.
![alt text](SavedSchedulePreview.png)
5. Once you are on this page, press `Enter` in the terminal to start the script.
6. The script will wait until the target time to refresh the page and automatically click the registration buttons.