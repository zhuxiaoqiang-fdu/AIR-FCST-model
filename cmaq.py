#!/public/software/nodes/python361/bin/python3

import os

class CMAQ:
    
    def __init__(self, FCST_TIME, timstr, flag, dom):
        self.FCST_TIME = FCST_TIME
        self.timstr = timstr
        self.flag = flag
        self.dom = dom

    def run_cmaq(self):
        os.environ['wrf_yy'] = self.timstr[0:4]
        os.environ['wrf_mm'] = self.timstr[4:6]
        os.environ['wrf_dd'] = self.timstr[6:8]
        os.environ['wrf_ndays'] = str(self.FCST_TIME)
        os.environ['sdom'] = self.dom
        if self.flag == 'base':
            os.chdir('./cmaq/run_cmaq_base')
            os.system('./21_0_36km_china_${sdom}.sh $wrf_yy $wrf_mm $wrf_dd $wrf_ndays')
        elif self.flag == 'SO_sector':
            os.chdir('./cmaq/run_cmaq_SO_sector')
            os.system('./21_0_36km_china_${sdom}.sh $wrf_yy $wrf_mm $wrf_dd $wrf_ndays')
        elif self.flag == 'SO_region':
            os.chdir('./cmaq/run_cmaq_SO_region')
            os.system('./21_0_36km_china_${sdom}.sh $wrf_yy $wrf_mm $wrf_dd $wrf_ndays')
        os.chdir('../../')

    def run_bc(self):
        os.environ['wrf_yy'] = self.timstr[0:4]
        os.environ['wrf_mm'] = self.timstr[4:6]
        os.environ['wrf_dd'] = self.timstr[6:8]
        os.environ['wrf_ndays'] = str(self.FCST_TIME)
        os.environ['sdom'] = self.dom
        if self.flag == 'base':
            os.chdir('./cmaq/run_bc_base')
            os.system('./run.12km_${sdom}.bcon  $wrf_yy $wrf_mm $wrf_dd $wrf_ndays')
        elif self.flag == 'SO_sector':
            os.chdir('./cmaq/run_bc_SO_sector')
            os.system('./run.12km_${sdom}.bcon  $wrf_yy $wrf_mm $wrf_dd $wrf_ndays')
        elif self.flag == 'SO_region':
            os.chdir('./cmaq/run_bc_SO_region')
            os.system('./run.12km_${sdom}.bcon  $wrf_yy $wrf_mm $wrf_dd $wrf_ndays')
        os.chdir('../..')












