import json
import pandas as pd

from Configuraion import Configuration


class ParseToSql:
    def __init__(self, config: Configuration, headerKey: str) -> None:
        self.dfs = []
        self.uniqueValues = []
        self.cfg = config
        self.headerKey = headerKey

        self.fillDfs()

    def run(self):
        self.fillValues()
        self.makeAsterSqlFile(
            self.cfg.getSqlForAster(), 
            self.uniqueValues, 
            self.cfg.getIVR()
            )

    def fillValues(self):
        for i in range(len(self.dfs)):
            offerValues = []

            for value in self.dfs[i][self.headerKey]:
                offerValues.append(value)

                if value not in self.uniqueValues:
                    self.uniqueValues.append(value)

            self.makeRuleSqlFile(
                self.cfg.getSqlForRule(),
                offerValues,
                self.cfg.getRuleIds()[i],
                self.cfg.getNames()[i]
            )

    def fillDfs(self):
        for name in self.cfg.getNames():
            self.dfs.append(pd.read_csv("./source/{0}.csv".format(name), dtype=str))

    def makeRuleSqlFile(self, baseString, values, ruleId, fileName):
        strValues = self.parseArrayWithDoubleQuotes(values)

        ruleSql = baseString + '\'{"values":'+strValues+'", question:1"}\'' + ' where id='+str(ruleId)+";"
        file = open('./output/{}.sql'.format(fileName), 'w')
        file.write(ruleSql)
        file.close()

    def parseArrayWithDoubleQuotes(self, values: list) -> str:
        string = ''
        first = True
        for value in values:
            if first:
                first = False
                string += '"{0}"'.format(value)
            else:
                string += ', "{0}"'.format(value)

        return "["+string+"]"

    def makeAsterSqlFile(self, baseString, values, ivr):
        first = True

        for value in values:
            if first:
                first = False
                baseString += "({0}, '{1}')".format(ivr, value)

            else:
                baseString += ", ({0}, '{1}')".format(ivr, value)

        file = open("./output/aster.sql", "w")
        file.write(baseString)
        file.close()
