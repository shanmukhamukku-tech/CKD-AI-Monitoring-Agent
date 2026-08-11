import logging
import os

def setup_logger():
    logger = logging.getLogger("CKD_Agent")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # Stream Handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File Handler
        fh = logging.FileHandler("agent.log")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger

# MUST BE AT TOP-LEVEL SCOPE SO OTHER FILES CAN IMPORT IT:
logger = setup_logger()