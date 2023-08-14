import streamlit as st
import src.utils.match_info as utils_match
import src.components.match_info as components_match
import numpy as np

st.set_page_config(layout="wide")

seasons = utils_match.get_seasons()

selected_season = st.selectbox(
    "Select a season", seasons,
    format_func=lambda x: "Season " + str(x))

matches = utils_match.get_matches()

matches_ids_selected_season, matches_selected_season, \
    matches_clubs = utils_match.get_matches_season(selected_season)

matches_df = utils_match.get_season_matches_df(matches_ids_selected_season,
                                        matches_selected_season,
                                        matches)

components_match.component_season_matches(matches_df)
if "keep_row" not in st.session_state:
    st.session_state["keep_row"] = None
components_match.component_selected_match(matches_df, matches_clubs)
