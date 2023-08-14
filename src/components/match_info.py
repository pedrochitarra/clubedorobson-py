"""Components to show match info and players involved in a match."""
import streamlit as st
import src.utils.match_info as utils_match
import src.utils.player_info as utils_player
import src.components.player_info as components_player
import pandas as pd
import base64
import src.utils.image_info as utils_image


def update_edited_rows():
    """For component component_season_matches, it's necessary to update
    st.session_state.selected_match with the new value of
    st.session_state.edited_rows."""
    # Get keys from st.session_state.edited_rows that are not in
    # st.session_state.custom_edited_rows
    edited_rows = st.session_state.matches_element["edited_rows"]
    # Keep only the highest value of edited_rows dict
    edited_rows = [(k, v["Details"]) for (k, v) in edited_rows.items()]
    # Get elements from edited_rows that the second element is True
    edited_rows = [row[0] for row in edited_rows if row[1]]
    # Keep only the highest value of edited_rows list
    selected_match = max(edited_rows) if len(edited_rows) > 0 else None
    st.session_state["selected_match"] = selected_match


def component_season_matches(matches_df: pd.DataFrame):
    """Component to show all matches from a season. It's possible to show the
    details of a match by clicking on it."""
    if "selected_match" not in st.session_state:
        st.session_state["selected_match"] = None

    st.data_editor(
        matches_df,
        column_config={
            "Details": st.column_config.CheckboxColumn("🔍"),
            "Home Club": None, "Away Club": None,
            "Home Goals": st.column_config.TextColumn("⚽"),
            "Away Goals": st.column_config.TextColumn("⚽"),
            "Home Crest": st.column_config.ImageColumn(""),
            "Away Crest": st.column_config.ImageColumn(""),
            "Stadium": st.column_config.ImageColumn("🏟️"),
            "Timestamp": None,
            "match_id": None, "home_club_id": None, "away_club_id": None,
            "stadium_name": None, "attendance": None},
        column_order=["Details", "Home Crest", "Home Goals", "Away Goals",
                        "Away Crest", "Stadium"],
        hide_index=True, key="matches_element",
        on_change=update_edited_rows, use_container_width=True
    )


def component_selected_match(matches_df: pd.DataFrame,
                             matches_clubs: pd.DataFrame):
    """Component to show the details of a selected match.

    Args:
        matches_df (pd.DataFrame): DataFrame with all matches from a season.
        matches_clubs (pd.DataFrame): DataFrame with all matches and the
            players involved in each match.
    """
    if st.session_state["selected_match"] is not None:
        selected_match = matches_df.iloc[st.session_state["selected_match"]]
        selected_match_id = selected_match["match_id"]

        home_club = selected_match["Home Club"]
        away_club = selected_match["Away Club"]
        home_goals = selected_match["Home Goals"]
        away_goals = selected_match["Away Goals"]

        # Write in HTML the home and away clubs and crests and the score in a
        # column. Also write the stadium image, name and the attendance in
        # another column.
        st.markdown(
            f"<div style='display: flex; width: 100%;'>"
            f"<div style='width: 50%; text-align: center;'>"
            f"<img src='{selected_match['Home Crest']}' width='15%'>"
            f"<h2 style='display: inline-block; margin: 0px 10px;'>"
            f"{home_club}<br>{home_goals} x {away_goals}<br>{away_club}</h2>"
            f"<img src='{selected_match['Away Crest']}' width='15%'>"
            f"</div>"
            f"<div style='width: 50%; text-align: center;'>"
            f"<img src='{selected_match['Stadium']}' width='50%'>"
            f"<h2 style='display: inline-block; margin: 0px 10px;'>"
            f"{selected_match['stadium_name']} <br>"
            f"{selected_match['attendance']} spectators</h2>"
            f"<h3 style='display: inline-block; margin: 0px 10px;'>"
            f"{selected_match['Timestamp']}</h3>"
            f"</div>"
            f"</div>",
            unsafe_allow_html=True
        )

        match_stats = matches_clubs[
            matches_clubs["matchId"] == selected_match["match_id"]]
        home_tab, away_tab = st.tabs(
            [selected_match["Home Club"], selected_match["Away Club"]])
        home_stats = match_stats[
            match_stats["clubId"] == selected_match["home_club_id"]]
        away_stats = match_stats[
            match_stats["clubId"] == selected_match["away_club_id"]]

        home_players, away_players = utils_match.get_players_in_match(
            selected_match_id, selected_match["home_club_id"])

        with home_tab:
            component_club_stats_in_match(home_stats)
            component_players_in_match(home_players)

        with away_tab:
            component_club_stats_in_match(away_stats)
            component_players_in_match(away_players)


def component_players_in_match(players_match: pd.DataFrame):
    """Component to show players involved in a match and their stats."""
    st.header("Players")
    st.divider()
    for _, player_row in players_match.iterrows():
        player = utils_player.get_player_by_online_id(
            player_row["name"])
        player["vproattr"] = player_row["vproattr"]
        player = utils_player.Player(player.to_dict())
        st.subheader(player.proName)
        if player_row["mom"] != "0":
            st.image("assets/football-icons/motm.png", width=50)
        col_1, col_2 = st.columns(2)
        with col_1:
            components_player.component_radial_chart(player)

        with col_2:
            # Write in HTML three columns. The first one with rating, goals,
            # and shots text and values. The second one with tackle attempts
            # and tackles made text and values. The third one with assists,
            # pass attempts and passes made text and values.
            st.markdown(
                f"<div style='display: flex; width: 100%;'>"
                f"<div style='width: 33%; text-align: center;'>"
                f"Rating"
                f"<h3 style='display: inline-block; margin: 0px 10px;'>"
                f"{player_row['rating']}</h3>"
                f"Goals"
                f"<h3 style='display: inline-block; margin: 0px 10px;'>"
                f"{player_row['goals']}</h3>"
                f"Shots"
                f"<h3 style='display: inline-block; margin: 0px 10px;'>"
                f"{player_row['shots']}</h3>"
                f"</div>"
                f"<div style='width: 33%; text-align: center;'>"
                f"Tackle attempts"
                f"<h3 style='display: inline-block; margin: 0px 10px;'>"
                f"{player_row['tackleattempts']}</h3>"
                f"Tackles made"
                f"<h3 style='display: inline-block; margin: 0px 10px;'>"
                f"{player_row['tacklesmade']}</h3>"
                f"</div>"
                f"<div style='width: 33%; text-align: center;'>"
                f"Assists"
                f"<h3 style='display: inline-block; margin: 0px 10px;'>"
                f"{player_row['assists']}</h3>"
                f"Pass attempts"
                f"<h3 style='display: inline-block; margin: 0px 10px;'>"
                f"{player_row['passattempts']}</h3>"
                f"Passes made"
                f"<h3 style='display: inline-block; margin: 0px 10px;'>"
                f"{player_row['passesmade']}</h3>"
                f"</div>"
                f"</div>",
                unsafe_allow_html=True
            )

        st.divider()


def component_club_stats_in_match(club_stats: pd.DataFrame):
    """Component to show club stats in a match"""
    # Write in HTML three columns. The first one with the passes image,
    # passes and passes completed. The second one with the shots image,
    # shots and goals. The third one with the tackle image, tackle attempts
    # and tackles made.

    tackle_url = utils_image.create_blob_from_file(
        "assets/football-icons/tackle.png"
    )

    passes_url = utils_image.create_blob_from_file(
        "assets/football-icons/passes.png"
    )

    player_url = utils_image.create_blob_from_file(
        "assets/football-icons/player.png"
    )

    st.markdown(
        f"<div style='display: flex; width: 100%;'>"
        f"<div style='width: 33%; text-align: center;'>"
        f"<img src='data:image/png;base64,{passes_url}' width='50%'>"
        f"<br>Passes"
        f"<h2 style='display: inline-block; margin: 0px 10px;'>"
        f"{club_stats['passattempts'].values[0]} <br> </h2>"
        f"<br>Passes Completed"
        f"<h2 style='display: inline-block; margin: 0px 10px;'>"
        f"{club_stats['passesmade'].values[0]}</h2>"
        f"</div>"
        f"<div style='width: 33%; text-align: center;'>"
        f"<img src='data:image/png;base64,{player_url}' width='50%'>"
        f"<br>Shots"
        f"<h2 style='display: inline-block; margin: 0px 10px;'>"
        f"{club_stats['shots'].values[0]} <br></h2>"
        f"<br>Goals"
        f"<h2 style='display: inline-block; margin: 0px 10px;'>"
        f"{club_stats['goals'].values[0]}</h2>"
        f"</div>"
        f"<div style='width: 33%; text-align: center;'>"
        f"<img src='data:image/png;base64,{tackle_url}' width='50%'>"
        f"<br>Tackle Attempts"
        f"<h2 style='display: inline-block; margin: 0px 10px;'>"
        f"{club_stats['tackleattempts'].values[0]} <br></h2>"
        f"<br>Tackles Made"
        f"<h2 style='display: inline-block; margin: 0px 10px;'>"
        f"{club_stats['tacklesmade'].values[0]}</h2>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )
