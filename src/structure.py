import sqlite3
import pandas as pd
import streamlit as st


class Match():
    def __init__(self, home_club: Club, away_club: Club) -> None:
        self.home_club = home_club
        self.away_club = away_club