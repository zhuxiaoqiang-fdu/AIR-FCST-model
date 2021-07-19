#!/public/software/nodes/python361/bin/python3

import datetime
import os
import multiprocessing, signal, time, queue
global os

class MET:
    
    def __init__(self, USA_WF_FILE, USA_FILE_DATE, FCST_TIME, timstr):
        self.USA_WF_FILE = USA_WF_FILE
        self.USA_FILE_DATE = USA_FILE_DATE
        self.pro_tim = FCST_TIME*24+1
        self.FCST_TIME = FCST_TIME
        self.timstr = timstr

    def manual_fct(self, job_queue,result_queue,ymd):
        signal.signal(signal.SIGINT,signal.SIG_IGN)
        while not job_queue.empty():
            try:
                job=job_queue.get(block=False)
                result_queue.put(self.single_wrf( ymd))
            except queue.Empty:
                pass

        
    def run_wgrib2(self):
        os.environ['USA_WF_PATH']=str('./')
        os.environ['USA_WF_FILE']=str(self.USA_WF_FILE)
        os.environ['USA_FILE_DATE']=str(self.USA_FILE_DATE)
        os.environ['USA_FILE_HOUR']=str(self.pro_tim+24)
        val=os.system('wgrib2 $USA_WF_PATH/$USA_WF_FILE -v | grep ":anl:" | wgrib2 -i $USA_WF_PATH/$USA_WF_FILE -small_grib 10:200 0:90   $USA_WF_PATH/$USA_FILE_DATE-$USA_FILE_HOUR-00.grib2')
        for i in range(3,self.pro_tim+24,3):
            keywd=':'+str(i)+'[[:space:]]'+'hour|:'+str(i)+'-..'+'[[:space:]]'+'hour'
            timstp = str(i).zfill(2)
            os.environ['keywd']=str(keywd)
            os.environ['timstp']=str(timstp)
            os.system('wgrib2 $USA_WF_PATH/$USA_WF_FILE -v | egrep $keywd  | wgrib2 -i $USA_WF_PATH/$USA_WF_FILE -small_grib 10:200 0:90  $USA_WF_PATH/$USA_FILE_DATE-$USA_FILE_HOUR-$timstp.grib2')

    
    def run_wps(self):
        global os
        stdate = (datetime.datetime.strptime(self.timstr, "%Y%m%d") + datetime.timedelta(days = -1)).strftime('%Y%m%d')
        edtime = (datetime.datetime.strptime(self.timstr, "%Y%m%d") + datetime.timedelta(days = self.FCST_TIME )).strftime('%Y%m%d')
        os.environ['wps_yy1'] = stdate[0:4]
        os.environ['wps_mm1'] = stdate[4:6]
        os.environ['wps_dd1'] = stdate[6:8]
        os.environ['wps_yy2'] = edtime[0:4]
        os.environ['wps_mm2'] = edtime[4:6]
        os.environ['wps_dd2'] = edtime[6:8]
        os.chdir('./met/run_wps')
        os.system('./wps3.sh ${wps_mm1} ${wps_mm2} ${wps_dd1} ${wps_dd2} ${wps_yy1} ${wps_yy2}')
        os.chdir('../..')

    def run_wrf(self):
        os.chdir('./met/run_wrf')
        YMD = [ (datetime.datetime.strptime(self.timstr, "%Y%m%d") + datetime.timedelta(days = i)).strftime('%Y%m%d') for i in range(self.FCST_TIME) ] 
        
        job_queue=multiprocessing.Queue()
        result_queue=multiprocessing.Queue()
        core_num = self.FCST_TIME
        for i in range(core_num):
            job_queue.put(None)
        workers = []
  
        for i in range(self.FCST_TIME):
            p = multiprocessing.Process(target = self.manual_fct, args = (job_queue, result_queue,YMD[i]))
            p.start()
            workers.append(p)

        try:
            for worker in workers:
                worker.join()
                print(worker)
        except KeyboardInterrupt:
            print('parent WRF received ctrl-c')
            for worker in workers:
                worker.terminate()
                worker.join()
        os.chdir('../..')


    def single_wrf(self, ymd):
        os.environ['wrf_yy'] = ymd[0:4]
        os.environ['wrf_mm'] = ymd[4:6]
        os.environ['wrf_dd'] = ymd[6:8]
        os.system('./wrf_setup -d ${wrf_mm}_${wrf_dd}')
        os.system('./04_0_generate_namelist.sh $wrf_yy $wrf_mm $wrf_dd')
        os.system('./04_1_real.sh $wrf_mm $wrf_dd')
        os.system('./04_2_run_job.sh $wrf_yy $wrf_mm $wrf_dd')
        os.system('./04_3_noqsub.sh $wrf_mm $wrf_dd')


    def run_mcip(self):
        os.chdir('./met/run_mcip/')
        YMD = [ (datetime.datetime.strptime(self.timstr, "%Y%m%d") + datetime.timedelta(days = i)).strftime('%Y%m%d') for i in range(self.FCST_TIME) ]
        for ymd in YMD:
            os.environ['wrf_yy'] = ymd[0:4]
            os.environ['wrf_mm'] = ymd[4:6]
            os.environ['wrf_dd'] = ymd[6:8]
            os.system('./run.china.mcip.d01 $wrf_yy $wrf_mm $wrf_dd')
            os.system('./run.china.mcip.d02 $wrf_yy $wrf_mm $wrf_dd')
            os.system('./run.china.mcip.d03 $wrf_yy $wrf_mm $wrf_dd')

