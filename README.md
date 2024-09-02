# Flask Application
## Step by step to run flask application
1. Create virtual environment by typing in terminal `python -m venv .venv`
2. Activate virtual environment using `source ./.venv/Scripts/activate` if you on Windows and `source ./.venv/bin/activate` if you on Linux or Mac
3. Run `pip install -r requirements.txt`
4. Create `.env` file like this with your own environment variables for PostgreSQL and Flask Application
```
FLASK_PORT=5500
FLASK_HOST='0.0.0.0'
PSQL_PORT='5432'
PSQL_HOST='127.0.0.1'
PSQL_USER='postgres'
PSQL_PASSWD='postgres'
PSQL_DB='postgres'
```
5. Then run `python db.py` to create tables for database<br>
6. Finally run `python app.py` to run flask application<br>

Enjoy! 😉