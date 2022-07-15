#!/usr/bin/python3
# -*- coding: utf-8 -*-

import platform
import shutil
import sys
import os


service_data = """[Unit]
Description=/usr/bin/python3 {}/main.py
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 $DevBranch_RPC/main.py
ExecReload=/usr/bin/python3 $DevBranch_RPC/main.py
ExecReload=/bin/kill $DevBranch_RPC/main.py

[Install]
WantedBy=multi-user.target
Alias=devbranch.service
"""


def check_os():
    if 'ubuntu' not in platform.version().lower():
        raise OSError("This service installation script supports only the Ubuntu and maybe Linux Mint / Debian (not tested).")
        sys.exit()


def check_privileges():
    if not os.environ.get("SUDO_UID") and os.geteuid() != 0:
        raise PermissionError("You need to run this script with sudo or as root. Needs to add DevBranch RPC as service.")
        sys.exit()


def copy_project():
    def copy(path=None):
        _dir = path or os.getcwd()
        dest_dir = os.path.expanduser('~') + '/.DevBranchRPC'
        
        for filename in os.listdir(_dir):
            # construct full file path
            source = source_folder + filename
            destination = dest_dir + filename
            
            # copy only files
            if os.path.isfile(source):
                shutil.copy(source, destination)
                print('copied', file_name)
            elif os.path.isdir(source):
                copy(source)
    copy()
    
    print(
        'Copied project to', os.path.expanduser('~') + '/.DevBranchRPC',
        '\nDo not remove this directory!'
    )


def install_service():
    with open('/lib/systemd/system/devbranch.service', 'w') as file:
        file.write(service_data)
    print('Installed service to /lib/systemd/system/devbranch.service')


def reload_daemon():
    
    
    print('Reload daemon')


if __name__ == '__main__':
    check_os()
    check_privileges()
    
    add_env()
    copy_project()
    
    install_service()
    reload_daemon()