import pyipmi
import pyipmi.interfaces
import os
import re
import datetime
import os.path
import time
import math
import numpy
import mmap
import array
import getopt
import sys
from nm_network_handle import *
from os_parameters_define import *
from utility_function import *
from nm_ipmi_raw_to_str import *
from error_messages_define import *
from config import *

##Function :  GET SSH known_hosts FILE PATH
def get_ssh_known_host_path():
     ## DEBUG_OS_TYPE is hard code define in os_parameters_define.py 
     if(DEBUG_OS_TYPE == os_linux):
          SSH_KNOWN_HOST      = LINUX_SSH_KNOWN_HOST_PATH
          SSH_ROOT_KNOWN_HOST = LINUX_SSH_ROOT_KNOWN_HOST_PATH
     elif(DEBUG_OS_TYPE == os_win):
          SSH_KNOWN_HOST      = WIN_SSH_KNOWN_HOST_PATH
          SSH_ROOT_KNOWN_HOST = WIN_SSH_KNOWN_HOST_PATH
     else:
          DEBUG('NO This OS')
          return ERROR, ERROR

     DEBUG('SSH_KNOWN_HOST :'+ SSH_KNOWN_HOST)
     DEBUG('SSH_ROOT_KNOWN_HOST :'+ SSH_ROOT_KNOWN_HOST)
     
     return SSH_KNOWN_HOST, SSH_ROOT_KNOWN_HOST

##Function :  GET NM TEST LIST
def get_test_list_path():
     ## DEBUG_OS_TYPE is hard code define in os_parameters_define.py 
     if(DEBUG_OS_TYPE == os_linux):
          NM_TEST_LIST = NM_TEST_LIST_LINUX
          NM_TEST_FILE = NM_TEST_FILE_LINUX
          SSH_LOG      = SSH_LOG_PATH_LINUX
     elif(DEBUG_OS_TYPE == os_win):
          NM_TEST_LIST = NM_TEST_LIST_WIN
          NM_TEST_FILE = NM_TEST_FILE_WIN
          SSH_LOG      = SSH_LOG_PATH_WIN
     else:
          DEBUG('NO This OS')
          return ERROR, ERROR, ERROR

     DEBUG('NM_TEST_LIST :'+ NM_TEST_LIST)
     DEBUG('NM_TEST_FILE :'+ NM_TEST_FILE)
     DEBUG('SSH_LOG :'+ SSH_LOG)
     
     return NM_TEST_LIST, NM_TEST_FILE, SSH_LOG
     