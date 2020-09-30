# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 17:57:33 2020

@author: shota
"""

import sys
import tkinter as tk
import pyautogui
import time
import cv2
import numpy as np
import shutil
import threading
import os

###画面のどのあたりで判定するか
x_top=200
x_bottom=300
y_top=200
y_bottom=400

###どのくらいの画素の違いで別のスライドとみなすかのしきい値
Threshold = 10000


desktop_path = os.path.expanduser("~\Desktop")

save_root = desktop_path + '\\zzzm'
save_src = save_root + '\\src'
save_image = save_root + '\\image'

os.makedirs(save_src, exist_ok=True)
os.makedirs(save_image, exist_ok=True)

def select_fold():
    
   return 0 

def count_img(img):
    value=0
    for i in range(x_top,x_bottom):
        for j in range(y_top,y_bottom):
            for k in range(3):
                value += img[i,j,k]
    return value



def button_clicked():    
    # ボタン非表示化
    Button.pack_forget()
    #ストップボタンの表示
    Button_stop = tk.Button(text=u'スライドの保存を終了する', width=50,command=destroy)
    Button_stop.pack()
    
    
    # 自動スクショを別のスレッドで実行
    thread1 = threading.Thread(target=auto_screenshot)    
    #デーモン化
    thread1.setDaemon(True)
    
    thread1.start()   

def destroy():
    # スレッド一覧を取得
    thread_list = threading.enumerate()
    # メインスレッドを取り除く
    thread_list.remove(threading.main_thread())
    for thread in thread_list:
        # スレッドごとに実行を停止して、終了
        thread.do_run = False
        #thread.join()
    root.destroy()
    
def auto_screenshot():
    count = 0         
    while(True):
        s = pyautogui.screenshot()
        s.save(save_src + '\\filename_{0:04d}.png'.format(count))
        #time.sleep(1)
        
        if count == 0:
            shutil.copyfile(save_src + '\\filename_{0:04d}.png'.format(count),save_image + '\\filename_{0:04d}.png'.format(count))
            count += 1
            continue
        
     
        
        img_src1=cv2.imread(save_src + "\\filename_{0:04d}.png".format(count))
        #time.sleep(1)
        img_src2=cv2.imread(save_src + "\\filename_{0:04d}.png".format(count-1))
        time.sleep(1)
       
        
        img_diff = cv2.absdiff(img_src2, img_src1)
        value=count_img(img_diff)
        if(value>Threshold):
            shutil.copyfile(save_src + '\\filename_{0:04d}.png'.format(count),save_image + '\\filename_{0:04d}.png'.format(count))
            
    #  削除できない場合
        if count == 1:
            count += 1
            continue     
    
    #   srcに保存した分を削除
        os.remove(save_src + "\\filename_{0:04d}.png".format(count-2))
        
        count += 1

        
        
root = tk.Tk()
root.title(u"ZZZM")
root.geometry("400x90")

#ラベル
Static1 = tk.Label(text=u'ZOOMのスライドを自動でスクショするアプリです\n先生はpdfで配布して欲しいですね…(# ﾟДﾟ)）')
Static1.pack()

#ボタン
Button = tk.Button(text=u'スライドの保存を開始する', width=50,command=button_clicked)
Button.pack()


root.mainloop()