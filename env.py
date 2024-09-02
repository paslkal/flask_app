from os import getenv

from dotenv import load_dotenv

load_dotenv(override=True)

flask_port = int(getenv('FLASK_PORT', '5500'))
flask_host = getenv('FLASK_HOST')
port=getenv('PSQL_PORT')
host=getenv('PSQL_HOST')
database=getenv('PSQL_DB')
user=getenv('PSQL_USER')
password=getenv('PSQL_PASSWD')

env = dict(port=port, host=host, database=database, user=user, password=password)
