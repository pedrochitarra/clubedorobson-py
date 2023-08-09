import streamlit as st
import src.utils.player_info as player_info
import plotly.graph_objects as go


def update_edited_rows():
    # Get keys from st.session_state.edited_rows that are not in
    # st.session_state.custom_edited_rows
    # st.write(st.session_state.matches_df)
    edited_rows = st.session_state.players_element["edited_rows"]
    # Keep only the highest value of edited_rows dict
    edited_rows = [(k, v["Details"]) for (k, v) in edited_rows.items()]
    # st.write(edited_rows)
    # Get elements from edited_rows that the second element is True
    edited_rows = [row[0] for row in edited_rows if row[1]]
    # st.write(edited_rows)
    # Keep only the highest value of edited_rows list
    selected_player = max(edited_rows) if len(edited_rows) > 0 else None
    st.session_state["selected_player"] = selected_player


def component_club_players(players_df):
    if "selected_player" not in st.session_state:
        st.session_state["selected_player"] = None

    st.data_editor(
        players_df, key="players_element", use_container_width=True,
        hide_index=True,
        on_change=update_edited_rows,
        column_config={
            "memberid": None, "name": None, "vproattr": None,
            "proName": st.column_config.TextColumn("Name"),
            "number": st.column_config.NumberColumn("#"),
            "birthdate": st.column_config.TextColumn("Born"),
            "proHeight": st.column_config.NumberColumn("Height (cm)"),
            "weight": st.column_config.NumberColumn("Weight (kg)"),
            # TODO: faces in assets!
            "face": None, "isfake": None,
            # TODO: for isfake, use x and y for the others
            "proPos": st.column_config.TextColumn("ProPos"),
            "gamesPlayed": st.column_config.TextColumn("Games"),
            "goals": st.column_config.TextColumn("⚽"),
            "assists": st.column_config.TextColumn("🅰️"),
            "proNationality": st.column_config.ImageColumn("Country"),
            "cleanSheetsDef": None, "cleanSheetsGK": None,
            "shotSuccessRate": None, "passesMade": None,
            "passSuccessRate": None, "tacklesMade": None,
            "tackleSuccessRate": None, "proName_y": None,
            "proStyle": None, "proHeight_y": None, "proNationality_y": None,
            "proOverall": None, "manOfTheMatch": None, "redCards": None,
            "favoritePosition": None, "createdAt_y": None, "updatedAt_y": None,
            "winRate": None,
            "clubid": None}
        )


def component_selected_player(players_df):
    if st.session_state["selected_player"] is not None:
        selected_player = players_df.iloc[st.session_state["selected_player"]]
        player = player_info.Player(selected_player.to_dict())
        player.build_general_stats()
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            st.header(player.proName)
            st.subheader(player.proPos)
            st.metric("Number", player.number)
            st.metric("Height (cm)", player.proHeight)
            st.metric("Weight (kg)", player.weight)
            st.metric("Born", player.birthdate)
            st.image(player.proNationality)

        with col_2:
            categories = [
                "Finishing", "Pace", "Passing", "Dribbling", 
                "Defending", "Physical"]
            values = [
                player.generalFinishing, player.generalPace,
                player.generalPassing, player.generalDribbling,
                player.generalDefending, player.generalPhysical
            ]

            # Create a radar chart using Scatterpolar
            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                text=values,
                fill='toself',  # Fill the area inside the radar
                marker=dict(color='rgba(255, 0, 0, 0.5)'),  # Marker settings
                name='Player Stats'
            ))
            # Update layout
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=False,
                                           tickfont=dict(color='black', size=20),
                                           range=[30, 100])),
                title='Player Stats',
                font=dict(size=20)
            )
            # Change font color to white
            fig.update_layout(font_color='white')

            fig.update_layout(title=dict(font=dict(size=30)),
                              paper_bgcolor='rgba(0,0,0,0)',
                              plot_bgcolor='rgba(0,0,0,0)')
            # Show the plot
            st.image(fig.to_image(format="png"), use_column_width=True)
            # st.plotly_chart(fig, use_container_width=True)

        with col_3:
            st.image(player.image, use_column_width=True)
            sub_col_1, sub_col_2, sub_col_3, sub_col_4 = st.columns(4)
            with sub_col_1:
                if not player.isfake:
                    st.metric("Games", player.gamesPlayed)
                    st.metric("Win %", player.winRate)
                    st.metric("MOTM", player.manOfTheMatch)
            with sub_col_2:
                if not player.isfake:
                    st.metric("Goals", player.goals)
                    st.metric("Assists", player.assists)
                    st.metric("Overall", player.proOverall)
            with sub_col_3:
                if not player.isfake:
                    st.metric("Passes", player.passesMade)
                    st.metric("Passes %", player.passSuccessRate)
                    st.metric("Shot %", player.shotSuccessRate)
            with sub_col_4:
                if not player.isfake:
                    st.metric("Tackles", player.tacklesMade)
                    st.metric("Tackles %", player.tackleSuccessRate)
                    st.metric("Red Cards", player.redCards)
