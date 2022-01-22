from time import sleep
from threading import Thread
import subprocess


def StartBlockMaker():
    subprocess.call(f'start /wait python BlockMakerProject/main_BlockMaker.py', shell=True)
def StartVallet(cnt,valletArgs):
    subprocess.call(f'start /wait python ValletProject\main_Vallet.py {cnt} {valletArgs}', shell=True)
def StartMiner(name):
    subprocess.call(f'start /wait python MinerProject\main_Miner.py {name}', shell=True)


if __name__ == "__main__":
    numofMiners=7
    usrnameforVallets=['Nebojsa','Teodora','Zorana','Nikola','Dusan']
    usernameforMiners=['Miner1','Miner2','Miner3','Miner4','Miner5','Miner6','Miner7']
    valletArgs = ""
    for i in usrnameforVallets:
        valletArgs=valletArgs+i+" "

    startBM=Thread(target=StartBlockMaker,args=())
    startBM.start()
    cnt =0
    sleep(2)
    for i in range(len(usrnameforVallets)):
        startVallet=Thread(target=StartVallet,args=[cnt,valletArgs])
        startVallet.start()
        cnt+=1
    cnt=0
    for i in range(len(usernameforMiners)):
        startMiner=Thread(target=StartMiner,args=[usernameforMiners[cnt]])
        startMiner.start()
        cnt+=1


