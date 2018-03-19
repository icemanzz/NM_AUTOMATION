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
   print 'Reading Power Domain is ', str(sys.argv[1])
   print ('Output file is '+ str(sys.argv))
   domain = int(sys.argv[1])
   ipmi = aardvark_ipmi_init()
   while (1):
        # Read Platform Power via 0xC8h cmd
        power_average_stress = read_power_py(ipmi, global_power_mode , domain , AC_power_side, 0)
        print('Average power reading = %d watts' %power_average_stress)
        time.sleep(0.5)
        
   print('Loop exit ~ Bye!')           
	 
## Below is __Main__
if __name__ == "__main__":
     main(sys.argv[1:])


