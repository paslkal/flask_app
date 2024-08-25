from os import getenv

from dotenv import load_dotenv

load_dotenv()

port=getenv('PSQL_PORT')
host=getenv('PSQL_HOST')
db=getenv('PSQL_DB')
user=getenv('PSQL_USER')
passwd=getenv('PSQL_PASSWD')

env = dict(port=port, host=host, db=db, user=user, password=passwd)
