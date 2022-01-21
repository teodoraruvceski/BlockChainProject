from asyncio.log import logger
import logging

class Logger:
    def __init__(self, fileName):
        self.fileName = fileName
        logging.basicConfig(filename=fileName,format='%(asctime)s - %(levelname)s : %(message)s',datefmt='%d/%m/%Y %I:%M:%S %p' ,encoding='utf-8',level=logging.INFO)
        
    def logMessage(self,message):
        logging.info(message)

    