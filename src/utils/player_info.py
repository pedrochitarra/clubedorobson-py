import sqlite3
import pandas as pd


def get_players_by_club(club_id):
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    players = cursor.execute(
        f"SELECT * FROM Jogadores WHERE clubId = {club_id}")
    players = players.fetchall()
    columns = [description[0] for description in cursor.description]
    players = pd.DataFrame(players, columns=columns)
    cursor.close()
    connection.close()
    return players


def get_robsoners():
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    players = cursor.execute(
        f"SELECT * FROM Robsoners")
    players = players.fetchall()
    columns = [description[0] for description in cursor.description]
    players = pd.DataFrame(players, columns=columns)
    cursor.close()
    connection.close()
    return players
