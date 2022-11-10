
import os
import win32gui
from handler.filehandler import filehandler
from glob import glob
import subprocess
import threading
from multiprocessing import Process
import psutil
import pyautogui

class handle(filehandler):
    def __init__(self):
        super().__init__()
    
    def check_env_path(self,filepath):
        paths = os.environ["PATH"].split(";")
        for path in paths:
            if(path[-1]!="\\"):
                path += "\\"
            tmp_path = path + filepath
            if os.path.exists(tmp_path):
                return tmp_path
        text = f"File does not exist:{str(filepath)}"
        self.write_log(text,1)
        raise Exception
    
    def launch_file(self,filepath,*args):
        if os.path.exists(filepath)==False:
            filepath = self.check_env_path(filepath)
        try:
            args_text = str(" ".join(*args))
        except:
            args_text = ""
        text = f"launched:{filepath} {args_text}"
        self.write_log(text,2)
        try:
            file_dir = os.path.dirname(filepath)
            os.chdir(file_dir)
            subprocess.Popen([filepath,*args])
            os.chdir(self.config.currentdirectory)
        except Exception as e:
            text = f"Failed:{filepath}"
            self.write_error(text,e,1)
            raise Exception
        text = f"closed:{filepath}"
        self.write_log(text,2)
    
    def launch_file_by_bat(self,filepath,*args):
        if os.path.exists(filepath)==False:
            filepath = self.check_env_path(filepath)
        try:
            args_text = str(" ".join(*args))
        except:
            args_text = ""
        text = f"launched:{filepath} {args_text}"
        self.write_log(text,2)
        try:
            with open("temp_exec_bat_file.bat","w") as f:
                tmp_key = '"' + filepath + '" ' + args_text
                f.write(tmp_key)
            subprocess.Popen(["temp_exec_bat_file.bat"],)
        except Exception as e:
            text = f"Failed:{filepath}"
            self.write_error(text,e,1)
            raise Exception
        text = f"closed:{filepath}"
        self.write_log(text,2)
    
    
    def wait_Thread(self,):
        try:
            thread_list = threading.enumerate()
            thread_list.remove(threading.main_thread())
            for thread in thread_list:
                thread.join()
        except Exception as e:
            text = f"Failed to join the thread"
            self.write_error(text,e,1)
            raise Exception
 
    def done_action(self,action_list):
        if len(action_list)==2 or len(action_list)==3:
            try:
                for num,al in enumerate(action_list):
                    action_list[num] = int(al)
            except:
                pass
        text = f"done action: {str(action_list)}"
        self.write_log(text,3)
        if(type(action_list[0]) is str):
            for action in action_list:
                try:
                    pyautogui.press(action)
                    pyautogui.sleep(self.DefaultWaitTime)
                except Exception as e:
                    text = f"Failed to done the action:{str(action)}"
                    self.write_error(text,e,1)
                    raise Exception
        else:
            try:
                a = action_list[0]
                b = action_list[1]
                if len(action_list)==2:
                    c = self.DefaultWaitTime
                else:
                    c = action_list[2]
                # pyautogui.moveTo(a, b)
                pyautogui.click(a,b)
                pyautogui.sleep(c)
            except Exception as e:
                text = f"Failed to done the action:{str(action_list)}"
                self.write_error(text,e,1)
                raise Exception
    
    def active_window(self,names):
        window_names = names.split(",")
        for window_name in window_names:
            text = f"Activate the windows:{str(window_name)}"
            self.write_log(text,2)
            try:
                target_app = win32gui.FindWindow(None,window_name)
                pyautogui.sleep(self.DefaultWaitTime)
                win32gui.SetForegroundWindow(target_app)
                return
            except Exception as e:
                text = f"Failed to active the window:{window_name}"
                self.write_error(text,e,1)
        text = f"Failed to active all windows:{window_names}"
        self.write_log(text,1)
        raise Exception
    
    def process_kill(self,target_name):
        text = f"Kill the process:{target_name}"
        self.write_log(text,2)
        for proc in psutil.process_iter():
            try:
                try:
                    proc_name = proc.exe()
                    if (proc_name.find(target_name)==-1):
                        continue
                    print("プロセスID:" + str(proc.pid))
                    print("実行モジュール：" + proc.exe())
                    # print("コマンドライン:" + str(proc.cmdline()))
                    # print("カレントディレクトリ:" + proc.cwd())
                    p = psutil.Process(proc.pid)
                    p.terminate()
                except:
                    continue
            except Exception as e:
                text = f"Failed to kill the process:{target_name}"
                self.write_error(text,e,1)
                raise Exception
    
    def launch_file_by_mode(self,filepath,mode=0,*args):
        try:
            args_text = " ".join(*args)
        except:
            args_text = ""
        if os.path.exists(filepath)==False:
            filepath = self.check_env_path(filepath)
        if mode == 0:
            self.launch_file(filepath,*args)
        elif mode == 1:
            filethread = threading.Thread(target=self.launch_file ,args=(filepath,*args,))
            filethread.start()
            pyautogui.sleep(self.DefaultWaitTime)
            return filethread
        elif mode == 2:
            fileprocess = Process(target=self.launch_file ,args=(filepath,*args,))
            fileprocess.start()
            pyautogui.sleep(self.DefaultWaitTime)
            return fileprocess
        elif mode == 3:
            fileprocess = Process(target=self.launch_file_by_bat ,args=(filepath,*args,))
            fileprocess.start()
            pyautogui.sleep(self.DefaultWaitTime)
            return fileprocess
    
    def wait_process(self,processname,mode=0):
        if mode == 0:
            text = f"wait to pass away the process: {processname}"
        elif mode == 1:
            text = f"wait to wake up the process: {processname}"
        self.write_log(text,2)
        rest_loop = 120
        while rest_loop>0:
            try:
                rest_loop -= 1
                pyautogui.sleep(5)
                process_list = []
                for p in psutil.process_iter(attrs=('name', 'pid', 'cmdline')):
                    process_list.append(p.info['name'])
                if mode == 0:
                    if (processname not in process_list):
                        return
                elif mode == 1:
                    if (processname in process_list):
                        return
            except Exception as e:
                text = f"Failed to wait the process:{processname}"
                self.write_error(text,e,1)
                raise Exception
        text = f"Failed to wait the process:{processname}"
        self.write_log(text,1)
        raise Exception
    
    def wait_file_existance(self,filepath,mode=0):
        if mode == 0:
            text = f"wait to pass away the file: {filepath}"
        elif mode == 1:
            text = f"wait to create the file: {filepath}"
        self.write_log(text,2)
        rest_loop = 120
        while rest_loop>0:
            try:
                rest_loop -= 1
                pyautogui.sleep(5)
                if mode == 0:
                    if (os.path.exists(filepath) == False):
                        return
                elif mode == 1:
                    if (os.path.exists(filepath) == True):
                        return
            except Exception as e:
                text = f"Failed to wait the file:{filepath}"
                self.write_error(text,e,1)
                raise Exception
        text = f"Failed to wait the file:{filepath}"
        self.write_log(text,1)
        raise Exception
    
    def shutdown(self,mode=0):
        __not_kill_trget = [
            "python.exe","cmd.exe",
            "BrHostSvr.exe","TextInputHost.exe",
            "DesktopExtension.exe","HP.MyHP.exe",
            'Registry',"lunch_attend"
        ]
        __not_kill_id = [4]
        for proc in psutil.process_iter():
            try:
                if proc.exe().find(":\Windows\System32") >= 0:
                    continue
                if int(proc.pid) in __not_kill_id:
                    continue
                nkt_flag = [_ for _ in __not_kill_trget if (proc.exe()).lower().find(_.lower()) >= 0]
                if len(nkt_flag) > 0:
                    # not_kill_id.append(proc.pid)
                    continue
                print("プロセスID:" + str(proc.pid))
                print("実行モジュール：" + proc.exe())
                print("コマンドライン:" + str(proc.cmdline()))
                print("カレントディレクトリ:" + proc.cwd())
                p = psutil.Process(proc.pid)
                # pid_list=[pc.pid for pc in p.children(recursive=True)] 
                # for pid in pid_list:
                #     try:
                #         if_flag = [i for i in not_kill_id if i == pid]
                #         if len(if_flag) > 0:
                #             continue
                #         psutil.Process(pid).terminate ()
                #         print("terminate 子プロセス　{}" .format(pid))
                #     except:
                #         pass
                # 親のterminate
                p.terminate ()
            except:
                pass
        if mode == 0:
            os.system("shutdown /s /t 0")            
        else:
            os.system("shutdown /r /t 0")
        

    
    def chk_number_of_file(self,filepath):
        text = f"check the number of the files under: {filepath}"
        self.write_log(text,2)
        rest_loop = 120
        number_of_files = len(glob(filepath))
        print(f"Current_file_number:{number_of_files}")
        while rest_loop>0:
            try:
                rest_loop -= 1
                pyautogui.sleep(5)
                tmp_count = len(glob(filepath))
                print(f"Current_file_number:{tmp_count}")
                if number_of_files != tmp_count:
                    return
            except Exception as e:
                text = f"Failed to wait the file:{filepath}"
                self.write_error(text,e,1)
                raise Exception
        text = f"Failed to wait the file:{filepath}"
        self.write_log(text,1)
        raise Exception
    
    def get_screenshot(self,filename):
        try:
            file_path = fr"{self.config.work_dir}\{filename}"
            if file_path[-4:]!=".png" or file_path[-4:]!=".jpg" or file_path[-5:]==".jpeg":
                file_path += ".png"
            text = f"Save the screenshot: {file_path}"
            self.write_log(text,3)
            screen_shot = pyautogui.screenshot() 
            screen_shot.save(file_path)
        except Exception as e:
                text = f"Failed to save the screenshot: {file_path}"
                self.write_error(text,e,1)
                raise Exception
    
    def send_keys(self,keywords):
        text = f"Send the keywords: {keywords}"
        self.write_log(text,3)
        try:
            for i in range(len(keywords)):
                pyautogui.press(keywords[i])
        except Exception as e:
            text = f"Failed to send the keywords: {keywords}"
            self.write_error(text,e,1)
            raise Exception
    