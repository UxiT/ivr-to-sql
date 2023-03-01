import os
from dotenv import load_dotenv
from Configuraion import Configuration
from ParseToSql import ParseToSql

load_dotenv()

ivr = input("IVR: ")
parseToSql = ParseToSql(Configuration(ivr), os.environ.get("HEADER"))

if __name__ == '__main__':
    parseToSql.run()
