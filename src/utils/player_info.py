"""Functions to get player info from database."""
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
import os


POSITIONS = ['GK', 'SW', 'RWB', 'RB', 'RCB', 'CB', 'LCB', 'LB', 'LWB', 'RDM',
             'CDM', 'LDM', 'RM', 'RCM', 'CM', 'LCM', 'LM', 'RAM', 'CAM', 'LAM',
             'RF', 'CF', 'LF', 'RW', 'RS', 'ST', 'LS', 'LW']


def get_players_by_club(club_id: int):
    """Get all players from a club."""
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    players = cursor.execute(
        f"SELECT * FROM Players WHERE clubId = {club_id}")
    players = players.fetchall()
    columns = [description[0] for description in cursor.description]
    players = pd.DataFrame(players, columns=columns)
    cursor.close()
    connection.close()
    return players


def get_robsoners():
    """Get all players from CdR."""
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    players = cursor.execute("SELECT * FROM Robsoners")
    players = players.fetchall()
    columns = [description[0] for description in cursor.description]
    players = pd.DataFrame(players, columns=columns)
    cursor.close()
    connection.close()
    return players


def get_player_vproattr(player_name: str):
    """Get player latest vproattr. We need this for real players."""
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    players = cursor.execute(
        f"""SELECT * FROM PlayersMatches WHERE name = '{player_name}'
        ORDER BY matchId DESC LIMIT 1""")
    players = players.fetchall()
    columns = [description[0] for description in cursor.description]
    players = pd.DataFrame(players, columns=columns)
    cursor.close()
    connection.close()
    if players.empty:
        return None
    return players.iloc[0]["vproattr"]


def get_player_by_online_id(online_id: str) -> pd.DataFrame:
    """Get player by online id. We need to get opponent players attributes."""
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    players = cursor.execute(
        f"""SELECT * FROM Players WHERE name = '{online_id}'""")
    players = players.fetchall()
    columns = [description[0] for description in cursor.description]
    players = pd.DataFrame(players, columns=columns)
    cursor.close()
    connection.close()
    return players.iloc[0]


def get_players_df(selected_club: int):
    """Get players dataframe. If CdR, join with robsoners, that are custom
    players created by CdR."""
    players_df = get_players_by_club(selected_club)
    if 6703918 == selected_club:
        robsoners = get_robsoners()
        # Join players and robsoners by players' name and robsoners' name
        players_df = robsoners.merge(players_df, how="left",
                                     left_on="name", right_on="name")

        players_df.sort_values(by="number", inplace=True)

        for index, row in players_df.iterrows():
            # Create a proPos column with the values of proPos_x or proPos_y
            if row["proPos_x"] is not None and row["proPos_x"] != "":
                players_df.at[index, "proPos"] = row["proPos_x"]
            else:
                players_df.at[index, "proPos"] = row["proPos_y"]
            # Create a proNationality column with the values of
            # proNationality_x or proNationality_y
            if not np.isnan(row["proNationality_x"]):
                players_df.at[index, "proNationality"] = row["proNationality_x"]
            else:
                players_df.at[index, "proNationality"] = row["proNationality_y"]
            # Create a proHeight column with the values of proHeight_x or
            # proHeight_y
            if row["proName_x"] is not None and row["proName_x"] != "":
                players_df.at[index, "proName"] = row["proName_x"]
            else:
                players_df.at[index, "proName"] = row["proName_y"]
            # Create a vproattr column. If it doesn't exist, get it from
            # database
            if row["vproattr"] is None:
                players_df.at[index, "vproattr"] = get_player_vproattr(
                    row["name"])

        # Drop unnecessary columns
        players_df.drop(
            columns=["proPos_x", "proPos_y", "proName_x", "proHeight_y",
                    "createdAt_x", "updatedAt_x",
                    "proNationality_x", "proNationality_y"],
            inplace=True)

        # Rename columns
        players_df.rename(columns={"proHeight_x": "proHeight"}, inplace=True)

    else:
        # For players that aren't CdR players, we don't have some names
        for index, row in players_df.iterrows():
            if row["proName"] is None or row["proName"] == "":
                players_df.at[index, "proName"] = row["name"]
        players_df["gamesPlayed"] = players_df["gamesPlayed"].apply(
            lambda x: int(x))
        players_df = players_df[(players_df["gamesPlayed"] > 0) &
                                (players_df["proNationality"] != "")]
        players_df.drop(columns=["createdAt", "updatedAt"], inplace=True)

    # Set the name of the player position
    players_df["proPos"] = players_df["proPos"].apply(
        lambda x: POSITIONS[int(x)])
    players_df["proNationality"] = players_df["proNationality"].astype(int)

    players_df["Details"] = False
    # For players that aren't CdR players, we set None to some columns
    if "number" not in players_df.columns:
        players_df["number"] = None
    if "birthdate" not in players_df.columns:
        players_df["birthdate"] = None
    if "weight" not in players_df.columns:
        players_df["weight"] = None

    # Convert the nationality to the flag path
    ea_root_folder = \
        "https://www.ea.com/ea-sports-fc/ultimate-team/web-app/content/"
    flags_root_folder = "24B23FDE-7835-41C2-87A2-F453DFDB2E82/2024/"
    fut_root_folder = "fut/items/images/mobile/flags/list/"
    flag_path = ea_root_folder + flags_root_folder + fut_root_folder

    players_df["proNationality"] = players_df["proNationality"].apply(
        lambda x: flag_path + str(x) + ".png")
    # Put proName, proPos, proNationality, number, birthDate, gamesPlayed,
    # goals, assists and Details in the first columns
    first_cols = ["Details", "proName", "proPos", "proNationality",
                    "number", "birthdate", "proHeight", "weight",
                    "gamesPlayed", "goals", "assists"]
    players_df = players_df[first_cols + players_df.columns.difference(
        first_cols).tolist()]

    return players_df

class Player:
    """Player class. It is used to create a player object with all the
    attributes of a player."""
    def __init__(self, player_info) -> None:
        for key, value in player_info.items():
            setattr(self, key, value)

        face_image =f"assets/players/{self.proName.replace(' ', '_').upper()}.png"
        # Check if file exists
        if os.path.isfile(face_image):
            self.image = face_image
        else:
            self.image = "https://www.fifacm.com/content/media/imgs/fifa23/players/notfound_0.png"

        self.__build_general_stats()

    def __build_stats_vproattr(self):
        attr_names = [
            "aceleracao", "pique", "agilidade", "equilibrio", "impulsao",
            "folego", "forca", "reacao", "combatividade", "frieza",
            "interceptacao", "posAtaque", "visao", "chuteslonge",
            "forcachute", "conducao", "finalizacao", "cobrancafalta",
            "cabeceio", "lancamento", "passecurto", "nocaodefensiva",
            "cruzamento", "controlebola", "divididaempe", "carrinho",
            "voleio", "curva", "penaltis", "goleiro",
            "mergulho", "manejo", "chutegoleiro", "reflexos"
        ]

        # Check if vproattr is a property of the object
        if not hasattr(self, "vproattr"):
            self.vproattr = get_player_vproattr(self.name)

        if self.vproattr is not None:
            vproattr_list = self.vproattr.split("|")
            for index, attr in enumerate(attr_names):
                if "|" in self.vproattr:
                # Set the value of the attribute in the self object
                    setattr(self, attr, int(vproattr_list[index]))
                else:
                    setattr(self, attr, 0)

    def __build_general_stats(self):
        self.__build_stats_vproattr()
        if self.vproattr is not None:
            self.generalFinishing = \
                int(
                    self.finalizacao * 0.45 + self.chuteslonge * 0.2 +
                    self.forcachute * 0.2 + self.posAtaque * 0.05 +
                    self.penaltis * 0.05 + self.voleio * 0.05
                )

            self.generalPace = \
                int(self.pique * 0.55 + self.aceleracao * 0.45)

            self.generalPassing = \
                int(
                    self.passecurto * 0.35 + self.visao * 0.2 +
                    self.cruzamento * 0.2 + self.lancamento * 0.15 +
                    self.curva * 0.05 + self.cobrancafalta * 0.05
                )

            self.generalDribbling = \
                int(
                    self.conducao * 0.5 + self.controlebola * 0.35 +
                    self.agilidade * 0.1 + self.equilibrio * 0.05
                )

            self.generalDefending = \
                int(
                    self.nocaodefensiva * 0.3 + self.divididaempe * 0.3 +
                    self.interceptacao * 0.2 + self.cabeceio * 0.1 +
                    self.carrinho * 0.1
                )

            self.generalPhysical = \
                int(
                    self.forca * 0.5 + self.folego * 0.25 +
                    self.combatividade * 0.2 + self.impulsao * 0.05
                )
