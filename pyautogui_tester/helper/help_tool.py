from pynput import keyboard
from pynput import mouse
from _config.config import config
import pyautogui
import threading


class HelpTool:
    config = config()
    def __init__(self):
        pass
    
    def write_handle_log(self,text):
        log_name = fr"{self.config.data_dir}\handle_reord.log"
        with open(log_name,"a",encoding="shift_jis") as f:
            f.write(text)
            f.write("\n")
    
    def on_press(self,key):
        try:
            tmp_str = f"(INPUT:{str(key.char)})"
        except AttributeError:
            tmp_str = f"(INPUT:{str(key)})"
        tmp_str = tmp_str.replace("(INPUT:Key.","(")
        self.write_handle_log(tmp_str)
    
    def on_release(self,key):
        tmp_str = f"(INPUT:{str(key)})"
        self.write_handle_log(tmp_str)
        print(f'release: {key}')
        if( key == keyboard.Key.esc):
            print("StopKey")
            self.listener.stop()
            self.listener = None
            
    def start(self):
        self.listener = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        self.listener.start()
        
    def getstatus(self):
        if(self.listener == None):
            return False       
        return True

    def record_keyboard(self):
        self.start()
        while(True):
            status = self.getstatus()
            if(status == False):
                break
    
    def on_move(self,x, y):
        return

    def on_click(self,x, y, button, pressed):
        if pressed:
            # Stop listener
            return False

    def on_scroll(self,x, y, dx, dy):
        return
    
    def record_click_point(self):
        while True:
            #リスナー起動
            with mouse.Listener(
                on_move=self.on_move,
                on_click=self.on_click,
                on_scroll=self.on_scroll) as listener:
                listener.join()
            
            
            recttop_x, recttop_y = pyautogui.position()
            tmp_str = f"({recttop_x},{recttop_y})"
            self.write_handle_log(tmp_str)
    
    def main(self):
        key_thread = threading.Thread(target=self.record_keyboard)
        key_thread.start()
        click_thread = threading.Thread(target=self.record_click_point)
        click_thread.start()

if __name__ == "__main__":
    instance = HelpTool()
    instance.main()
        