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
   print 'usage : pmbus_proxy.py [msg_type : 1 =read_byte, 2 = write_byte, 3 = read_word, 4 = write_word , 5 = block_read , 6 = block_write] '
   print '                       [sensor_bus : 0 =host_smbus, 1 = sml0, 2 = sml1, 3 = sml2 , 4 = sml3 , 5= sml4] '
   print '                       [target_addr : 0xb0] '
   print '                       [read_len : 1 = get pmbus version, 2 = read_pin/pout, 7 = read_ein/eout] '
   print '                       [cmd : get pmbus version = 0x98 , 0x86 , 0x97] '
   print 'example read_pin : > python pmbus_proxy.py 3 2 0xb0 2 0x97  '
   print 'example read_ein : > python pmbus_proxy.py 5 2 0xb0 7 0x86  '
   print 'example get_pm_ver : > python pmbus_proxy.py 1 2 0xb0 1 0x98  '
   print 'SMbus Number is ', str(sys.argv[1])
   print ('Output file is '+ str(sys.argv))
   msg_type = int(sys.argv[1], 16)
   sensor_bus = int(sys.argv[2], 16)
   target_addr = int(sys.argv[3], 16)
   write_len = 1
   read_len = int(sys.argv[4], 16)
   cmd = int(sys.argv[5], 16)  
   ipmi = aardvark_ipmi_init()
   while (1):
        # Send PMbus Proxy cmd
        send_raw_pmbus_cmd_extend_py(ipmi, msg_type , d9h_pec_report, d9h_pec_en, sensor_bus , target_addr , 0 , 0 , 0 , d9h_trans_potocol_pmbus , write_len , read_len , cmd)
        #print('Average power reading = %d watts' %power_average_stress)
        time.sleep(0.5)
        
   print('Loop exit ~ Bye!')           
	 
## Below is __Main__
if __name__ == "__main__":
     main(sys.argv[1:])

