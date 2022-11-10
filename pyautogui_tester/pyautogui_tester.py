

import pyautogui
from handler import handle
from glob import glob

class pyautogui_tester(handle):
    def __init__(self):
        super().__init__()
        self.read_settings()
        self.read_default_settings()
        text = "Reading Setting Files has successed"
        self.write_log(text,1)
        text = f"""Setting Contents
[default_settings]
{str(self.default_settings)}
[Actions]
{str(self.actions)} 
[Settings]
{str(self.settings)}
"""
        self.write_log(text,2)
    
    def exe_actions(self,actions:list):
        tmp_thread = ""
        for action in actions:
            self.write_log(action,3)
            print(action)
            flag = str(action[0])
            if flag in self.default_settings.keys():
                self.exe_actions(self.default_settings[flag])
            elif flag == "waitThread":
                self.wait_Thread()
            elif flag.find("getscreenshot:")==0:
                self.get_screenshot(flag[flag.find(":")+1:])
            elif flag.find("launchfile")==0:
                if flag.find("launchfile:")==0:
                    mode = 0
                elif flag.find("launchfilebythread:")==0:
                    mode = 1
                elif flag.find("launchfilebyprocess:")==0:
                    mode = 2
                elif flag.find("launchfilebybat:")==0:
                    mode = 3
                else:
                    mode = -1
                print(mode)
                if type(action) == list:
                    del action[0]
                    self.launch_file_by_mode(flag[flag.find(":")+1:],mode,*action)
                else:
                    self.launch_file_by_mode(flag[flag.find(":")+1:],mode)            
            elif flag.find("chk_number_of_file:")==0:
                self.chk_number_of_file(flag[flag.find(":")+1:])
            elif flag.find("waitprocesskill:")==0:
                self.wait_process(flag[flag.find(":")+1:],0)
            elif flag.find("waitprocessstart:")==0:
                self.wait_process(flag[flag.find(":")+1:],1)
            elif flag.find("waitfilekill:")==0:
                self.wait_file_existance(flag[flag.find(":")+1:],0)
            elif flag.find("waitfilecreate:")==0:
                self.wait_file_existance(flag[flag.find(":")+1:],1)
            elif flag.find("activewindow:")==0:
                tmp_line = ",".join(action)
                tmp_line = tmp_line[flag.find(":")+1:]
                self.active_window(tmp_line)
            elif flag.find("processkill:")==0:
                self.process_kill(flag[flag.find(":")+1:])
            elif flag.find("INPUT:")==0:
                self.send_keys(flag[flag.find(":")+1:])
            elif flag.find("KEYDOWN:")==0:
                pyautogui.keyDown(flag[flag.find(":")+1:])
            elif flag.find("KEYUP:")==0:
                pyautogui.keyUp(flag[flag.find(":")+1:])
            elif flag.find("HOTKEY:")==0:
                pyautogui.hotkey(flag[flag.find(":")+1:],action[1])
            elif flag.find("DOUBLECLICK:")==0:
                pyautogui.doubleClick(int(flag[flag.find(":")+1:]),int(action[1]))
            elif flag.find("WAIT:")==0:
                pyautogui.sleep(int(flag[flag.find(":")+1:]))
            elif flag==("SHUTDOWN"):
                self.shutdown()
            elif flag==("RESTART"):
                self.shutdown(mode=1)
            elif flag==("END"):
                exit()
            else:
                self.done_action(action)

    def main(self):
        self.exe_actions(self.actions)

if __name__ == "__main__":
    tester_inst = pyautogui_tester()
    print("座標設定はVirtualBoxのウィンドウ1920×1200の100％スケール想定で設けています")
    waiting = input(">>")
    tester_inst.main()
    text = "Process Finished"
    tester_inst.write_log(text,1)
    