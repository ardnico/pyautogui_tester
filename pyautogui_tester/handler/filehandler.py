
import os
import sys
from _config.config import config

class filehandler:
    config = config()
    def __init__(self):
        pass
  
    def read_default_settings(self):
        self.default_settings = {}
        default_file = self.config.data_dir + "\\default_settings.data"
        if os.path.exists(default_file):
            with open(default_file,"r",encoding="shift_jis") as f:
                tmp_txt = f.read()
        else:
            tmp_txt = fr"""

"""
            with open(default_file,"w",encoding="shift_jis") as f:
                f.write(tmp_txt)
        tmp_txt = self.replace_setting_keywords(tmp_txt)
        tmp_txt = tmp_txt.split("\n")
        tmp_key = ""
        tmp_list = []
        for line in tmp_txt:
            if len(line)==0:
                continue
            if line[0] == "[" and line[-1] == "]":
                if len(tmp_list) > 0:
                    self.default_settings[tmp_key] = tmp_list
                    tmp_list = []
                tmp_key = line[1:-1] 
            elif line[0] == "(" and line[-1] == ")":
                line = line[1:-1].split(",")
                tmp_list.append(line)
        self.default_settings[tmp_key] = tmp_list

    def read_settings(self):
        self.settings = {}
        setting_file = self.config.data_dir + "\\settings.data"
        if os.path.exists(setting_file):
            with open(setting_file,"r",encoding="shift_jis") as f:
                tmp_txt = f.read()
        else:
            tmp_txt = r"""[Sttings]
DefaultWaitTime:1
# 0:None 1:low 2:middle 3:high
LogLevel:3
# sample definition
sampleexe:C:\sample\sample.exe
samplebat:C:\sample\sample.bat
"""
            with open(setting_file,"w",encoding="shift_jis") as f:
                f.write(tmp_txt)
            print(f"設定ファイルを新規作成しました。処理を中断するので編集の上実行ください:{setting_file}")
            self.read_actions()
            sys.exit()
        tmp_list = tmp_txt.split("\n")
        tmp_list = [i for i in tmp_txt if i.find("#")!=0]
        for line in tmp_list:
            key = line.split(":")[0]
            value = line[len(line.find(":")):]
            if key == "DefaultWaitTime":
                try:
                    self.DefaultWaitTime = value
                except:
                    text = "DefaultWaitTime was not found in setting.data"
                    self.write_log(text,1)
                    self.DefaultWaitTime = 1
            elif key == "LogLevel":
                try:
                    self.LogLevel = value
                except:
                    text = "LogLevel was not found in setting.data"
                    self.write_log(text,1)
                    self.LogLevel = 3
            else:
                try:
                    self.settings[key] = value
                except:
                    pass
        self.read_actions()
    
    def replace_setting_keywords(self,text):
        for key in self.settings.keys():
            text = text.replace(f"%{key}%",str(self.settings[key]))
        return text       
    
    def read_actions(self):
        self.actions = []
        actions_file = self.config.data_dir + "\\actions.data"
        if os.path.exists(actions_file):
            with open(actions_file,"r",encoding="shift_jis") as f:
                tmp_txt = f.read()
        else:
            tmp_txt = fr"""# sample setting
(100,400)
# クリックする座標を入力
# 無指定時は座標クリック後DefaultWaitTime[s]だけ待機
(100,300,5)
# 指定時は指定された時間[s]だけ待機
(tab,space)
# 特殊キーの指定
(waitThread)
# 直前に実行したスレッドと合流して、処理を待つ
(waitprocesskill:SystemConfig.exe)
# プロセスがなくなるまで待機します(Timeoutは600s)
(waitprocessstart:SystemConfig.exe)
# プロセスが立ち上がるまで待機します(Timeoutは600s)
(chk_number_of_file:C:\Program Files\sample)
# 指定したフォルダ内のファイル数が変わるまで待ちます(Timeoutは600s)
(getscreenshot:samplefile)
# スクリーンショットを取得 拡張子がついていない場合は自動でpngファイルとして保存
(launchfile:C:\ssample\sample.exe)
# 任意のファイルを起動します
(launchfilebythread:C:\ssample\sample.exe)
# 任意のファイルを別スレッドで起動します
(launchfilebyprocess:C:\ssample\sample.exe)
# 任意のファイルを別プロセスで起動します
(activewindow:Test Dialog)
# 任意のウィンドウをアクティブにします
(processkill:DeviceControlManager.exe)
# 任意のプロセスを停止させます
(INPUT:test_keyword)
# 文字入力の指定
(KEYDOWN:ctrl)
(KEYUP:ctrl)
# Keydownで押しっぱなしにするキーを指定 話すときはKEYUPで指定
(HOTKEY:ctrl,z)
# 同時押しするキーを指定
(WAIT:1)
# 時間待機
(PAUSE)
# 入力待ちの状態で待機
# Settings.data内で指定した変数は以下のように使用することが可能
(launchfile:%sampleexe%)

"""
            with open(actions_file,"w",encoding="shift_jis") as f:
                f.write(tmp_txt)
            waiting = input(f"実行したいテスト内容を指定してください: {actions_file}")
            sys.exit()
        tmp_txt = self.replace_setting_keywords(tmp_txt)
        tmp_txt = tmp_txt.split("\n")
        tmp_list = []
        for line in tmp_txt:
            if len(line)==0:
                continue
            if ((line[0] == "[" and line[-1] == "]") or 
                (line[0] == "(" and line[-1] == ")")):
                line = line[1:-1].split(",")
                tmp_list.append(line)
        self.actions = tmp_list
    
    def write_log(self,text,level):
        if (level > self.LogLevel):
            return
        time_line = self.config.get_time_ymdhms()
        log_dir = self.config.get_log_dir()
        with open(fr"{log_dir}\pyautogui_tester.log","a",encoding="shift_jis") as f:
            f.write(f"[{time_line}] {text}\n")
    
    def write_error(self,text,e,level):
        try:
            text += f"""=== エラー内容 ===
type:{str(type(e))}"""
        except:
            pass
        try:
            text += f"args:{str(e.args)}\n"
        except:
            pass
        try:
            text += f"message:{e.message}\n"
        except:
            pass
        try:
            text += f"e:{str(e)}"
        except:
            pass
        self.write_log(text,level)
    