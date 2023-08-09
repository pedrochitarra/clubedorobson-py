import src.utils.club_info as utils_club
import src.components.club_info as components_club
import streamlit as st


clubs = utils_club.get_all_clubs()
# Get CdR, the row with clubId == 6703918
cdr = clubs[clubs["clubId"] == 6703918]
# Get the index of CdR
cdr_index = int(cdr.index[0])

selected_club = st.selectbox(
    "Select a club", clubs,
    format_func=lambda x: clubs[clubs["clubId"] == x]["name"].values[0],
    index=cdr_index)

club = utils_club.get_club_info(selected_club)
club_name = club.club_name
crest_id = club.crest_id
stadium = utils_club.get_stadium_info(club)
seasons = utils_club.get_seasons_info()

components_club.component_general_info(club_name, crest_id, stadium)
components_club.component_kits(club)
if club.club_id == 6703918:

    components_club.component_seasons(seasons)
    components_club.components_goals(seasons)
    components_club.component_grouped_seasons(seasons)
    components_club.component_trophies(seasons)
