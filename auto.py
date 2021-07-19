#!/public/software/nodes/python361/bin/python3
'''
@Program: AIR_FCST_auto System 
@Author: Shengqiang Zhu
@Copyright by ACES@FDU
@Date: June 14, 2021
'''


from met import *
from emis import *
from cmaq import *
from post_cmaq import *
from util import *
import os

def main():

################ Control Information####################################
    USA_WF_FILE = 'GFS_Global_0p5deg_20210614_0000.grib2'
    USA_FILE_DATE = '20210502'
    FCST_TIME = 7
    flag = 'SO_region'      # select: 'base', 'SO_sector', 'SO_region'
#######################################################################

    timstr = (datetime.datetime.strptime(USA_FILE_DATE, "%Y%m%d") + datetime.timedelta(days = 1)).strftime('%Y%m%d') # timstr = USA_FILE_DATE + 1
    basedir = '/data2/sqzhu/zhusq/AIR_FCST_auto/'
    os.chdir(basedir)


    # MET Module
    met1 = MET(USA_WF_FILE, USA_FILE_DATE, FCST_TIME, timstr)
    met1.run_wgrib2()
    met1.run_wps()
    met1.run_wrf()
    met1.run_mcip()

    # EMISSION Module
    emis1 = EMIS(FCST_TIME, timstr, flag)
    emis1.run_megan()
    emis1.pro_emiss()

    # CMAQ Module
    # Init the CMAQ class
    cmaq1 = CMAQ(FCST_TIME, timstr, flag, 'd01')
    cmaq2 = CMAQ(FCST_TIME, timstr, flag, 'd02')
    cmaq3 = CMAQ(FCST_TIME, timstr, flag, 'd03')
    # Process the CMAQ class
    cmaq1.run_cmaq()
    cmaq2.run_bc()
    cmaq2.run_cmaq()
    cmaq3.run_bc()
    cmaq3.run_cmaq()

    # POST_CMAQ Module
    post_cmaq1 = POST_CMAQ(FCST_TIME, timstr, flag)
    post_cmaq1.combine()
    post_cmaq1.extract()
    post_cmaq1.plot_region()
    post_cmaq1.plot_ts()    


    # Save files
    util1 = UTIL(FCST_TIME, timstr, flag)
    util1.move_file()

if __name__=='__main__':
    main()










