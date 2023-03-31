import pandas as pd

from Configuraion import Configuration


class ParseToSql:
    def __init__(self, config: Configuration) -> None:
        self.dfs = []
        self.uniqueValues = []
        self.cfg = config

        self.fillDfs()

    def run(self):
        self.fillValues()

        self.makeAsterSqlFile(
            self.cfg.sqlForAster,
            self.uniqueValues,
            self.cfg.ivr
        )

        self.addExtra(self.cfg.ivr)
        # self.substractUnused()

    def fillValues(self):

        total = len(self.dfs)
        self.__printProgressBar(0, total, prefix = 'Progress:', suffix = 'Complete', length = 50)

        for i in range(total):
            offerValues = []

            for column in self.dfs[i].columns.values:
                for value in self.dfs[i][column]:
                    if value == '' or type(value) == float:
                        continue

                    if len(value) < 5:
                        value = "0"*(5-len(value)) + value

                    offerValues.append(value)

                    if value not in self.uniqueValues:
                        self.uniqueValues.append(value)

            self.makeRuleSqlFile(
                self.cfg.sqlForRule,
                offerValues,
                self.cfg.ruleIds[i],
                self.cfg.names[i]
            )

            self.__printProgressBar(i+1, total, prefix = 'Progress:', suffix = 'Complete', length = 50)

    def fillDfs(self):
        print("[1] Reading source files...")
        
        for name in self.cfg.names:
            self.dfs.append(pd.read_csv(
                "./source/{0}/{1}.csv".format(self.cfg.bundle, name), dtype=str))

    def makeRuleSqlFile(self, baseString, values, ruleId, fileName):
        strValues = self.parseArrayWithDoubleQuotes(values)

        ruleSql = baseString + '\'{"values":'+strValues+', "question":1}\'' + \
            ' where bundle_offer_rule_id='+str(ruleId)+";"
        file = open('./output/{0}/{1}.sql'.format(self.cfg.bundle ,fileName), 'w')
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

        print("[2] Making aster sql file. Total values = {}".format(len(values)))
        for value in values:
            if first:
                first = False
                baseString += "({0}, '{1}')".format(ivr, value)

            else:
                baseString += ", ({0}, '{1}')".format(ivr, value)

        file = open("./output/{}/aster.sql".format(self.cfg.bundle), "w")
        file.write(baseString)
        file.close()

    def addExtra(self, ivr):
        print("[3] Checking for extra values...")
        df = pd.read_csv("./source/{}/value.csv".format(self.cfg.bundle), dtype=str)

        data = df['Zips'].values.tolist()
        extraValues = []

        for value in self.uniqueValues:
            if value not in data:
                extraValues.append(value)

        print("... Extra values count: {}".format(len(extraValues)))

        baseString = self.cfg.sqlForAster

        first = True
        for value in extraValues:
            if first:
                first = False
                baseString += "({0}, '{1}')".format(ivr, value)

            else:
                baseString += ", ({0}, '{1}')".format(ivr, value)

        file = open("./output/{}/aster_extra.sql".format(self.cfg.bundle), "w")
        file.write(baseString)
        file.close()

    def substractUnused(self):
        print("[4] Finding values to remove...")
        removeCnt = len(self.cfg.remove)
        self.__printProgressBar(0, removeCnt, prefix = 'Progress:', suffix = 'Complete', length = 50)

        values = []
        sql = "delete from ivr_values where value in ("

        first = True
        for i in range(removeCnt):
            df = pd.read_csv("./source/{0}/{1}.csv".format(self.cfg.bundle ,self.cfg.remove[i]), dtype=str)

            for value in df['Zips'].tolist():
                

                if value not in self.uniqueValues and value not in values:
                    values.append(value)

                    if first:
                        first = False
                        sql += "'{0}'".format(value)
                    else:
                        sql += ", '{0}'".format(value)

            self.__printProgressBar(i+1, removeCnt, prefix = 'Progress:', suffix = 'Complete', length = 50)

        print("Values to remove count: {}".format(len(values)))
        sql += ") and ivr = {0};".format(self.cfg.ivr)

        file = open("./output/{}/remove.sql".format(self.cfg.bundle), "w")
        file.write(sql)
        file.close()
        

    def __printProgressBar (self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 80, fill = '█', printEnd = "\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()