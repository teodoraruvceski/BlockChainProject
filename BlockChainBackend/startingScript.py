from time import sleep
from threading import Thread
import subprocess


def StartBlockMaker():
    subprocess.call(f'start /wait python BlockMakerProject/main_BlockMaker.py', shell=True)
def StartVallet(cnt,valletArgs):
    subprocess.call(f'start /wait python ValletProject\main_Vallet.py {cnt} {valletArgs}', shell=True)
def StartMiner():
    subprocess.call(f'start /wait python MinerProject\main_Miner.py', shell=True)


if __name__ == "__main__":
    numofMiners=7
    usrnameforVallets=['Nebojsa','Teodora','Zorana','Nikola','Dusan']
    valletArgs = ""
    for i in usrnameforVallets:
        valletArgs=valletArgs+i+" "

    startBM=Thread(target=StartBlockMaker,args=())
    startBM.start()
    cnt =0
    sleep(2)
    for i in range(numofMiners):
        startVallet=Thread(target=StartVallet,args=[cnt,valletArgs])
        startVallet.start()
        cnt+=1
        
    for i in range(numofMiners):
        startMiner=Thread(target=StartMiner,args=())
        startMiner.start()


