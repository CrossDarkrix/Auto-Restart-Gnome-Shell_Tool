#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Finderが突然CPU張り付きになる現象の対策ツール

[変数解説]
CPUPercent = CPU使用率の値が入る。
OneStartDetects = いわゆるキルスイッチ。値が0の時に発動し、1の時止める。
"""

import subprocess
from time import sleep

CPUPercent = ['40'] # 初期値は「10」
OneStartDetects = ['0'] # 初期値は「0」
CPUPercent[0] = '1' # CPUPercentの数値を「1」に設定

def CPU_Usage(): # psコマンドでgnome-shellプロセスを監視
    _percent = subprocess.Popen('ps -axro %cpu,command | grep Finder', shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8', errors='ignore').split('\n')[0].split(' ')[1]
    return _percent # CPU_Usageの返り値を設定

def main():
    while True:
        try:
            try:
                if CPUPercent[0] != CPU_Usage(): # CPUPercent内の数値がCPU_Usageとは違うとき
                    if CPU_Usage() <= CPUPercent[0]: # CPU_UsageがCPUPercentより数値が低いか
                        CPUPercent[0] = CPU_Usage() # 数値が低かったのでCPUPercentに数値を書き込み
                        OneStartDetects[0] = '0' # OneStartDetectsに「0」を書き込む
                        sleep(0.9) # 0.9秒待機
                    elif CPU_Usage() >= CPUPercent[0]: # もし、CPU_Usageの数値がCPUPercentに入っている数値より高い場合発動
                        if OneStartDetects[0] == '0': # 数値が高かったが、OneStartDetectsは0かどうか
                            CPUPercent[0] = CPU_Usage() # CPUPercentにCPU_Usageの値を入力
                            OneStartDetects[0] = '1' # コマンドを実行するのでOneStartDetectsは1にする
                            subprocess.run('killall -9 Finder', shell=True) # gnome-shellの再起動
                            sleep(0.9) # 0.9秒待機
                        elif OneStartDetects[0] == '1': # キルスイッチが1だった場合
                            CPUPercent[0] = CPU_Usage() # CPUPercentにCPU_Usageの値を入力
                            sleep(180) # 3分待機
                            if CPU_Usage() >= CPUPercent[0]: # 3分間待機してもCPU_Usageの値がCPUPercentより高かった場合
                                CPUPercent[0] = CPU_Usage() # CPUPercentにCPU_Usageの値を入力
                                subprocess.run('killall -9 Finder', shell=True) # gnome-shellの再起動
                                sleep(180) # 3分待機
                            elif CPU_Usage() <= CPUPercent[0]: # CPU_Usageの値がCPUPercentより低かった場合
                                sleep(0.9) # 0.9秒待機
                            elif CPU_Usage() == CPUPercent[0]: # CPU_Usageの数値がCPUPercentと同じだった場合
                                sleep(0.9) # 0.9秒待機
                else: # CPUPercent内の数値がCPU_Usageと同じだった場合
                    sleep(0.9) # 0.9秒待機
            except: # 問題が発生した場合
                sleep(1) # 1秒待機
        except KeyboardInterrupt: # CTRL+Cが入力された場合
            break # ループを抜け出す。

if __name__ == '__main__':
    main()
