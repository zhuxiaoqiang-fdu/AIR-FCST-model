#!/public/software/nodes/python361/bin/python3

import datetime
import os
import pandas as pd
import numpy 
import csv
import matplotlib.pyplot as plt
import imageio
import time
import datetime
from PIL import Image

class POST_CMAQ:
    
    def __init__(self, FCST_TIME, timstr, flag):
        self.FCST_TIME = FCST_TIME
        self.timstr = timstr
        self.flag = flag

    def combine(self):
        stdate = (datetime.datetime.strptime(self.timstr, "%Y%m%d") + datetime.timedelta(days = 1)).strftime('%Y%m%d')
        eddate = (datetime.datetime.strptime(self.timstr, "%Y%m%d") + datetime.timedelta(days = FCST_TIME)).strftime('%Y%m%d')        
        os.chdir('./post_cmaq/combine')
        os.environ['stdate_com'] = stdate
        os.environ['eddate_com'] = eddate
        os.environ['flag'] = self.flag
        os.system('./combine_china.FCST_${flag}.sh $stdate_com $eddate_com')

    def extract(self):
        stdate = self.timstr
        stdate1 = (datetime.datetime.strptime(self.timstr, "%Y%m%d") + datetime.timedelta(days = 1)).strftime('%Y%m%d')
        eddate = (datetime.datetime.strptime(self.timstr, "%Y%m%d") + datetime.timedelta(days = FCST_TIME-1)).strftime('%Y%m%d')
        os.chdir('./post_cmaq/extract')
        os.environ['stdate_ext'] = stdate
        os.environ['eddate_ext'] = eddate
        os.environ['stdate_ext1'] = stdate1
        os.system('./china.ts_FCST_${flag}.sh $stdate_ext $eddate_ext $stdate_ext1')
        
    def plot_region(self):
        YMD = [ (datetime.datetime.strptime(self.timstr, "%Y%m%d") + datetime.timedelta(days = i)).strftime('%Y%m%d') for i in range(self.FCST_TIME) ]    
        os.chdir('./post_cmaq/plot/region')
        box1 = (0,300,2000,1700)
        if self.flag == 'base':
            spec_list = ['O3']
        elif self.flag == 'SO_region':
            spec_list = ['O3', 'O3_X1', 'O3_X2', 'O3_X2', 'O3_X3', 'O3_X4', 'O3_X5','O3_X6', 'O3_X7', 'O3_X8']
        elif self.flag == 'SO_sector':
            spec_list = ['O3', 'O3_X1', 'O3_X2', 'O3_X2', 'O3_X3', 'O3_X4', 'O3_X5','O3_X6', 'O3_BG']
        ddmax_list = []
        for spec in spec_list:
            ext_dir = '../../extract/output_' + self.flag
            ext_tot_file = ext_dir + '/station.china.FCST.36km.'+spec+'.matrix.'+spec 
            matx_dat=pd.read_csv(ext_tot_file,header=None,delim_whitespace=True)
            dd=matx_dat.quantile([0.25,0.5,0.95])
            ddmax=(dd.loc[0.95,:]).max()
            ddmax_rd=round(ddmax/10)*10
            ddmax_rd = min(max(ddmax_rd, 10), 120)
            ddmax_list.append(str(ddmax_rd))

        if self.flag == 'base':
            os.environ['ddmax'] = ddmax_list[0]
        else:
            os.environ['tot'] = ddmax_list[0]
            os.environ['X1'] = ddmax_list[1]
            os.environ['X2'] = ddmax_list[2]
            os.environ['X3'] = ddmax_list[3]
            os.environ['X4'] = ddmax_list[4]
            os.environ['X5'] = ddmax_list[5]
            os.environ['X6'] = ddmax_list[6]
        if self.flag == 'SO_sector':
            os.environ['BG'] = ddmax_list[7]

        elif self.flag == 'SO_region':
            os.environ['X7'] == ddmax_list[7]
            os.environ['X8'] == ddmax_list[8]

        for i in range(1, self.FCST_TIME*24 + 1):
            istr = str(i).zfill(3)
            tim = (i-1)%24
            dim = (i-1)//24
            tim_str = str(tim).zfill(2)
            ddt_tim = tim_str + ':00:00'
            os.environ['tstp']=istr
            os.environ['ddte']=str(di[dim])
            os.environ['ddt_tim']=ddt_tim

            if self.flag == 'base':
                os.system('./china.36km.FCST_base.O3.gnuplot.sh $ddmax $tstp $ddte $ddt_tim')
            elif self.flag == 'SO_sector':
                os.system('china.36km.FCST_SO_sector.O3.gnuplot.sh $tstp $tot $BG $X1 $X2 $X3 $X4 $X5 $X6 $ddte $ddt_tim')
            elif self.flag == 'SO_region':
                os.system('./china.36km.FCST_SO_region.O3.gnuplot.sh $tstp $tot $X1 $X2 $X3 $X4 $X5 $X6 $X7 $X8 $ddte $ddt_tim')
        imagines = []
        ednm = 'O3.png'        
        gfnm=spec+'.gif'
        filenames=sorted((fn for fn in os.listdir('.') if fn.endswith(ednm)))
        for filename in filenames:
            img=Image.open(filename)
            image1=img.crop(box1)
            image1.save(filename)
            imagines.append(imageio.imread(filename))
        imageio.mimsave(gfnm,imagines,duration=1)
        os.chdir('../../..')


    def plot_ts(self):
        os.chdir('./post_cmaq/plot/ts')
        stdate = (datetime.datetime.strptime(self.timstr, "%Y%m%d") + datetime.timedelta(days = 1)).strftime('%Y%m%d')
        eddate = (datetime.datetime.strptime(self.timstr, "%Y%m%d") + datetime.timedelta(days = FCST_TIME-1)).strftime('%Y%m%d')
        staf = pd.read_csv('../../extract/taian.xy.txt',header=None,delim_whitespace=True,usecols = [0])
        ext_dir = '../../extract/output_'+self.flag
        city_list = []
        ddmax_list = []
        for i in range(len(staf[0])):
            ext_sta_file = ext_dir + '/station.china.FCST.36km.O3.ts.' + staf[0][i]
            ext_dat = pd.read_csv(ext_sta_file,header=None,delim_whitespace=True)
            ddmax=(ext_dat[1]).max()
            ddmax_rd=round(ddmax*1.4/10)*10
            city_list.append(ext_dat[0][i])
            ddmax_list.append(ddmax_rd)
            
        os.environ['stdate'] = stdate
        os.environ['eddate'] = eddate
        os.environ['flag'] = self.flag
        os.environ['max1'] = ddmax_list[0]
        os.environ['max2'] = ddmax_list[1]
        os.environ['max3'] = ddmax_list[2]
        os.system('./ts.FCST.gnuplot.sh $flag $stdate $eddate $max1 $max2 max3')
        os.chdir('../../../')




