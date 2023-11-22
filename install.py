# Install script to install all dependencies Linux machine will need

import subprocess
from getpass import getpass

def installs():
    try:
        password = getpass(prompt="Enter sudo password: ")
    except:
        return
    try:
        subprocess.check_call(['pip', 'install', 'slash'])
        print('Successfully installed slash')
    except subprocess.CalledProcessError as e:
        print(f'Failed to install slash. Error: {e}')
    try:
        subprocess.check_call(['echo', password, '|', 'sudo', 'apt-get', 'install', '-y', 'gpio'], shell=True)
        print('Successfully installed gpio package')
    except subprocess.CalledProcessError as e:
        print(f'Failed to install gpio package. Error: {e}')
    try:
        subprocess.check_call(['echo', password, '|', 'sudo', 'apt-get', 'install', '-y', 'python3-rpi.gpio'], shell=True)
        print('Successfully installed python3-rpi.gpio package')
    except subprocess.CalledProcessError as e:
        print(f'Failed to install python3-rpi.gpio package. Error: {e}')
    try:
        subprocess.check_call(['pip', 'install', 'python-can'])
        print('Successfully installed python-can')
    except subprocess.CalledProcessError as e:
        print(f'Failed to install python-can. Error: {e}')

if __name__ == '__main__':
    installs()