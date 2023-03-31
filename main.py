from Configuraion import Configuration
from ParseToSql import ParseToSql

parseToSql = ParseToSql(Configuration())

if __name__ == '__main__':
    try:
        parseToSql.run()
        print("Done!")  
    except Exception as e:
        print(e)
