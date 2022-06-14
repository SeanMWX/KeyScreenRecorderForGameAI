from pynput.keyboard import Key, Controller,Listener
from pynput import keyboard
import pyautogui, time, cv2, fnmatch, os
import numpy as np

def imagesave(name):
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image),
                         cv2.COLOR_RGB2BGR)
    if not os.path.exists(name):
        os.makedirs(name)
        cv2.imwrite(name+"/0.png", image)
    else:
        num = len(fnmatch.filter(os.listdir(name), '*.png'))
        cv2.imwrite(name+"/%d.png" % (num), image)

keyboard_exec = Controller()
holding_keys = []

def on_press(key):
    # stop when pressing "stop"
    if key == keyboard.Key.esc:
        listener.stop()
    # key string
    string = str(key).replace("'","")
    # do not duplicate holding_keys
    if string in holding_keys:
        return
    # pressing + holding keys
    if len(holding_keys) == 0:
        string = string
    elif len(holding_keys) > 0:
        string = string
        for i in range(len(holding_keys)):
            string = string + '+%s' % (holding_keys[i])
    # save current image
    imagesave('data/'+string)
    # add pressing key to array
    holding_keys.append(str(key).replace("'",""))
    with open('keys.txt', 'a') as f:
        f.writelines(string + "\n")
        f.flush()
    print(string)
    
def on_release(key):
    string = str(key).replace("'","")
    holding_keys.remove(string)
    string = string+'.release'
            
with Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()
    
    