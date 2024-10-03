import logging

class Logger:
    def __init__(self,name):
        logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s', handlers=[
            logging.FileHandler(f"logs/{name}.log"),
            logging.StreamHandler()
        ])
        self.logger=logging.getLogger(name)
    def log(self,message):
        self.logger.info("Logging started")
        self.logger.info(message)
        