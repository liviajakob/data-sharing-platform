'''
Definitions of global variables
File: definitions.py

Contains:
    ROOT_DIR
    CONFIG_PATH

@author: livia
'''
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is the Project Root
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.conf') # This is where the config file is