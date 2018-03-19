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
## import other function define
from file_path_handle import *
from nm_network_handle import *
from os_parameters_define import *
from utility_function import *
from nm_ipmi_raw_to_str import *
from error_messages_define import *
from config import *

	 
def main(argv):
   print 'usage : peci_proxy.py [PECI_CLIENT_ADDR : CPU0 = 0x30 , CPU1=0x31, CPU2= 0x32, CPU3=0x33... ] '
   print '                       [peci_interface : Fallback =0, Inbend PECI = 1, PECI wire = 2] '
   print '                       [write_len : ] '
   print '                       [read_len : ] '
   print '                       [raw_peci : ] '
   print 'example GET_TEMP() : > python peci_proxy.py 0x30 0 1 2 1  '
   print 'example RdPkgConfig(): Package Thermal Status MSR 0x1B1 : > python peci_proxy.py 0x30 0 5 5 0xa1 0 0x14 0 0'

   PECI_CLIENT_ADDR = int(sys.argv[1], 16)
   peci_interface = int(sys.argv[2], 16)
   write_len = int(sys.argv[3], 16)
   read_len = int(sys.argv[4], 16)
   raw_peci = []
   loop = 0
   for loop in range(0 , (len(sys.argv)- 5)):
        raw_peci.append('0x'+ format(int(sys.argv[5+loop], 16),'02x'))
   DEBUG(raw_peci)  
   ipmi = aardvark_ipmi_init()
   # Prepare GetTemp PECI raw data aray
   while (1):
        # Send GetTemp via ME RAW PECI proxy: Write length = 1 byte , Read_Length = 2 bytes
        resp = send_raw_peci_py(ipmi , PECI_CLIENT_ADDR, peci_interface, write_len , read_len , raw_peci )
        time.sleep(0.5)
        
   print('Loop exit ~ Bye!')           
	 
## Below is __Main__
if __name__ == "__main__":
     main(sys.argv[1:])


