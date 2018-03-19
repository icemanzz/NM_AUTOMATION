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
from file_path_handle import *
from os_parameters_define import *
from utility_function import *
from nm_ipmi_raw_to_str import *
from error_messages_define import *
from config import *

##Function :  ping parameter detect:
def ping_parameter_detect():
     ## DEBUG_OS_TYPE is hard code define in os_parameters_define.py 
     if(DEBUG_OS_TYPE == os_linux):
          PING_PARAMETER      = LINUX_PING_PARAMETER
     elif(DEBUG_OS_TYPE == os_win):
          PING_PARAMETER      = WIN_PING_PARAMETER
     else:
          DEBUG('NO This OS')
          return ERROR
     DEBUG('PING_PARAMETER :'+ PING_PARAMETER)
     
     return PING_PARAMETER



##Function : SSH CMD SWITCH FOR WIN AND LINUX OS
def ssh_send_cmd_switch( background_run,  PROGRAM_PATH , STRESS_CMD , LOG_SAVE ):
     ## Check Netwrok Configuration : Fix IP / DHCP IP
     if(dhcp_ip_mode_en == 1 ):
          #This IP is Server dynamic assign
          OS_IP = ip_search()
          if(OS_IP == ERROR):
               print('ERROR CAN NOT Find Any IP Available In Target System....')
               return ERROR               
          print('Get Target system IP :' + OS_IP)
     else:
          # This IP is define in os_parameters_define.py
          OS_IP = os_ip_addr
     # Start Send ssh cmd to Target OS IP address
     if(DEBUG_OS_TYPE == os_linux):
          if(background_run == background_run_enable):
                      os.system( LINUX_BACKGROUND_RUN + 'ssh ' + SSH_IGNORE_HOST_KEY + os_user + '@' + OS_IP +' -t sudo ' + PROGRAM_PATH + ' ' + STRESS_CMD + ' &')
          elif(background_run == background_run_disable):
               if(LOG_SAVE == 1):
                      os.system('ssh '+ SSH_IGNORE_HOST_KEY + os_user + '@'+ OS_IP + ' -t sudo ' + PROGRAM_PATH + ' ' + STRESS_CMD + ' > ' + SSH_LOG_PATH_LINUX)
               else:
                      os.system('ssh '+ SSH_IGNORE_HOST_KEY + os_user + '@'+ OS_IP + ' -t sudo ' + PROGRAM_PATH + ' ' + STRESS_CMD)
          else:
               DEBUG('ssh_send_cmd_switch : ERROR!!  Incorrect type of background_run !!')
               return ERROR               
     elif(DEBUG_OS_TYPE == os_win):
          if(background_run == background_run_enable):
                      os.system( WIN_BACKGROUND_RUN + WIN_SSH_PATH + SSH_IGNORE_HOST_KEY + os_user + '@' + OS_IP +' -t sudo ' + PROGRAM_PATH + ' ' + STRESS_CMD + ' &')
          elif(background_run == background_run_disable):
               if(LOG_SAVE == 1):
                      os.system(WIN_SSH_PATH + SSH_IGNORE_HOST_KEY + os_user + '@'+ OS_IP + ' -t sudo ' + PROGRAM_PATH + ' ' + STRESS_CMD + ' > ' + SSH_LOG_PATH_WIN)                 
               else:
                      os.system(WIN_SSH_PATH + SSH_IGNORE_HOST_KEY + os_user + '@'+ OS_IP + ' -t sudo ' + PROGRAM_PATH + ' ' + STRESS_CMD)         
          else:
               DEBUG('ssh_send_cmd_switch : ERROR!!  Incorrect type of background_run !!')
               return ERROR            
     else:
          return ERROR
          
     return SUCCESSFUL

##Function : Define OS IP auto search process
def ip_search():
     # Get OS PING Parameters
     PING_PARAMETER = ping_parameter_detect()   
     ## Check Previous IP data log
     if os.path.isfile(OS_IP_LOG) :
          DEBUG('file exist')
          file = open(OS_IP_LOG, 'r')
          with open(OS_IP_LOG, "r") as ins:
              ip_list = []
              for line in ins:
                  ip_list.append(line.rstrip('\n'))
          file.close()
          DEBUG(ip_list)
          DEBUG('Try previous OS IP : ' + ip_list[0] )
          rsp = os.system('ping '+ PING_PARAMETER + ip_list[0])
          #and then check the response...
          if rsp == 0:
               print ip_list[0], ' is up!'
               print('Set Target IP : ' + ip_list[0])
               return ip_list[0]
          else:
               DEBUG( 'Previous IP ' + ip_list[0] + ' is down! Search New Target IP Again...')
               #delete previous ip log
               os.remove(OS_IP_LOG)
     else:
          DEBUG('previous ip list file not exist, start new search ip process...')

     # Start OS IP re-search process                     
     ip_range = start_ip_range
     for ip_range in range(start_ip_range , end_ip_range ):
          ip_addr  = head_ip_add + str(ip_range)
          rsp = os.system('ping '+ PING_PARAMETER + ip_addr)
          #and then check the response...
          if rsp == 0:
               print ip_addr, ' is up!'
               print('Set Target IP : ' + ip_addr)
               ##Save this OS ip in log file for next reboot re-use
               file = open(OS_IP_LOG, 'w')
               file.write(ip_addr)
               file.close()
               return ip_addr
          else:
               DEBUG( ip_addr + ' is down!')

     print('ERROR!!  Can not find any target IP in netwrok , please check network link and make sure target system boot into OS')
     return ERROR     


     