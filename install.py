# Install script to install all dependencies Linux machine will need

import subprocess

def installs():
    try:
        subprocess.check_call(['pip', 'install', 'python-can'])
        print('Successfully installed python-can')
    except subprocess.CalledProcessError as e:
        print(f'Failed to install python-can. Error: {e}')

if __name__ == '__main__':
    installs()