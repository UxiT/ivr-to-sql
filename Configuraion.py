import os
from dotenv import load_dotenv

class Configuration:
    
    def __init__(self):
        load_dotenv()

        self.dir = "./source/{0}/{1}".format(os.getenv('BUNDLE'), os.getenv('DIR'))
        self.remove_dir = "./source/{0}/{1}".format(os.getenv('BUNDLE'), os.getenv('DIR_REMOVE'))
        self.sqlForRule = os.getenv('SQL_FOR_RULE')
        self.sqlForAster = os.getenv('SQL_FOR_ASTER')
        self.ivr = os.getenv('IVR')
        self.bundle = os.getenv('BUNDLE')