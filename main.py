#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import time
import json

import rpc

from time import mktime
from os import getcwd


class NotFoundActivity(Exception):
    
    def __init__(self, filename: str, message: str):
        self.filename = filename
        self.message = message
        super().__init__(message)
    
    
    def __str__(self):
        return f'Cannot find activity file with name "{self.filename}", make sure the activity file exists in activities folder.'

class DiscordClientError(Exception):
    
    def __str__(self):
        return f'Cannot find the official Discord client application, see #Requirements in README.md'


class RichPresense(object):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.load_data()
        self.configure_cfg()
        self.rpc_init()
        self.event()
    
    
    def load_data(self):
        data = {}
        try:
            with open(f'{getcwd()}/activities/{self.config}', 'r') as file:
                data = json.load(file)
        except FileNotFoundError as error:
            raise NotFoundActivity(self.config, error)
        
        self.activity_name = data['activity_info']['name']
        self.client_id = data['activity_info']['client_id']
        
        # remove unnecassary data
        del data['activity_info']
        
        data['timestamps']['start'] = mktime(time.localtime())
        self.data = data
    
    
    def configure_cfg(self):
        if not self.timetrack:
            del self.data['timestamps']
    
    
    def rpc_init(self):
        try:
            self.rpc = rpc.DiscordIpcClient.for_platform(self.client_id)
        except OSError as error:
            raise NoDiscordClient(error)
    
    
    def event(self):
        while True:
            self.rpc.set_activity(self.data)
            
            time.sleep(1337)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Discord custom DevBranch activity ( Rich Presense ).')
    parser.add_argument('-c', '--config', default='default.json', type=str, help='Activity json file name, should be placed in activities folder.')
    parser.add_argument('-t', '--timetrack', default=True, action='store_false', help='Turn off "time elapsed" when argument specified ')
    args = parser.parse_args()
    
    RichPresense(**vars(args))
