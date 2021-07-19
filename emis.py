#!/public/software/nodes/python361/bin/python3

import datetime
import os
import multiprocessing, signal, time, queue
import sys

class EMIS:
    
    def __init__(self, FCST_TIME, timstr, flag):
        self.FCST_TIME = FCST_TIME
        self.timstr = timstr
        self.flag = flag

    def manual_fct2(self,job_queue,result_queue,ymd):
        signal.signal(signal.SIGINT,signal.SIG_IGN)
        while not job_queue.empty():
            try:
                job=job_queue.get(block=False)
                result_queue.put(self.single_megan( ymd))
            except queue.Empty:
                pass

    def run_megan(self):
        os.chdir('./emiss/MEAGAN/MEGANv2.10/work/')
        YMD = [ (datetime.datetime.strptime(self.timstr, "%Y%m%d") + datetime.timedelta(days = i)).strftime('%Y%m%d') for i in range(self.FCST_TIME) ]
        job_queue=multiprocessing.Queue()
        result_queue=multiprocessing.Queue()
        core_num = self.FCST_TIME
        for i in range(core_num):
            job_queue.put(None)
        workers = []

        for i in range(self.FCST_TIME):
            p = multiprocessing.Process(target = self.manual_fct2, args = (job_queue, result_queue, YMD[i], ))
            p.start()
            workers.append(p)
       
        try:
            for worker in workers:
                worker.join()
                print(worker)
        except KeyboardInterrupt:
            print('parent MEGAN received ctrl-c')
            for worker in workers:
                worker.terminate()
                worker.join()
        os.chdir('../../../..')

    def single_megan(self, ymd):
        os.environ['wrf_yy'] = ymd[0:4]
        os.environ['wrf_mm'] = str(ymd[5:6]).zfill(2)
        os.environ['wrf_dd'] = str(ymd[6:8]).zfill(2)
        os.system('./12_0_run.met2mgn.v210_d01.csh $wrf_yy $wrf_mm $wrf_dd 01 36km')
        os.system('./12_0_run.met2mgn.v210_d02.csh $wrf_yy $wrf_mm $wrf_dd 01 12km')
        os.system('./12_0_run.met2mgn.v210_d03.csh $wrf_yy $wrf_mm $wrf_dd 01 4km')
        os.system('./12_1_run.emproc.v210_d01.csh $wrf_yy $wrf_mm $wrf_dd 01 36km')
        os.system('./12_1_run.emproc.v210_d02.csh $wrf_yy $wrf_mm $wrf_dd 01 12km')
        os.system('./12_1_run.emproc.v210_d03.csh $wrf_yy $wrf_mm $wrf_dd 01 4km')
        os.system('./12_2_run.mgn2mech.v210_d01.csh  $wrf_yy $wrf_mm $wrf_dd 01 36km')
        os.system('./12_2_run.mgn2mech.v210_d02.csh  $wrf_yy $wrf_mm $wrf_dd 01 12km')
        os.system('./12_2_run.mgn2mech.v210_d03.csh  $wrf_yy $wrf_mm $wrf_dd 01 4km')


    def pro_emiss(self):
        YMD = [ (datetime.datetime.strptime(self.timstr, "%Y%m%d") + datetime.timedelta(days = i)).strftime('%Y%m%d') for i in range(self.FCST_TIME) ]

        if self.flag != 'SO_sector':
            os.chdir('./emiss/combine_base')
            for ymd in YMD:
                os.environ['wrf_yy'] = ymd[0:4]
                os.environ['wrf_mm'] = ymd[4:6]
                os.environ['wrf_dd'] = ymd[6:8]
                os.system('./13_0.aero6.meic.combine_all_d01.sh $wrf_yy $wrf_mm $wrf_dd')
                os.system('./13_0.aero6.meic.combine_all_d02.sh $wrf_yy $wrf_mm $wrf_dd')
                os.system('./13_0.aero6.meic.combine_all_d03.sh $wrf_yy $wrf_mm $wrf_dd')
            os.chdir('../../') 
        else:
            os.chdir('./emiss/combine_SO_sector/')
            for ymd in YMD:
                os.environ['wrf_yy'] = ymd[0:4]
                os.environ['wrf_mm'] = ymd[4:6]
                os.environ['wrf_dd'] = ymd[6:8]
                os.system('./13_0.aero6.meic.combine_all_d01.sh $wrf_yy $wrf_mm $wrf_dd')
                os.system('./13_0.aero6.meic.combine_all_d02.sh $wrf_yy $wrf_mm $wrf_dd')
                os.system('./13_0.aero6.meic.combine_all_d03.sh $wrf_yy $wrf_mm $wrf_dd')
            os.chdir('../..')



        if self.flag == 'SO_region':
            os.chdir('./emiss/combine_SO_region/')                        
            for ymd in YMD:
                os.environ['wrf_yy'] = ymd[0:4]
                os.environ['wrf_mm'] = ymd[4:6]
                os.environ['wrf_dd'] = ymd[6:8]
                os.system('./13_0.aero6.meic.combine_all_d01.sh $wrf_yy $wrf_mm $wrf_dd')
                os.system('./13_0.aero6.meic.combine_all_d02.sh $wrf_yy $wrf_mm $wrf_dd')
                os.system('./13_0.aero6.meic.combine_all_d03.sh $wrf_yy $wrf_mm $wrf_dd')
            os.chdir('../../')
 







