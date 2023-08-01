import streamlit as st



def update_edited_rows():
    # Get keys from st.session_state.edited_rows that are not in
    # st.session_state.custom_edited_rows
    # st.write(st.session_state.matches_df)
    edited_rows = st.session_state.matches_element["edited_rows"]
    # st.write(edited_rows)
    # Keep only the highest value of edited_rows dict
    edited_rows = [(k, v["Details"]) for (k, v) in edited_rows.items()]
    # st.write(edited_rows)
    # Get elements from edited_rows that the second element is True
    edited_rows = [row[0] for row in edited_rows if row[1]]
    # st.write(edited_rows)
    # Keep only the highest value of edited_rows list
    keep_row = max(edited_rows)
    st.session_state["keep_row"] = keep_row


def component_season_matches(matches_df):
    if "keep_row" not in st.session_state:
        st.session_state["keep_row"] = None
    st.data_editor(
        matches_df,
        column_config={
            "Home Goals": st.column_config.TextColumn("H ⚽"),
            "Away Goals": st.column_config.TextColumn("A ⚽"),
            "Home Crest": st.column_config.ImageColumn(""),
            "Away Crest": st.column_config.ImageColumn(""),
            "Stadium": st.column_config.ImageColumn("🏟️"),
            "Timestamp": st.column_config.TextColumn("⏰"),
            "match_id": None,
            "home_club_id": None,
            "away_club_id": None,
            "stadium_name": None,
            "attendance": None},
        hide_index=True,
        key="matches_element",
        on_change=update_edited_rows,
        use_container_width=True
    )


def component_selected_match(matches_df, matches_clubs):
    # st.write(st.session_state)
    if st.session_state["keep_row"] is not None:
        selected_match = matches_df.iloc[st.session_state["keep_row"]]
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
        with home_tab:
            col_1, col_2, col_3 = st.columns(3)
            with col_1:
                st.image("assets/football-icons/passes.png", width=50)
                col_1.metric("Passes",
                             home_stats["passattempts"].values[0])
                col_1.metric("Passes Completed",
                             home_stats["passesmade"].values[0])
            with col_2:
                st.image("assets/football-icons/player.png", width=50)
                col_2.metric("Shots", home_stats["shots"].values[0])
                col_2.metric("Goals", home_stats["goals"].values[0])
            with col_3:
                st.image("assets/football-icons/tackle.png", width=50)
                col_3.metric("Tackle Attempts",
                             home_stats["tackleattempts"].values[0])
                col_3.metric("Tackles Made",
                             home_stats["tacklesmade"].values[0])
        with away_tab:
            col_1, col_2, col_3 = st.columns(3)
            with col_1:
                st.image("assets/football-icons/passes.png", width=50)
                col_1.metric("Passes",
                             away_stats["passattempts"].values[0])
                col_1.metric("Passes Completed",
                             away_stats["passesmade"].values[0])
            with col_2:
                st.image("assets/football-icons/player.png", width=50)
                col_2.metric("Shots", away_stats["shots"].values[0])
                col_2.metric("Goals", away_stats["goals"].values[0])
            with col_3:
                st.image("assets/football-icons/tackle.png", width=50)
                col_3.metric("Tackle Attempts",
                             away_stats["tackleattempts"].values[0])
                col_3.metric("Tackles Made",
                             away_stats["tacklesmade"].values[0])

