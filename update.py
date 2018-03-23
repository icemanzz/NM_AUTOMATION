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



def update_nm_tests():
     os.system('git reset --hard')
     os.system('git clean -fd')
     os.system('git pull')
