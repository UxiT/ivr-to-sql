import os
from dotenv import load_dotenv

class Configuration:
    
    def __init__(self):
        load_dotenv()

        self.__names = list(os.getenv('NAMES').split(', '))
        self.__ruleIds = list(os.getenv('RULE_IDS').split(', '))
        self.__sqlForRule = os.getenv('SQL_FOR_RULE')
        self.__sqlForAster = os.getenv('SQL_FOR_ASTER')
        self.__ivr = os.getenv('IVR')
        self.__header = os.getenv('HEADER')
        self.__remove = list(os.getenv('REMOVE').split(', '))

        if(os.getenv('NAMES_EXTRA')):
            self.namesExtra = list(os.getenv('NAMES_EXTRA').split(', '))
            self.ruleIdsExtra = list(os.getenv('RULE_IDS_EXTRA').split(', '))
        else:
            self.namesExtra = None
    
    def getNames(self) -> list:
        return self.__names

    def getRuleIds(self) -> list:
        return self.__ruleIds

    def getSqlForRule(self) -> str:
        return self.__sqlForRule

    def getSqlForAster(self) -> str:
        return self.__sqlForAster

    def getIVR(self):
        return self.__ivr
    
    def getHeader(self):
        return self.__header
    
    def getRemove(self):
        return self.__remove