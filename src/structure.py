import sqlite3
import pandas as pd
import streamlit as st


database_file = "data/raw/clubedorobson.db"
connection = sqlite3.connect(database_file)
cursor = connection.cursor()
players = cursor.execute(
    f"""UPDATE Jogadores SET proName = 'Show' WHERE proName = 'Sins'""")
connection.commit()
cursor.close()
connection.close()

class Match():
    def __init__(self, home_club: Club, away_club: Club) -> None:
        self.home_club = home_club
        self.away_club = away_club