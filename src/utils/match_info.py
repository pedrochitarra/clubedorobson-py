import sqlite3
import pandas as pd
import src.utils.club_info as utils_club
import numpy as np


def get_seasons():
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    matches = cursor.execute(
        f"SELECT * FROM Partidas")
    matches = matches.fetchall()
    columns = [description[0] for description in cursor.description]
    matches = pd.DataFrame(matches, columns=columns)

    matches.sort_values(by=["matchId"], inplace=True)

    matches_clubs = cursor.execute( 
        f"SELECT * FROM ClubesPartidas")
    matches_clubs = matches_clubs.fetchall()
    columns = [description[0] for description in cursor.description]
    matches_clubs = pd.DataFrame(matches_clubs, columns=columns)

    cursor.close()
    connection.close()

    our_club = 6703918
    matches_clubs.dropna(inplace=True)
    our_seasons = matches_clubs[matches_clubs["clubId"] == our_club]

    seasons = our_seasons["seasonid"].unique().astype(int).tolist()
    seasons.sort()

    return seasons


def get_matches():
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    matches = cursor.execute(f"SELECT * FROM Partidas")
    matches = matches.fetchall()
    columns = [description[0] for description in cursor.description]
    matches = pd.DataFrame(matches, columns=columns)

    matches.sort_values(by=["matchId"], inplace=True)
    cursor.close()
    connection.close()

    return matches


def get_matches_season(season: int):
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    matches = cursor.execute(f"SELECT * FROM Partidas")
    matches = matches.fetchall()
    columns = [description[0] for description in cursor.description]
    matches = pd.DataFrame(matches, columns=columns)

    matches.sort_values(by=["matchId"], inplace=True)

    matches_clubs = cursor.execute(
        f"SELECT * FROM ClubesPartidas")
    matches_clubs = matches_clubs.fetchall()
    columns = [description[0] for description in cursor.description]
    matches_clubs = pd.DataFrame(matches_clubs, columns=columns)

    cursor.close()
    connection.close()

    our_club = 6703918
    matches_clubs.dropna(inplace=True)

    matches_ids_selected_season = matches_clubs[
        (matches_clubs["seasonid"] == season) &
        (matches_clubs["clubId"] == our_club)]["matchId"]

    matches_selected_season = matches_clubs[
        matches_clubs["matchId"].isin(matches_ids_selected_season)]

    return matches_ids_selected_season, matches_selected_season, matches_clubs


def get_season_matches_df(matches_ids_selected_season, matches_selected_season,
                          matches):
    matches_df = pd.DataFrame()
    for match in matches_ids_selected_season:
        home_club = matches[matches["matchId"] == match]["homeClub"].values[0]
        away_club = matches[matches["matchId"] == match]["awayClub"].values[0]
        home_goals = matches[matches["matchId"] == match]["homeGoals"].values[0]
        away_goals = matches[matches["matchId"] == match]["awayGoals"].values[0]
        match_df = pd.DataFrame()

        # Convert timestamp to datetime
        timestamp = matches[matches["matchId"] == match]["timestamp"].values[0]
        timestamp = pd.to_datetime(timestamp, unit="s")
        # Format timestamp to stop showing seconds
        timestamp = timestamp.strftime("%d/%m/%Y %H:%M")
        home_club = utils_club.get_club_info(home_club)
        away_club = utils_club.get_club_info(away_club)
        match_df["Timestamp"] = [timestamp]
        # Get stadium emoji
        stadium = utils_club.get_stadium_info(home_club)
        match_df["Stadium"] = utils_club.get_stadium_image(stadium["stadium_id"])
        match_df["stadium_name"] = [stadium["name"]]
        # Capacity * random number between 0.8 and 1.0.
        attendance = stadium["capacity"] * (0.8 + 0.2 * np.random.random())
        match_df["attendance"] = int(attendance)
        match_df["Home Crest"] = [utils_club.get_crest_image(home_club.crest_id)]
        match_df["Home Club"] = [home_club.club_name]
        match_df["home_club_id"] = [home_club.club_id]
        match_df["Home Goals"] = [home_goals]
        match_df["Away Goals"] = [away_goals]
        match_df["Away Club"] = [away_club.club_name]
        match_df["away_club_id"] = [away_club.club_id]
        match_df["Away Crest"] = [utils_club.get_crest_image(away_club.crest_id)]
        match_df["match_id"] = [match]
        matches_df = pd.concat([matches_df, match_df])

    matches_df["Details"] = False

    return matches_df
