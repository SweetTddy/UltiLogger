# Keylogger with screen recorder
A keylogger that sends logs on email and records screen.

# Installation

This script requires numpy, pyautogui, opencv, requests, pynput and pypiwin32.

Install packages from Windows console

```bash
pip install numpy pyautogui opencv-python requests pynput pypiwin32
```

# Instructions

- This script requires continuous Internet connection

- Change 171 and 172 lines in Python file to set your email and password **(WORKS ONLY FOR GMAIL MAILBOX)**
```python
171. gmail = 'YOUR_GMAIL'
172. pass_for_gmail = 'YOUR_PASSWORD'
```

- Run script

# IMPORTANT

- Make sure less secure apps mode is enabled in Google account settings
- This app was tested only on Windows 10
