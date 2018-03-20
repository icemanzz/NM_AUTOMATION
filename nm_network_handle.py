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
          current_os_ip = start_ip_range
          for current_os_ip in range(start_ip_range , end_ip_range):
               #This IP is Server dynamic assign
               OS_IP, ip_range, ip_search_done = ip_search(current_os_ip)
               current_os_ip = ip_range
               if(OS_IP == ERROR):
                    print('ERROR CAN NOT Find Any IP Available In Target System....')
                    return ERROR 
               if(ip_search_done == 1): # break loop
                    current_os_ip = end_ip_range + 1 # break for  loop
               print('Get Target system IP :' + OS_IP)
               if(ip_search_done == 0):
                    ##Save Discoveried DHCP IP
                    file = open(OS_IP_TEST_LIST, 'a')
                    file.write(OS_IP +'\n')
                    file.close()

     else:
          # This IP is define in os_parameters_define.py
          OS_IP = os_ip_addr
     # Prepare IP check list 
     if os.path.isfile(OS_IP_TEST_LIST) and ip_search_done != 1 :
          DEBUG('file exist')
          file = open(OS_IP_TEST_LIST, 'r')
          with open(OS_IP_TEST_LIST, "r") as ins:
              ip_list = []
              for line in ins:
                  ip_list.append(line.rstrip('\n'))
          file.close()
          DEBUG('TEST OS IP LIST : ' + ip_list )         
          # Detect PTU PATH and parameters settings
          PTUGEN_P100_30SECS, PTUMON_3SECS, PTUMON_PATH, PTUGEN_PATH = ptu_parameters_detect(ipmi)
          # Remove old KNOWN_HOST in .ssh folder :
          SSH_KNOWN_HOST, SSH_ROOT_KNOWN_HOST = get_ssh_known_host_path()
          if os.path.isfile(SSH_KNOWN_HOST) :
              os.remove(SSH_KNOWN_HOST)
          if os.path.isfile(SSH_ROOT_KNOWN_HOST) :
              os.remove(SSH_ROOT_KNOWN_HOST)
          # Define IP test cmd
          TEST_CMD = 'ls ' + PTUGEN_PATH
     # Start Send ssh cmd to Target OS IP address
     if(DEBUG_OS_TYPE == os_linux):
          if(background_run == background_run_enable and ip_search_done == 1):
                      os.system( LINUX_BACKGROUND_RUN + 'ssh ' + SSH_IGNORE_HOST_KEY + os_user + '@' + OS_IP +' -t sudo ' + PROGRAM_PATH + ' ' + STRESS_CMD + ' &')
          elif(background_run == background_run_disable and ip_search_done == 1):
               if(LOG_SAVE == 1):
                      os.system('ssh '+ SSH_IGNORE_HOST_KEY + os_user + '@'+ OS_IP + ' -t sudo ' + PROGRAM_PATH + ' ' + STRESS_CMD + ' > ' + SSH_LOG_PATH_LINUX)
               else:
                      os.system('ssh '+ SSH_IGNORE_HOST_KEY + os_user + '@'+ OS_IP + ' -t sudo ' + PROGRAM_PATH + ' ' + STRESS_CMD)
          elif(ip_search_done == 0):         
                      count = 0
                      for count in range(0 , len(ip_list)):
                           rsp = os.system('ssh '+ SSH_IGNORE_HOST_KEY + os_user + '@'+ ip_list[count] + ' -t sudo ' + SSH_CMD_PATH_EMPTY + ' ' + TEST_CMD + ' > ' + SSH_LOG_PATH_LINUX) 
                           if rsp == 0:
                                print ip_list[count], ' is up!'
                                print('Set CentOS Target IP : ' + ip_list[count])
                                ##Save Target CentOS  DHCP IP
                                file = open(OS_IP_LOG, 'w')
                                file.write(ip_list[count])
                                file.close()
                                return SUCCESSFUL
                           else:
                                DEBUG( ip_list[count] + ' is down!')
                                count = count + 1
          else:
               DEBUG('ssh_send_cmd_switch : ERROR!!  Incorrect type of background_run !!')
               return ERROR               
     elif(DEBUG_OS_TYPE == os_win and ip_search_done == 1):
          if(background_run == background_run_enable and ip_search_done == 1):
                      os.system( WIN_BACKGROUND_RUN + WIN_SSH_PATH + SSH_IGNORE_HOST_KEY + os_user + '@' + OS_IP +' -t sudo ' + PROGRAM_PATH + ' ' + STRESS_CMD + ' &')
          elif(background_run == background_run_disable and ip_search_done == 1):
               if(LOG_SAVE == 1):
                      os.system(WIN_SSH_PATH + SSH_IGNORE_HOST_KEY + os_user + '@'+ OS_IP + ' -t sudo ' + PROGRAM_PATH + ' ' + STRESS_CMD + ' > ' + SSH_LOG_PATH_WIN)                 
               else:
                      os.system(WIN_SSH_PATH + SSH_IGNORE_HOST_KEY + os_user + '@'+ OS_IP + ' -t sudo ' + PROGRAM_PATH + ' ' + STRESS_CMD)         
          elif(ip_search_done == 0):         
                      count = 0
                      for count in range(0 , len(ip_list)):
                           rsp = os.system(WIN_SSH_PATH + SSH_IGNORE_HOST_KEY + os_user + '@'+ ip_list[count] + ' -t sudo ' + SSH_CMD_PATH_EMPTY + ' ' + TEST_CMD + ' > ' + SSH_LOG_PATH_LINUX) 
                           if rsp == 0:
                                print ip_list[count], ' is up!'
                                print('Set CentOS Target IP : ' + ip_list[count])
                                ##Save Target CentOS  DHCP IP
                                file = open(OS_IP_LOG, 'w')
                                file.write(ip_list[count])
                                file.close()
                                return SUCCESSFUL
                           else:
                                DEBUG( ip_list[count] + ' is down!')
                                count = count + 1
          else:
               DEBUG('ssh_send_cmd_switch : ERROR!!  Incorrect type of background_run !!')
               return ERROR            
     else:
          return ERROR
          
     return SUCCESSFUL

##Function : Define OS IP auto search process
def ip_search( current_check_ip ):
     ip_search_done = 0
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
               ip_search_done = 1
               return ip_list[0], ip_search_done
          else:
               DEBUG( 'Previous IP ' + ip_list[0] + ' is down! Search New Target IP Again...')
               #delete previous ip log
               os.remove(OS_IP_LOG)
     else:
          DEBUG('previous ip list file not exist, start new search ip process...')

     # Start OS IP re-search process                     
     ip_range = current_check_ip
     for ip_range in range(current_check_ip , end_ip_range ):
          ip_addr  = head_ip_add + str(ip_range)
          rsp = os.system('ping '+ PING_PARAMETER + ip_addr)
          #and then check the response...
          if rsp == 0:
               print ip_addr, ' is up!'
               print('Set Target IP : ' + ip_addr)
               return ip_addr, ip_range , ip_search_done
          else:
               DEBUG( ip_addr + ' is down!')

     print('ERROR!!  Can not find any target IP in netwrok , please check network link and make sure target system boot into OS')
     return ERROR     


     