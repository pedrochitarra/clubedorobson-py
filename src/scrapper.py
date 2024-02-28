"""Scrapping functions for the FIFA Pro Clubs API."""
import requests
import sqlite3
import json
import time
from tqdm import tqdm


HEADERS = {
        "Host": "proclubs.ea.com",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "content-type": "application/json",
        "Origin": "https://www.ea.com",
        "Connection": "keep-alive",
        "Referer": "https://www.ea.com/",
        "User-Agent": "Chrome/115.0.0.0 Safari/537.36"
    }

DATABASE_FILE = "data/raw/mock.db"


def update_club(club_id: int):
    """Get the club data from the API and insert it into the database. The key
    customKit is a dictionary, so it needs to be handled separately. Each key
    of it is inserted as a column in the Clubs table together with the other
    columns in the response.

    Args:
        club_id (int): The ID of the club.
    """
    params = {
        "clubIds": club_id,
        "platform": "ps5"
    }

    url_club = "https://proclubs.ea.com/api/fifa/clubs/info"
    response = requests.get(url_club, headers=HEADERS, params=params).json()

    club_data = response[f"{club_id}"]
    custom_kit = club_data["customKit"]

    # Insert club data into database
    insert_data = {}
    for key in club_data.keys():
        if key == "customKit":
            for kit_key in custom_kit.keys():
                insert_data[kit_key] = custom_kit[kit_key]
        else:
            insert_data[key] = club_data[key]

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    columns = ", ".join(insert_data.keys())
    placeholders = ', '.join(['?' for _ in insert_data.keys()])
    sql_query = f"""INSERT OR REPLACE INTO Clubs ({columns})
                VALUES ({placeholders})"""
    cursor.execute(sql_query, tuple(insert_data.values()))
    connection.commit()
    cursor.close()


def update_players(club_id: int):
    """Get the players data from the API and insert it into the database.
    Each key of the dictionary is inserted as a column in the Players table.

    Args:
        club_id (int): The ID of the club.
    """
    params = {
        "clubId": club_id,
        "platform": "ps5"
    }

    url_players = "https://proclubs.ea.com/api/fifa/members/stats"

    response = requests.get(url_players, headers=HEADERS, params=params).json()

    players_data = response["members"]

    for player in players_data:
        player["clubId"] = club_id

    # Insert players data into database
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    columns = ", ".join(players_data[0].keys())
    placeholders = ', '.join(['?' for _ in players_data[0].keys()])
    sql_query = f"""INSERT OR REPLACE INTO Players ({columns})
                 VALUES ({placeholders})"""
    cursor.executemany(sql_query, [tuple(player.values())
                                   for player in players_data])
    connection.commit()
    cursor.close()


def update_matches(club_id: int):
    """Get the matches data from the API and insert it into the database.
    Each match element has a dictionary of clubs, a dictionary of players and
    a dictionary of aggregate stats for each club.

    Each of these dictionaries has two keys: the home club and the away club.
    The value of each key is a dictionary with the data of the club. Inside of
    each player dictionary, the key is the player ID and the value is a
    dictionary with the data of the player.

    Args:
        club_id (int): The ID of the club.
    """
    params = {
        "clubIds": club_id,
        "matchType": "gameType9",
        "platform": "ps5"
    }
    url_matches = "https://proclubs.ea.com/api/fifa/clubs/matches"

    response = requests.get(url_matches, headers=HEADERS, params=params).json()
    # Insert matches data into database
    connection = sqlite3.connect(DATABASE_FILE)

    for match in response:
        match_dict = {
            "matchId": match["matchId"],
            "timestamp": match["timestamp"]
        }
        cursor = connection.cursor()
        columns = ", ".join(match_dict.keys())
        placeholders = ', '.join(['?' for _ in match_dict.keys()])
        sql_query = f"""INSERT OR REPLACE INTO Matches
                     ({columns}) VALUES ({placeholders})"""
        cursor.execute(sql_query, tuple(match_dict.values()))
        connection.commit()
        cursor.close()

        # Insert clubs data in match into database
        for key, value in match["clubs"].items():
            club_dict = value
            club_dict["matchId"] = match["matchId"]
            club_dict["clubId"] = key
            # Remove key details because we already have the data in the
            # Clubs table.
            club_dict.pop("details")
            cursor = connection.cursor()
            columns = ", ".join(club_dict.keys())
            placeholders = ', '.join(['?' for _ in club_dict.keys()])
            sql_query = f"""INSERT OR REPLACE INTO ClubsMatches
                         ({columns}) VALUES ({placeholders})"""
            cursor.execute(sql_query, tuple(club_dict.values()))
            connection.commit()
            cursor.close()

        # Insert players data in match into database
        # This first dict contains the clubs
        for club_key, club_value in match["players"].items():
            # This second dict contains the players
            for player_key, player_value in club_value.items():
                player_dict = player_value
                player_dict["matchId"] = match["matchId"]
                player_dict["clubId"] = club_key
                player_dict["playerId"] = player_key
                cursor = connection.cursor()
                columns = ", ".join(player_dict.keys())
                placeholders = ', '.join(['?' for _ in player_dict.keys()])
                sql_query = f"""INSERT OR REPLACE INTO PlayersMatches
                             ({columns}) VALUES ({placeholders})"""
                cursor.execute(sql_query, tuple(player_dict.values()))
                connection.commit()
                cursor.close()

        # Insert club aggregate data in match into database
        for key, value in match["aggregate"].items():
            aggregate_dict = value
            aggregate_dict["matchId"] = match["matchId"]
            aggregate_dict["clubId"] = key
            cursor = connection.cursor()
            columns = ", ".join(aggregate_dict.keys())
            placeholders = ', '.join(['?' for _ in aggregate_dict.keys()])
            sql_query = f"""INSERT OR REPLACE INTO ClubsMatchesAgg
                         ({columns}) VALUES ({placeholders})"""
            cursor.execute(sql_query, tuple(aggregate_dict.values()))
            connection.commit()
            cursor.close()


def update_seasonals(club_id: int):
    """Get the seasonal data from the API and insert it into the database.
    The seasonal data contains aggregate stats for each club from all seasons.

    Args:
        club_id (int): The ID of the club.
    """
    params = {
        "clubIds": club_id,
        "platform": "ps5"
    }
    seasonals_url = "https://proclubs.ea.com/api/fifa/clubs/seasonalStats"

    response = requests.get(seasonals_url, headers=HEADERS,
                            params=params).json()[0]
    response["recentResults"] = json.dumps(response["recentResults"])

    # Insert seasonal data into database
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    columns = ", ".join(response.keys())
    placeholders = ', '.join(['?' for _ in response.keys()])
    sql_query = f"""INSERT OR REPLACE INTO Seasonals
                 ({columns}) VALUES ({placeholders})"""
    cursor.execute(sql_query, tuple(response.values()))
    connection.commit()
    cursor.close()


def update_other_clubs():
    """Get the data of other clubs that played against us from the API and
    insert it into the database. We get the IDs from the ClubsMatches table.
    """
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()
    cursor.execute("""SELECT DISTINCT clubId FROM ClubsMatches
                   WHERE clubId != 2654598""")
    other_clubs = cursor.fetchall()
    cursor.close()

    for club in tqdm(other_clubs):
        # time.sleep(0.2)
        update_club(club[0])
        # time.sleep(0.2)
        update_seasonals(club[0])
        # time.sleep(0.2)
        update_players(club[0])
        # time.sleep(0.2)
        update_matches(club[0])


def main():
    """Update the database with the data of our club from the API."""
    update_club(2654598)
    update_players(2654598)
    update_matches(2654598)
    update_seasonals(2654598)
    # update_other_clubs()


if __name__ == "__main__":
    main()
