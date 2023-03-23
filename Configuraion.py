import os
from dotenv import load_dotenv

class Configuration:
    
    def __init__(self):
        load_dotenv()

        self.names = list(os.getenv('NAMES').split(', '))
        self.ruleIds = list(os.getenv('RULE_IDS').split(', '))
        self.sqlForRule = os.getenv('SQL_FOR_RULE')
        self.sqlForAster = os.getenv('SQL_FOR_ASTER')
        self.ivr = os.getenv('IVR')
        self.header = os.getenv('HEADER')
        self.remove = list(os.getenv('REMOVE').split(', '))
        self.bundle = os.getenv('BUNDLE')

        if(os.getenv('NAMES_EXTRA')):
            self.namesExtra = list(os.getenv('NAMES_EXTRA').split(', '))
            self.ruleIdsExtra = list(os.getenv('RULE_IDS_EXTRA').split(', '))
        else:
            self.namesExtra = None