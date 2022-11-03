

import pyautogui
from handler import handle
from glob import glob
"""
実装タスク
# DatabaseのCSV取得
"""

class ipu_testr(handle):
    def __init__(self):
        super().__init__()
        self.read_default_settings()
        self.read_settings()
        text = "Reading Setting Files has successed"
        self.write_log(text,1)
        text = f"""Setting Contents
[default_settings]
{str(self.default_settings)}
DefaultWaitTime: {self.DefaultWaitTime}
InstallerPath: {self.InstallerPath}
OldInstallerPath: {self.OldInstallerPath}
LogLevel :{self.LogLevel}
[Actions]
{str(self.actions)} 
"""
        self.write_log(text,2)
    
    def exe_actions(self,actions):
        tmp_thread = ""
        for action in actions:
            self.write_log(action,3)
            print(action)
            flag = str(action[0])
            if flag in self.default_settings.keys():
                self.exe_actions(self.default_settings[flag])
            elif flag == "launchSetup":
                tmp_thread = self.launch_Setup()
            elif flag == "oldlaunchSetup":
                tmp_thread = self.old_launch_Setup()
            elif flag == "waitSetup":
                self.wait_Thread(tmp_thread)
            elif flag == "launchIPU":
                tmp_thread = self.launch_IPU()
            elif flag.find("getscreenshot:")==0:
                self.get_screenshot(flag[flag.find(":")+1:])
            elif flag.find("launchfile:")==0:
                self.launch_file_by_mode(flag[flag.find(":")+1:],0)
            elif flag.find("launchfilebythread:")==0:
                self.launch_file_by_mode(flag[flag.find(":")+1:],1)
            elif flag.find("launchfilebyprocess:")==0:
                self.launch_file_by_mode(flag[flag.find(":")+1:],2)
            elif flag.find("launchfilebybat:")==0:
                self.launch_file_by_mode(flag[flag.find(":")+1:],3)
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
                self.active_window(flag[flag.find(":")+1:])
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
                flag = flag[flag.find(":")+1:].split(",")
                pyautogui.doubleClick(int(flag[0]),int(flag[1]))
            elif flag.find("WAIT:")==0:
                pyautogui.sleep(int(flag[flag.find(":")+1:]))
            else:
                self.done_action(action)

    def main(self):
        self.exe_actions(self.actions)

if __name__ == "__main__":
    tester_inst = ipu_testr()
    print("座標設定はVirtualBoxのウィンドウ1920×1200の100％スケール想定で設けています")
    waiting = input(">>")
    tester_inst.main()
    text = "Process Finished"
    tester_inst.write_log(text,1)
    