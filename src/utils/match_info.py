"""Functions to get match info from database."""
import sqlite3
import pandas as pd
import src.utils.club_info as utils_club
import numpy as np
from typing import Tuple


def get_seasons_list():
    """Get all seasons values of our team from database."""
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    # Get all matches from database
    matches = cursor.execute("SELECT * FROM Partidas")
    matches = matches.fetchall()
    columns = [description[0] for description in cursor.description]
    matches = pd.DataFrame(matches, columns=columns)

    matches.sort_values(by=["matchId"], inplace=True)

    # Get all matches that our team played
    matches_clubs = cursor.execute("SELECT * FROM ClubesPartidas")
    matches_clubs = matches_clubs.fetchall()
    columns = [description[0] for description in cursor.description]
    matches_clubs = pd.DataFrame(matches_clubs, columns=columns)

    cursor.close()
    connection.close()

    our_club = 6703918
    matches_clubs.dropna(inplace=True)
    # Get all seasons that our team played
    our_seasons = matches_clubs[matches_clubs["clubId"] == our_club]

    # Convert to list
    seasons = our_seasons["seasonid"].unique().astype(int).tolist()
    seasons.sort()

    return seasons


def get_matches():
    """Get all matches from database."""
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    matches = cursor.execute("SELECT * FROM Partidas")
    matches = matches.fetchall()
    columns = [description[0] for description in cursor.description]
    matches = pd.DataFrame(matches, columns=columns)

    matches.sort_values(by=["matchId"], inplace=True)
    cursor.close()
    connection.close()

    return matches


def get_matches_season(season: int):
    """Get all matches from selected season."""
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    matches = cursor.execute("SELECT * FROM Partidas")
    matches = matches.fetchall()
    columns = [description[0] for description in cursor.description]
    matches = pd.DataFrame(matches, columns=columns)

    matches.sort_values(by=["matchId"], inplace=True)

    matches_clubs = cursor.execute("SELECT * FROM ClubesPartidas")
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

    return matches_ids_selected_season, matches_clubs


def get_season_matches_df(matches_ids_selected_season: list):
    """Get a dataframe with all matches_ids from selected season.

    Args:
        matches_ids_selected_season (list): List of matches ids from selected
            season.
    """
    # Get all matches from all seasons
    matches = get_matches()
    matches_df = pd.DataFrame()
    # For each match, get the match info and append to matches_df
    for match_id in matches_ids_selected_season:
        home_club = matches[
            matches["matchId"] == match_id]["homeClub"].values[0]
        away_club = matches[
            matches["matchId"] == match_id]["awayClub"].values[0]
        home_goals = matches[
            matches["matchId"] == match_id]["homeGoals"].values[0]
        away_goals = matches[
            matches["matchId"] == match_id]["awayGoals"].values[0]
        match_df = pd.DataFrame()

        # Convert timestamp to datetime
        timestamp = matches[
            matches["matchId"] == match_id]["timestamp"].values[0]
        timestamp = pd.to_datetime(timestamp, unit="s")
        # Format timestamp to stop showing seconds
        timestamp = timestamp.strftime("%d/%m/%Y %H:%M")
        home_club = utils_club.get_club_info(home_club)
        away_club = utils_club.get_club_info(away_club)
        match_df["Timestamp"] = [timestamp]
        match_df["Stadium"] = home_club.stadium_path
        match_df["stadium_name"] = [home_club.stadium_name]
        # Capacity * random number between 0.8 and 1.0.
        attendance = home_club.stadium_capacity * (
            0.8 + 0.2 * np.random.random())
        match_df["attendance"] = int(attendance)
        match_df["Home Crest"] = [home_club.crest_path]
        match_df["Home Club"] = [home_club.club_name]
        match_df["home_club_id"] = [home_club.club_id]
        match_df["Home Goals"] = [home_goals]
        match_df["Away Goals"] = [away_goals]
        match_df["Away Club"] = [away_club.club_name]
        match_df["away_club_id"] = [away_club.club_id]
        match_df["Away Crest"] = [away_club.crest_path]
        match_df["match_id"] = [match_id]
        matches_df = pd.concat([matches_df, match_df])

    matches_df["Details"] = False

    return matches_df


def get_players_in_match(match_id: int,
                         home_club_id: int) -> Tuple[pd.DataFrame,
                                                     pd.DataFrame]:
    """Get all players that played in a match and separate them by home and
    away club."""
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    players_match = cursor.execute(f"""SELECT * FROM JogadoresPartidas
                                   WHERE matchId = {match_id}""")
    players_match = players_match.fetchall()
    columns = [description[0] for description in cursor.description]
    players_match = pd.DataFrame(players_match, columns=columns)

    cursor.close()
    connection.close()

    our_players = players_match[
        players_match["clubid"] == 6703918]

    other_players = players_match[
        players_match["clubid"] != 6703918]

    if home_club_id == 6703918:
        home_players = our_players
        away_players = other_players
    else:
        home_players = other_players
        away_players = our_players

    return home_players, away_players
