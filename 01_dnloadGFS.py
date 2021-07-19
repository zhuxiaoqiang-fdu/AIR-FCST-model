#!/usr/bin/python3.6

import time
import wget
import glob as gb

sfile=gb.dn_file_name
url='https://motherlode.ucar.edu/native/grid/NCEP/GFS/Global_onedeg/'+sfile
filename=wget.download(url)
subject = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + 'time ready!!!'
print(subject)






