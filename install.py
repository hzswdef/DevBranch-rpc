#!/usr/bin/python3
# -*- coding: utf-8 -*-

import platform
import shutil
import sys
import os


service_data = """[Unit]
Description=DevBranch Discord activity status
After=multi-user.target
[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 {}/main.py
[Install]
WantedBy=multi-user.target
"""


def check_os():
    if 'ubuntu' not in platform.version().lower():
        raise OSError("This service installation script supports only the Ubuntu OS.")


def check_privileges():
    if not os.environ.get("SUDO_UID") and os.geteuid() != 0:
        raise PermissionError("You need to run this script with sudo or as root. Needs to add these RPC as service.")
        sys.exit()


def copy_project():
    shutil.copytree(
        os.getcwd(),
        os.path.expanduser('~') + '/.DevBranch-rpc'
    )


def install_service():
    with open('/lib/systemd/system/rpc.service', 'w') as file:
        file.write(service_data.format(os.path.expanduser('~') + '/.DevBranch-rpc'))


if __name__ == '__main__':
    check_os()
    check_privileges()
    
    copy_project()
    
    install_service()