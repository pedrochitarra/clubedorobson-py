"""Component to show the matches of a season and the details of a selected
match, also showing the stats of the players in each match."""
import streamlit as st
import src.utils.match_info as utils_match
import src.components.match_info as components_match


st.set_page_config(layout="wide")

# Get seasons list to select
seasons = utils_match.get_seasons_list()
selected_season = st.selectbox("Select a season", seasons,
                               format_func=lambda x: "Season " + str(x))

# Get matches ids and matches from selected season
matches_ids_selected_season, matches_clubs = utils_match.get_matches_season(
    selected_season)

# Get matches df from selected season
matches_df = utils_match.get_season_matches_df(
    matches_ids_selected_season)

components_match.component_season_matches(matches_df)
if "keep_row" not in st.session_state:
    st.session_state["keep_row"] = None
components_match.component_selected_match(matches_df, matches_clubs)
