#!/public/software/nodes/python361/bin/python3

import os
global os

class UTIL:

    def __init__(self, FCST_TIME, timstr, flag):
        self.FCST_TIME = FCST_TIME
        self.timstr = timstr
        self.flag = flag
    
    def move_file(self):
        global os
        os.environ['wrf_md'] = self.timstr
        os.environ['flag'] = self.flag
        os.system('mkdir ./lost_found/$wrf_md/CMAQ')
        os.syetem('mkdir ./lost_found/$wrf_md/MET')
        os.system('mkdir ./lost_found/$wrf_md/EMIS')
        os.system('mkdir ./lost_found/$wrf_md/POST')
        os.system('mv GFS_Global* ./lost_found/$wrf_md/MET')
        os.system('rm *.grib2')
        YMD = [ (datetime.datetime.strptime(self.timstr, "%Y%m%d") + datetime.timedelta(days = i)).strftime('%Y%m%d') for i in range(self.FCST_TIME) ]
        for ymd in YMD:
            os.environ['wrf_yy'] = ymd[0:4]
            os.environ['wrf_mm'] = ymd[4:6]  
            os.environ['wrf_dd'] = ymd[6:8]
            os.system('rm ./met/run_wps/output/*')
            os.system('rm -rf ./met/run_wrf/${wrf_mm}${wrf_dd}')
            os.system('mv ./met/run_mcip/output/* ./lost_found/$wrf_md/MET/'
            os.system('rm -rf ./emiss/MEAGAN/MEGANv2.10/Input/MGNMET/*')
            os.system('rm -rf ./emiss/MEAGAN/MEGANv2.10/Input/PAR/*')
            os.system('rm -rf ./emiss/MEAGAN/MEGANv2.10/Output/*')
            os.system('mv ./emiss/combine_${flag}/output_d0* ./lost_found/$wrf_md/EMIS/')
            os.system('rm -rf ./cmaq/run_bc_${flag}/output_d0*')
            os.system('mv ./cmaq/run_cmaq_${flag}/output_d* ./lost_found/$wrf_md/CMAQ/')
            os.system('rm -rf ./post_cmaq/combine/output*')
            os.system('rm -rf ./post_cmaq/extract/output*')
            os.system('rm ./post_cmaq/plot/region/*ps')
            os.system('rm ./post_cmaq/plot/region/*png')
            os.system('rm ./post_cmaq/plot/region/*gif')
            os.system('rm ./post_cmaq/plot/ts/out_ready/*')
            os.system('rm ./post_cmaq/plot/ts/station.cmaq.ts.O3.*')

















