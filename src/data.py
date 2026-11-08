"""Acesso ao banco SQLite (backup de 24/02/2021). Cada tabela é lida uma vez e fica em cache."""
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "clubedorobson.db"
CLUB_ID = 6703918

# Colunas numéricas guardadas como texto no dump original
_NUMERIC = {
    "Players": ["gamesPlayed", "winRate", "goals", "assists", "shotSuccessRate", "passesMade",
                "passSuccessRate", "tacklesMade", "tackleSuccessRate", "proPos", "proHeight",
                "proOverall", "manOfTheMatch", "redCards"],
    "Matches": ["homeGoals", "awayGoals"],
    "PlayersMatches": ["goals", "assists", "rating", "shots", "passesmade", "passattempts",
                       "tacklesmade", "tackleattempts", "mom"],
    "ClubsMatches": ["rating"],
}


@st.cache_data
def table(name: str) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as con:
        df = pd.read_sql(f'SELECT * FROM "{name}"', con)
    for col in _NUMERIC.get(name, []):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def clubs() -> pd.DataFrame:
    return table("Clubs").set_index("clubId", drop=False)


def club(club_id: int = CLUB_ID) -> pd.Series:
    return clubs().loc[club_id]


def seasonal() -> pd.Series:
    return table("Seasonals").iloc[0]


def robsoners() -> pd.DataFrame:
    return table("Robsoners").set_index("name", drop=False)


def members() -> pd.DataFrame:
    """Jogadores reais do clube (tabela Players), com o cadastro do Robsoner quando existe."""
    players = table("Players")
    players = players[players["clubid"] == CLUB_ID].copy()
    rob = robsoners()
    players["robsoner"] = players["name"].isin(rob.index)
    players["displayName"] = [rob.at[n, "proName"] if n in rob.index else p
                              for n, p in zip(players["name"], players["proName"])]
    players["number"] = [rob.at[n, "number"] if n in rob.index else None for n in players["name"]]
    return players.sort_values("gamesPlayed", ascending=False)


def matches() -> pd.DataFrame:
    """Partidas do clube com temporada e resultado do ponto de vista do Robson ('w', 'd', 'l')."""
    m = table("Matches")
    m = m[(m["homeClub"] == CLUB_ID) | (m["awayClub"] == CLUB_ID)].copy()
    cm = table("ClubsMatches")
    seasons = cm[cm["clubId"] == CLUB_ID].set_index("matchId")["seasonid"]
    m["season"] = m["matchId"].map(seasons)
    home = m["homeClub"] == CLUB_ID
    ours = m["homeGoals"].where(home, m["awayGoals"])
    theirs = m["awayGoals"].where(home, m["homeGoals"])
    m["result"] = "d"
    m.loc[ours > theirs, "result"] = "w"
    m.loc[ours < theirs, "result"] = "l"
    m["date"] = pd.to_datetime(m["timestamp"], unit="s")
    return m.sort_values("timestamp", ascending=False)


def match(match_id: str) -> pd.Series:
    m = matches()
    return m[m["matchId"] == str(match_id)].iloc[0]


def club_match_stats(match_id: str) -> pd.DataFrame:
    cm = table("ClubsMatches")
    return cm[cm["matchId"] == str(match_id)].set_index("clubId")


def player_match_stats(match_id: str) -> pd.DataFrame:
    pm = table("PlayersMatches")
    return pm[pm["matchId"] == str(match_id)]


def stadium_capacity(name: str):
    st_ = table("Stadiums")
    hit = st_[st_["name"].str.lower() == str(name).lower()]
    return int(hit["capacity"].iloc[0]) if len(hit) else None
