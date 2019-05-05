import logging
import os

## Logger
class Logger():

    def __init__(self, projectRoot):
        # Specify logger layout
        self.logger = logging.getLogger('eth')
        hdlr = logging.FileHandler(os.path.join(projectRoot, 'log', 'eth.log'))
        formatter = logging.Formatter('%(asctime)s (%(levelname)s) - %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)  # to get information from info and above