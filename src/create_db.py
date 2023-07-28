"""Create the database from sql dump created from Postgres. To speed things
up I'll use the sqlite3 module to create the database and then use the
sqlalchemy module to create the tables and insert the data."""


import sqlite3
import os


# Delete file if exists
if os.path.exists("data/raw/clubedorobson.db"):
    os.remove("data/raw/clubedorobson.db")
database_file = "data/raw/clubedorobson.db"
connection = sqlite3.connect(database_file)

# List of sql files to create the database
create_files = [file for file in os.listdir("sql")
                if file.endswith(".sql") and "create" in file.lower()]

for file in create_files:
    with open(f"sql/{file}", "r") as f:
        try:
            sql = f.read()
            cursor = connection.cursor()
            cursor.execute(sql)
        except Exception as e:
            cursor.close()
            connection.rollback()
            connection.close()
            raise e
        finally:
            cursor.close()
            connection.commit()

# List of sql files to insert data into the database
populate_files = [file for file in os.listdir("sql")
                  if file.endswith(".sql") and "insert" in file.lower()]

for file in populate_files:
    with open(f"sql/{file}", "r") as f:
        try:
            sql = f.read()
            cursor = connection.cursor()
            # Split the SQL statements by semicolon and execute them one by one
            statements = sql.split(";")
            for statement in statements:
                if statement.strip() != "":
                    cursor.execute(statement)
        except Exception as e:
            cursor.close()
            connection.rollback()
            connection.close()
            raise e
        finally:
            cursor.close()
            connection.commit()

connection.close()
