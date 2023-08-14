"""Components to show match info and players involved in a match."""
import streamlit as st
import src.utils.match_info as utils_match
import src.utils.player_info as utils_player
import src.components.player_info as components_player
import pandas as pd


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
            "Home Goals": st.column_config.TextColumn("H ⚽"),
            "Away Goals": st.column_config.TextColumn("A ⚽"),
            "Home Crest": st.column_config.ImageColumn(""),
            "Away Crest": st.column_config.ImageColumn(""),
            "Stadium": st.column_config.ImageColumn("🏟️"),
            "Timestamp": st.column_config.TextColumn("⏰"),
            "match_id": None, "home_club_id": None, "away_club_id": None,
            "stadium_name": None, "attendance": None},
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

        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            st.image(selected_match["Home Crest"], width=64)
        with col_2:
            st.write(f"{home_club} {home_goals} x {away_goals} {away_club}")
        with col_3:
            st.image(selected_match["Away Crest"], width=64)
        st.image(selected_match["Stadium"], width=256)
        st.write(selected_match["stadium_name"])
        st.metric("", selected_match["Timestamp"])
        st.metric("Attendance", selected_match["attendance"])
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
            st.metric("Rating", player_row["rating"])
            st.metric("Goals", player_row["goals"])
            st.metric("Shots", player_row["shots"])
            st.metric("Tackle attempts", player_row["tackleattempts"])
            st.metric("Tackles made", player_row["tacklesmade"])
            st.metric("Assists", player_row["assists"])
            st.metric("Pass attempts", player_row["passattempts"])
            st.metric("Passes made", player_row["passesmade"])
        st.divider()


def component_club_stats_in_match(club_stats: pd.DataFrame):
    """Component to show club stats in a match"""
    col_1, col_2, col_3 = st.columns(3)
    with col_1:
        st.image("assets/football-icons/passes.png", width=50)
        col_1.metric("Passes", club_stats["passattempts"].values[0])
        col_1.metric("Passes Completed", club_stats["passesmade"].values[0])
    with col_2:
        st.image("assets/football-icons/player.png", width=50)
        col_2.metric("Shots", club_stats["shots"].values[0])
        col_2.metric("Goals", club_stats["goals"].values[0])
    with col_3:
        st.image("assets/football-icons/tackle.png", width=50)
        col_3.metric("Tackle Attempts", club_stats["tackleattempts"].values[0])
        col_3.metric("Tackles Made", club_stats["tacklesmade"].values[0])
