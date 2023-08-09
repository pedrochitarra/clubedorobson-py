
import streamlit as st

import numpy as np
import src.components.player_info as components_players
import src.utils.player_info as player_info
import src.utils.club_info as club_info


st.set_page_config(layout="wide")

clubs = club_info.get_all_clubs()
# st.write(clubs)
# Get CdR, the row with clubId == 6703918
cdr = clubs[clubs["clubId"] == 6703918]
# Get the index of CdR
cdr_index = int(cdr.index[0])

selected_club = st.selectbox(
    "Select a club", clubs,
    format_func=lambda x: clubs[clubs["clubId"] == x]["name"].values[0],
    index=cdr_index)

players_df = player_info.get_players_df(selected_club)
if selected_club == 6703918:
    components_players.component_club_players(players_df)
    components_players.component_selected_player(players_df)
else:
    st.write(players_df)
