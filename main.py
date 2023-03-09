from Configuraion import Configuration
from ParseToSql import ParseToSql

parseToSql = ParseToSql(Configuration())

if __name__ == '__main__':
    parseToSql.run()
    print("Done!")
