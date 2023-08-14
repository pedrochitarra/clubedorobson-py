"""Functions and class to get club information from database."""
import pandas as pd
import sqlite3
import numpy as np


class Club:
    """Class containing the club information. This includes the club name,
    crest, stadium name, stadium capacity, home and away kits, and the
    team's colors.

    Attributes:
        club_id: The club's ID
        club_name: The club's name
        is_custom_team: Whether the club is a custom team or not
        crest_id: The club's crest ID
        stadium_name: The club's stadium name
        standard_crest_id: The club's standard crest ID
        kit_colors: The club's kit colors
        home_kit_path: The club's home kit image path
        away_kit_path: The club's away kit image path
        crest_path: The club's crest image path
        stadium_path: The club's stadium image path
        stadium_capacity: The club's stadium capacity
    """
    def __init__(self, club_id, club_name, is_custom_team,
                 crest_id, stad_name, standard_crest_id,
                 kit_colors) -> None:
        self.club_id = club_id
        self.club_name = club_name
        self.is_custom_team = is_custom_team
        self.crest_id = crest_id
        self.stadium_name = stad_name
        self.standard_crest_id = standard_crest_id
        self.kit_colors = kit_colors

        self.__get_kits_urls()
        self.__get_crest_url()
        self.__get_stadium()
        self.__get_stadium_url()

    def __get_crest_url(self):
        """Get the crest image path from the club's crest ID. The crest ID is
        used to get the image path from the FIFA 21 database."""
        root_folder = \
            "https://fifa21.content.easports.com/fifa/fltOnlineAssets/"
        crest_folder = \
            "05772199-716f-417d-9fe0-988fa9899c4d/2021/fifaweb/crests/"
        crest_path = f"256x256/l{self.crest_id}.png"
        self.crest_path = root_folder + crest_folder + crest_path


    def __get_kits_urls(self):
        """Get the home and away kit image paths from the club's standard crest
        ID. The standard crest ID is used to get the image paths from the FIFA
        21 database."""
        root_folder = 'https://www.ea.com/fifa/ultimate-team/web-app/content/'
        mobile_folder = '21D4F1AC-91A3-458D-A64E-895AA6D871D1/2021/fut/items'
        home_kit_folder = '/images/mobile/kits/home/'
        away_kit_folder = '/images/mobile/kits/away/'
        self.home_kit_path = root_folder + mobile_folder + home_kit_folder + \
            f'j0_{self.standard_crest_id}_0.png'
        self.away_kit_path = root_folder + mobile_folder + away_kit_folder + \
            f'j1_{self.standard_crest_id}_0.png'

    def __get_stadium_url(self):
        """Get the stadium image path from the club's stadium ID. The stadium
        ID is used to get the image path from the FIFA 21 database."""
        root_folder = 'https://www.ea.com/fifa/ultimate-team/web-app/content/'
        mobile_folder = '21D4F1AC-91A3-458D-A64E-895AA6D871D1/2021/fut/items'
        stadium_folder = '/images/mobile/vanity/stadium/'
        stadium_path = f'{self.stadium_id}.png'
        self.stadium_path = root_folder + mobile_folder + stadium_folder + \
            stadium_path

    def __get_stadium(self):
        """Get the stadium name and capacity from the club's stadium name. The
        stadium name is used to get the stadium name and capacity from the
        FIFA 21 database."""
        database_file = "data/raw/clubedorobson.db"
        connection = sqlite3.connect(database_file)
        cursor = connection.cursor()
        # Check it the stadium name is in the database. There are some
        # stadiums that can have custom names by game design. If the stadium
        # name is not in the database, it's created by the club id so
        # that every club has a stadium image.
        stadium = cursor.execute(
            f"SELECT * FROM Estadios WHERE name like '%{self.stadium_name}%'")
        stadium = stadium.fetchall()

        if len(stadium) != 0:
            columns = [description[0] for description in cursor.description]
            stadium = pd.DataFrame(stadium, columns=columns)
            stadium = stadium.iloc[0]
        else:
            candidate_stadiums = cursor.execute("SELECT * FROM Estadios")
            candidate_stadiums = candidate_stadiums.fetchall()
            columns = [description[0] for description in cursor.description]
            candidate_stadiums = pd.DataFrame(candidate_stadiums,
                                              columns=columns)
            # Get the last 3 digits of the club id
            club_id = self.club_id
            final_club_id = int(str(club_id)[-3:])
            # Select a stadium with a id most close to the final_club_id
            stadium = candidate_stadiums.iloc[
                (candidate_stadiums["stadium_id"] -
                final_club_id).abs().argsort()[:1]]
            stadium = stadium.iloc[0]

        stadium = stadium.to_dict()
        self.stadium_id = stadium["stadium_id"]
        self.stadium_capacity = stadium["capacity"]


def get_club_info(club_id: int = 6703918):
    """Get the club's name, crest ID, stadium name, stadium ID, stadium
    capacity, kit colors and if the club is a custom team from the FIFA 21
    database. The club ID is used to get the club's information from the
    database.

    Args:
        club_id (int): The club's ID. Defaults to 6703918.
    """
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    club = cursor.execute(
        f"SELECT * FROM Clubes WHERE clubId = {club_id}")
    club = club.fetchall()
    columns = [description[0] for description in cursor.description]
    cursor.close()
    connection.close()
    club = pd.DataFrame(club, columns=columns)
    club_name = club["name"].values[0]
    is_custom_team = club["iscustomteam"].sum()
    # If the team is a custom team, the crest ID is in the column
    # customcrestid. If not, the crest ID is in the column standardcrestid.
    if is_custom_team == 1:
        crest_id = club["customcrestid"].sum()
    else:
        crest_id = club["standardcrestid"].sum()
    # The stadium name is in the column stadname.
    stad_name = club["stadname"].values[0]

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


def get_seasons_info() -> dict:
    """Get the club's seasons information from the FIFA 21 database."""
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    seasons = cursor.execute("SELECT * FROM Seasonals")
    seasons = seasons.fetchall()[0]
    columns = [description[0] for description in cursor.description]
    cursor.close()
    connection.close()

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


def get_all_clubs() -> pd.DataFrame:
    """Get all clubs from the database."""
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    club = cursor.execute("SELECT * FROM Clubes")
    club = club.fetchall()
    columns = [description[0] for description in cursor.description]
    clubs = pd.DataFrame(club, columns=columns)

    cursor.close()
    connection.close()

    return clubs


def get_club_last_matches(club_id: int) -> pd.DataFrame:
    """Get the club's last 10 matches from the database.

    Args:
        club_id (int): The club's ID.
    """
    database_file = "data/raw/clubedorobson.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    matches = cursor.execute(
        f"""SELECT * FROM Partidas WHERE homeClub = {club_id}
        OR awayClub = {club_id}
        ORDER BY matchId DESC
        LIMIT 10;""")
    matches = matches.fetchall()
    columns = [description[0] for description in cursor.description]

    cursor.close()
    connection.close()

    matches = pd.DataFrame(matches, columns=columns)

    # The column result is related to our club.
    matches["result"] = 0
    # The column opponent_club_id is related to the opponent club so that we
    # can get the opponent's crest.
    matches["opponent_club_id"] = 0

    # Convert the timestamp column to datetime
    matches["timestamp"] = pd.to_datetime(matches["timestamp"], unit="s")

    for i, match in matches.iterrows():
        # Check if the home club won
        home_won = match["homeClub"] > match["awayClub"]
        # Check if the match was a draw
        draw = match["homeClub"] == match["awayClub"]
        # Get the goals difference
        goals_diff = np.abs(int(match["homeGoals"]) - int(match["awayGoals"]))
        # Get the clubs that played the match
        clubs_match = [match["homeClub"], match["awayClub"]]
        # Get the club id that is not ours
        clubs_match.remove(6703918)
        opponent_club = clubs_match[0]
        matches.at[i, "opponent_club_id"] = opponent_club

        our_club = "home" if match["homeClub"] == 6703918 else "away"

        # If it was a draw, the result is 0.5
        if draw:
            matches.at[i, "result"] = 0.5
        # If a team won, check if it was our club
        elif home_won and our_club == "home":
            matches.at[i, "result"] = 1 * goals_diff
        else:
            matches.at[i, "result"] = -1 * goals_diff

    # Create a color column for the plotly bar chart
    matches["color"] = matches["result"].apply(
        lambda x: "#47cc4e" if x >= 1 else "#ff0000" if x <= -1 else "#f2f2f2")

    return matches
