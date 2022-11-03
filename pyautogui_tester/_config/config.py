
import os
from datetime import datetime as dt

class config:
    todate = dt.now().strftime('%Y%m%d')
    def __init__(
        self,
        data_dir=fr"{os.getcwd()}\data",
        work_dir=fr"{os.getcwd()}\{todate}",
        log_dir=fr"{os.getcwd()}\log",
    ):
        self.set_data_dir(data_dir)
        self.set_work_dir(work_dir)
        self.set_log_dir(log_dir)
        self.currentdirectory = os.getcwd()
    
    def set_data_dir(self,data_dir):
        os.makedirs(data_dir,exist_ok=True)
        self.data_dir = data_dir
    
    def get_data_dir(self):
        return self.data_dir
    
    def set_work_dir(self,work_dir):
        os.makedirs(work_dir,exist_ok=True)
        self.work_dir = work_dir
    
    def get_work_dir(self):
        return self.work_dir
    
    def set_log_dir(self,log_dir):
        os.makedirs(log_dir,exist_ok=True)
        self.log_dir = log_dir
    
    def get_log_dir(self):
        return self.log_dir
    
    def get_time_ymdhms(self):
        return dt.now().strftime('%Y/%m/%d %H:%M:%S')
    
    def get_time_ymd(self):
        return dt.now().strftime('%Y/%m/%d')
    