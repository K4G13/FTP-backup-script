from ftplib import FTP
import os
from datetime import datetime
import json

def is_file(filename):
    current = ftp.pwd()
    try:
        ftp.cwd(filename)
    except:
        ftp.cwd(current)
        return True
    ftp.cwd(current)
    return False

def fetch_dir(dir_items,i=0):
    for item in dir_items:
        for _ in range(i): print("   ",end="")
        if is_file(item):
            print(f"\033[32m{item}\033[0m")
            ftp.retrbinary("RETR " + item, open(item, 'wb').write)
        else:
            print(f"\033[33m[{item}]\033[0m")
            ftp.cwd(item)
            os.mkdir(item)
            os.chdir(item)
            new_dir_items = ftp.nlst()
            fetch_dir(new_dir_items,i+1)
            ftp.cwd("..")
            os.chdir("..")

### login_data.json EXAMPLE:
# {
#     "ip": "<your_server_ip>",
#     "user": "<user>",
#     "password": "<passowrd>"
# }

f = open("login_data.json")
login_data = json.load(f)
f.close()

ftp = FTP(login_data['ip'])
ftp.login(login_data['user'],login_data['password'])

backups_dir = os.path.join("backups")
if not os.path.exists(backups_dir):
    os.mkdir(backups_dir)
os.chdir(backups_dir)

time_stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
os.mkdir(time_stamp)
os.chdir(time_stamp)
main_directory = ftp.nlst() 
fetch_dir(main_directory)

ftp.quit()