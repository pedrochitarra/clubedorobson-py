import src.utils.club_info as club_info
import streamlit as st
import src.utils.player_info as player_info


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

players = player_info.get_players_by_club(selected_club)
st.write(players)

if 6703918 == selected_club:
    robsoners = player_info.get_robsoners()

    # Join players and robsoners by players' name and robsoners' name
    players_df = robsoners.merge(players, how="left",
                                 left_on="name", right_on="name")

    players_df.sort_values(by="number", inplace=True)
    players_df["Details"] = False

    st.data_editor(
        players, key="players_element", use_container_width=True,
        hide_index=True,
        column_config={
            "memberid": None, "name": None, "vproattr": None,
            "proName_x": st.column_config.TextColumn("Name"),
            "number": st.column_config.NumberColumn("#"),
            "birthDate": st.column_config.TextColumn("Born"),
            "proHeight_x": st.column_config.NumberColumn("Height"),
            "proWeight_x": st.column_config.NumberColumn("Weight"),
            # TODO: faces in assets!
            "face": None, "isfake": None,
            "createdAt_x": None, "updatedAt_x": None,
            # TODO: flag from fifa assets!
            "proNationality_x": None,
            # TODO: for isfake, use x and y for the others
            "proPos_x": None,
            "gamesPlayed": st.column_config.TextColumn("Games"),
            "winRate": st.column_config.TextColumn("Win %"),
            "goals": st.column_config.TextColumn("⚽"),
            "assists": st.column_config.TextColumn("🅰️"),
            "cleanSheetsDef": None, "cleanSheetsGK": None,
            "shotSuccessRate": None, "passesMade": None,
            "passSuccessRate": None, "tacklesMade": None,
            "tackleSuccessRate": None, "proName_y": None, "proPos_y": None,
            "proStyle": None, "proHeight_y": None, "proNationality_y": None,
            "proOverall": None, "manOfTheMatch": None, "redCards": None,
            "favoritePosition": None, "createdAt_y": None, "updatedAt_y": None,
            "clubid": None}
        )