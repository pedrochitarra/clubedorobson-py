"""Create the DDL statements for the mock database."""
import sqlite3


def generate_ddl_for_tables(db_path: str) -> list:
    """Generate the DDL statements for the tables in the database.

    Args:
        db_path (str): Path to the database file.

    Returns:
        ddl_statements (list): List of DDL statements for each table.
    """
    db_connection = sqlite3.connect(db_path)
    cursor = db_connection.cursor()

    # Get table names from sqlite_master
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = [row[0] for row in cursor.fetchall()]

    ddl_statements = []

    for table_name in table_names:
        # Get the CREATE statement for each table
        cursor.execute(f"""SELECT sql FROM sqlite_master WHERE
                       type='table' AND name='{table_name}'""")
        create_statement = cursor.fetchone()[0]
        ddl_statements.append(create_statement)

    db_connection.close()

    return ddl_statements


database_path = "data/raw/mock.db"
ddl_statements = generate_ddl_for_tables(database_path)

# Write the DDL statements to a file
with open("sql/mock_ddl.sql", "w") as f:
    for ddl_statement in ddl_statements:
        f.write(ddl_statement + ";\n\n")
