import pandas as pd
import os

from Configuraion import Configuration


class ParseToSql:
    def __init__(self, config: Configuration) -> None:
        self.dfs = []
        self.uniqueValues = []
        self.cfg = config
        self.active_names = []

        self.fillDfs()


    def run(self):
        self.fillValues()

        self.makeAsterSqlFile(
            self.cfg.sqlForAster,
            self.uniqueValues,
            self.cfg.ivr
        )

        self.addExtra(self.cfg.ivr)
        self.substractUnused()

    def fillDfs(self):
        print("[1] Reading source files...")
        
        for filename in os.listdir(self.cfg.dir):
            path = os.path.join(self.cfg.dir, filename)

            if os.path.isfile(path):
                self.dfs.append(pd.read_csv(path, dtype=str))
                self.active_names.append(filename)


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
                offerValues,
                self.active_names[i]
            )

            self.__printProgressBar(i+1, total, prefix = 'Progress:', suffix = 'Complete', length = 50)


    def makeRuleSqlFile(self, values, fileName):
        strValues = self.parseArrayWithDoubleQuotes(values)

        ruleSql = '\'{"values":'+strValues+', "question":1}\''
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
        data = pd.read_csv("./source/{}/value.csv".format(self.cfg.bundle), dtype=str)['Zips'].values.tolist()
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

        values = []
        sql = "delete from ivr_values where value in ("

        first = True

        for filename in os.listdir(self.cfg.remove_dir):
            path = os.path.join(self.cfg.remove_dir, filename)

            data = pd.read_csv(path, dtype=str)['Zips'].tolist()

            for value in data:
                if value not in self.uniqueValues and value not in values:
                    values.append(value)

                    if first:
                        first = False
                        sql += "'{0}'".format(value)
                    else:
                        sql += ", '{0}'".format(value)

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