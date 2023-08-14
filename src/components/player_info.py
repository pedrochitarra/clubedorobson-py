"""Components to show player info"""
import streamlit as st
import src.utils.player_info as player_info
import plotly.graph_objects as go
import pandas as pd
import base64
import src.utils.image_info as utils_image


def update_edited_rows():
    """For component component_club_players, it's necessary to update
    st.session_state.selected_player with the new value of
    st.session_state.edited_rows."""
    # Get keys from st.session_state.edited_rows that are not in
    # st.session_state.custom_edited_rows
    edited_rows = st.session_state.players_element["edited_rows"]
    # Keep only the highest value of edited_rows dict
    edited_rows = [(k, v["Details"]) for (k, v) in edited_rows.items()]
    # Get elements from edited_rows that the second element is True
    edited_rows = [row[0] for row in edited_rows if row[1]]
    # Keep only the highest value of edited_rows list
    selected_player = max(edited_rows) if len(edited_rows) > 0 else None
    st.session_state["selected_player"] = selected_player


def component_club_players(players_df: pd.DataFrame):
    """Component to show all players from a club. It's possible to show the
    details of a player by clicking on it.

    Args:
        players_df (pd.DataFrame): DataFrame with all players from a club.
    """
    if "selected_player" not in st.session_state:
        st.session_state["selected_player"] = None
    st.data_editor(
        players_df, key="players_element", use_container_width=True,
        hide_index=True,
        on_change=update_edited_rows,
        column_config={
            "Details": st.column_config.CheckboxColumn("🔍"),
            "memberid": None, "name": None, "vproattr": None,
            "proName": st.column_config.TextColumn("Name"),
            "number": st.column_config.NumberColumn("#"),
            "birthdate": st.column_config.TextColumn("Born"),
            "proHeight": st.column_config.NumberColumn("Height (cm)"),
            "weight": st.column_config.NumberColumn("Weight (kg)"),
            "face": None, "isfake": None,
            "proPos": st.column_config.TextColumn("Pos"),
            "gamesPlayed": st.column_config.NumberColumn("Games"),
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


def component_selected_player(players_df: pd.DataFrame):
    """Component to show the details of a selected player.

    Args:
        players_df (pd.DataFrame): DataFrame with all players from a club.
    """
    if st.session_state["selected_player"] is not None:
        selected_player = players_df.iloc[st.session_state["selected_player"]]
        player = player_info.Player(selected_player.to_dict())

        player_face_url = utils_image.create_blob_from_file(
            player.image
        )

        radar_chart = component_radial_chart(player, return_image=True)
        radar_chart_url = base64.b64encode(radar_chart).decode("utf-8")

        if player.number is None:
            player.number = "N/A"
        if player.proHeight is None:
            player.proHeight = "N/A"
        if player.weight is None:
            player.weight = "N/A"
        if player.birthdate is None:
            player.birthdate = "N/A"

        # Write in HTML three columns. The first one has the player image, the
        # position, the number, the height, the weight, the birthdate and the
        # nationality. The second one has a radar chart with the player stats.
        st.markdown(
            f"<div style='display: flex; width: 100%;'>"
                f"<div style='width: 50%;'>"
                    f"<div style='display: flex; justify-content: center;'>"
                    f"<img src='data:image/png;base64,{player_face_url}' "
                    f"style='width: 80%;'>"
                    f"</div>"
                    f"<br><br>"
                    f"<div style='display: flex; justify-content: center;'>"
                        f"<img src='{player.proNationality}' width='30%'>"
                    f"</div>"
                f"</div>"

                f"<div style='width: 50%;'>"
                    f"<img src='data:image/png;base64,{radar_chart_url}' "
                    f"style='width: 100%;'>"
                f"<p style='text-align: center;  font-weight: bold;'> Position </p>"
                f"<h3 style='text-align: center;  font-weight: bold;'>"
                f"{player.proPos}</h3>"
                f"<p style='text-align: center;  font-weight: bold;'> Number </p>"
                f"<h3 style='text-align: center;  font-weight: bold;'>"
                f"{player.number}</h3>"
                f"<p style='text-align: center;  font-weight: bold;'> Height </p>"
                f"<h3 style='text-align: center;  font-weight: bold;'>"
                f"{player.proHeight} cm</h3>"
                f"<p style='text-align: center;  font-weight: bold;'> Weight </p>"
                f"<h3 style='text-align: center;  font-weight: bold;'>"
                f"{player.weight} kg</h3>"
                f"<p style='text-align: center;  font-weight: bold;'> Birthdate </p>"
                f"<h3 style='text-align: center;  font-weight: bold;'>"
                f"{player.birthdate}</h3>"
                f"</div>"
        , unsafe_allow_html=True)

        # Write in HTML four columns. The first one has the
        # games, win%, MOTM. The second one has the goals, assists and overall.
        # The third one has the passes, passes% and shot%. The fourth one has
        # the tackles, tackles% and red cards.

        stats_list = [player.gamesPlayed, player.winRate, player.manOfTheMatch,
                      player.goals, player.assists, player.proOverall,
                      player.passesMade, player.passSuccessRate,
                      player.shotSuccessRate, player.tacklesMade,
                      player.tackleSuccessRate, player.redCards]

        stats_names = ["Games", "Win %", "MOTM", "Goals", "Assists", "Overall",
                    "Passes", "Passes %", "Shot %", "Tackles", "Tackles %",
                    "Red Cards"]

        base_html = "<div style='display: flex; width: 100%;'>"
        for i in range(0, 4):
            stats_column = stats_list[i*3:(i+1)*3]
            stats_names_column = stats_names[i*3:(i+1)*3]
            base_html += \
                f"""
                <div style='width: 25%;'>
                    <p style='text-align: center; font-weight: bold;'>
                        {stats_names_column[0]}</p>
                    <h3 style='text-align: center; font-weight: bold;'>
                        {stats_column[0]}</h3>
                    <p style='text-align: center; font-weight: bold;'>
                        {stats_names_column[1]}</p>
                    <h3 style='text-align: center; font-weight: bold;'>
                        {stats_column[1]}</h3>
                    <p style='text-align: center; font-weight: bold;'>
                        {stats_names_column[2]}</p>
                    <h3 style='text-align: center; font-weight: bold;'>
                        {stats_column[2]}</h3>
                </div>
                """

        base_html += "</div>"
        # Remove empty lines from the HTML
        base_html = base_html.replace("\n", "")
        st.markdown(base_html, unsafe_allow_html=True)


def component_radial_chart(player: player_info.Player,
                           return_image: bool = False):
    """Component to show a radar chart with the player stats.

    Args:
        player (player_info.Player): Player object.
    """
    categories = [
        "Finishing", "Pace", "Passing", "Dribbling",
        "Defending", "Physical"]

    if player.vproattr is not None:
        values = [
            player.generalFinishing, player.generalPace,
            player.generalPassing, player.generalDribbling,
            player.generalDefending, player.generalPhysical
        ]
        # Create a radar chart using Scatterpolar
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values, theta=categories, text=values, fill='toself',
            marker=dict(color='rgba(255, 0, 0, 0.5)'), name='Player Stats'
        ))
        # Update layout
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=False,
                                    tickfont=dict(color='black', size=20),
                                    range=[50, 100])),
            title='Player Stats',
            font=dict(size=20),
            font_color='white',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig.update_layout(title=dict(font=dict(size=30)))
    else:
        empty_trace = go.Scatterpolar(r=[], theta=[], mode='markers')

        # Create a layout for the plot (optional)
        layout = go.Layout(
            polar=dict(
                radialaxis=dict(visible=True),
                angularaxis=dict(visible=True)
            )
        )

        # Create a Figure with the empty trace and layout
        fig = go.Figure(data=[empty_trace], layout=layout)
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=False,
                                    tickfont=dict(color='black', size=20),
                                    range=[50, 100])),
            title='Player Stats',
            font=dict(size=20),
            font_color='white',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        # Hide axis ticks and labels
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=False,
                    range=[0, 100]
                ),
                angularaxis=dict(
                    visible=False
                )
            )
        )
        fig.show()
    # Show the plot
    if not return_image:
        st.image(fig.to_image(format="png"), use_column_width=True)
        return None
    else:
        return fig.to_image(format="png")
