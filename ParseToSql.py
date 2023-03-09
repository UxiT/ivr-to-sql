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
            self.cfg.getSqlForAster(),
            self.uniqueValues,
            self.cfg.getIVR()
        )

        self.addExtra(self.cfg.getIVR())

    def fillValues(self):

        total = len(self.dfs)
        self.__printProgressBar(0, total, prefix = 'Progress:', suffix = 'Complete', length = 50)

        for i in range(total):
            offerValues = []

            for value in self.dfs[i][self.cfg.getHeader()]:
                offerValues.append(value)

                if value not in self.uniqueValues:
                    self.uniqueValues.append(value)

            self.makeRuleSqlFile(
                self.cfg.getSqlForRule(),
                offerValues,
                self.cfg.getRuleIds()[i],
                self.cfg.getNames()[i]
            )

            self.__printProgressBar(i+1, total, prefix = 'Progress:', suffix = 'Complete', length = 50)

    def fillDfs(self):
        print("[1] Reading source files...")
        
        for name in self.cfg.getNames():
            self.dfs.append(pd.read_csv(
                "./source/{0}.csv".format(name), dtype=str))

    def makeRuleSqlFile(self, baseString, values, ruleId, fileName):
        strValues = self.parseArrayWithDoubleQuotes(values)

        ruleSql = baseString + '\'{"values":'+strValues+', "question":1}\'' + \
            ' where bundle_offer_rule_id='+str(ruleId)+";"
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

        print("[2] Making aster sql file. Total values = {}".format(len(values)))
        for value in values:
            if first:
                first = False
                baseString += "({0}, '{1}')".format(ivr, value)

            else:
                baseString += ", ({0}, '{1}')".format(ivr, value)

        file = open("./output/aster.sql", "w")
        file.write(baseString)
        file.close()

    def addExtra(self, ivr):
        print("[3] Checking for extra values...")
        df = pd.read_csv("./source/value.csv", dtype=str)

        data = df['Zips'].values.tolist()
        extraValues = []

        for value in self.uniqueValues:
            if value not in data:
                extraValues.append(value)

        print("... Extra values count: {}".format(len(extraValues)))

        baseString = self.cfg.getSqlForAster()

        first = True
        for value in extraValues:
            if first:
                first = False
                baseString += "({0}, '{1}')".format(ivr, value)

            else:
                baseString += ", ({0}, '{1}')".format(ivr, value)

        file = open("./output/aster_extra.sql", "w")
        file.write(baseString)
        file.close()


    def __printProgressBar (self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 80, fill = '█', printEnd = "\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
        # Print New Line on Complete
        if iteration == total: 
            print()