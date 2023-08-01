import pandas as pd
import sqlite3
import streamlit as st
from src.structure import Club


def get_club_info(club_id: int = 6703918):
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    club = cursor.execute(
        f"SELECT * FROM Clubes WHERE clubId = {club_id}")
    club = club.fetchall()
    columns = [description[0] for description in cursor.description]
    club = pd.DataFrame(club, columns=columns)
    club_name = club["name"].values[0]
    is_custom_team = club["iscustomteam"].sum()
    if is_custom_team == 1:
        crest_id = club["customcrestid"].sum()
    else:
        crest_id = club["standardcrestid"].sum()

    stad_name = club["stadname"].values[0]

    cursor.close()
    connection.close()

    standard_crest_id = club["standardcrestid"].sum()

    kit_color_1 = club["kitcolor1"].sum()
    kit_color_2 = club["kitcolor2"].sum()
    kit_color_3 = club["kitcolor3"].sum()

    kit_colors = {
        "kit_color_1": kit_color_1,
        "kit_color_2": kit_color_2,
        "kit_color_3": kit_color_3
    }

    club = Club(club_id, club_name, is_custom_team, crest_id, stad_name,
                standard_crest_id, kit_colors)

    return club


def get_stadium_info(club: Club):
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    stadium = cursor.execute(
        f"SELECT * FROM Estadios WHERE name like '%{club.stad_name}%'")
    stadium = stadium.fetchall()

    if len(stadium) != 0:
        columns = [description[0] for description in cursor.description]
        stadium = pd.DataFrame(stadium, columns=columns)
        stadium = stadium.iloc[0]
    else:
        candidate_stadiums = cursor.execute("SELECT * FROM Estadios")
        candidate_stadiums = candidate_stadiums.fetchall()
        columns = [description[0] for description in cursor.description]
        candidate_stadiums = pd.DataFrame(candidate_stadiums, columns=columns)
        # Get the last 3 digits of the club id
        club_id = club.club_id
        final_club_id = int(str(club_id)[-3:])
        # Select a stadium with a id most close to the final_club_id
        stadium = candidate_stadiums.iloc[
            (candidate_stadiums["stadium_id"] -
             final_club_id).abs().argsort()[:1]]
        stadium = stadium.iloc[0]

    stadium = stadium.to_dict()
    stadium["name"] = club.stad_name

    return stadium


def get_seasons_info():
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    seasons = cursor.execute("SELECT * FROM Seasonals")
    seasons = seasons.fetchall()[0]
    columns = [description[0] for description in cursor.description]
    seasons = pd.DataFrame(seasons).T
    seasons.columns = columns

    wins = seasons["wins"].sum()
    draws = seasons["ties"].sum()
    losses = seasons["losses"].sum()

    # General stats
    goals_scored = seasons["alltimegoals"].sum()
    goals_conceded = seasons["alltimegoalsagainst"].sum()
    n_seasons = seasons["seasons"].sum()
    titles_won = seasons["titleswon"].sum()
    league_wins = seasons["leaguewins"].sum()
    div_1_won = seasons["divswon1"].sum()
    div_2_won = seasons["divswon2"].sum()
    div_3_won = seasons["divswon3"].sum()
    div_4_won = seasons["divswon4"].sum()
    promotions = seasons["promotions"].sum()
    holds = seasons["holds"].sum()
    relegations = seasons["relegations"].sum()
    best_points = seasons["bestpoints"].sum()
    best_division = seasons["bestdivision"].sum()
    star_level = seasons["starlevel"].sum()

    return {
        "wins": wins, "draws": draws, "losses": losses,
        "goals_scored": goals_scored, "goals_conceded": goals_conceded,
        "n_seasons": n_seasons, "titles_won": titles_won,
        "league_wins": league_wins, "div_1_won": div_1_won,
        "div_2_won": div_2_won, "div_3_won": div_3_won,
        "div_4_won": div_4_won, "promotions": promotions,
        "holds": holds, "relegations": relegations,
        "best_points": best_points, "best_division": best_division,
        "star_level": star_level
    }


def get_all_clubs():
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    club = cursor.execute(
        f"SELECT * FROM Clubes")
    club = club.fetchall()
    columns = [description[0] for description in cursor.description]
    clubs = pd.DataFrame(club, columns=columns)

    cursor.close()
    connection.close()

    return clubs


def get_crest_image(crest_id: int) -> str:
    root_folder = "https://fifa21.content.easports.com/fifa/fltOnlineAssets/"
    crest_folder = "05772199-716f-417d-9fe0-988fa9899c4d/2021/fifaweb/crests/"
    crest_path = f"256x256/l{crest_id}.png"
    crest_image = root_folder + crest_folder + crest_path

    return crest_image


def get_stadium_image(stadium_id: int) -> str:
    root_folder = 'https://www.ea.com/fifa/ultimate-team/web-app/content/'
    mobile_folder = '21D4F1AC-91A3-458D-A64E-895AA6D871D1/2021/fut/items'
    stadium_folder = '/images/mobile/vanity/stadium/'
    stadium_path = f'{stadium_id}.png'
    stadium_image = root_folder + mobile_folder + stadium_folder + \
        stadium_path

    return stadium_image
