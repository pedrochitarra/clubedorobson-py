"""Streamlit components for the club information page. This page contains the
general information of the club, such as the club name, crest, stadium name,
stadium capacity, stadium image, home and away kits, seasons information, goals
information, trophies information and last matches information."""
import streamlit as st
import src.utils.club_info as club_info
import plotly.graph_objects as go
from src.utils.club_info import Club
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import pandas as pd


def component_general_info(club: Club):
    """Component containing the general information of the club. This includes
    the club name, crest, stadium name, stadium capacity and stadium image.
    All this information is inside the Club object.

    Args:
        club: Club object containing the club information
    """
    with st.container():
        # Define the text with a big font size using HTML tags
        team_name = f"<h2 style='text-align: center;'>{club.club_name}</h1>"
        # Render the big text using Markdown
        st.markdown(team_name, unsafe_allow_html=True)
        col_1, col_2 = st.columns(2)
        # Display the crest and stadium image
        with col_1:
            crest_image = club.crest_path
            st.image(crest_image, use_column_width=True)

        with col_2:
            stadium_image = club.stadium_path
            st.image(stadium_image, use_column_width=True)
            stadium_name = \
                f"<p style='text-align: center;'>{club.stadium_name}</p>"
            st.markdown(stadium_name, unsafe_allow_html=True)
            st.markdown(
                f"""<p style='text-align: center;'>Capacity:
                {club.stadium_capacity}</p>""",
                unsafe_allow_html=True)


def component_kits(club: Club):
    """Component containing the home and away kits of the club. This includes
    the home and away kit images. All this information is inside the Club
    object.

    Args:
        club: Club object containing the club information
    """
    with st.container():
        col_1, col_2 = st.columns(2)
        with col_1:
            st.image(club.home_kit_path, use_column_width=True)
        with col_2:
            st.image(club.away_kit_path, use_column_width=True)


def component_seasons(seasons: dict):
    """Component containing the seasons information of the club. This includes
    the number of wins, draws and losses. All this information is inside the
    seasons dictionary.

    Args:
        seasons: Dictionary containing the seasons information
    """
    wins = seasons["wins"]
    draws = seasons["draws"]
    losses = seasons["losses"]
    with st.container():
        # Create a plotly bar chart with the wins, draws and losses
        fig = go.Figure(
            data=[
                go.Bar(name="General history", x=["Wins", "Draws", "Losses"],
                       y=[wins, draws, losses])
            ])
        # Set the colors of the bars and the text inside the bars
        fig.update_traces(marker=dict(color=["#47cc4e", "#ffcc00", "#ff0000"]),
                          text=fig.data[0].y, textposition="inside")
        # Set the title
        fig.update_layout(title="General history")
        # Increase the font size of the title and the legend
        fig.update_layout(font=dict(size=24), legend=dict(font=dict(size=18)))
        st.plotly_chart(fig, use_container_width=True)


def components_goals(seasons: dict):
    """Component containing the goals information of the club. This includes
    the goals scored and conceded. All this information is inside the seasons
    dictionary.

    Args:
        seasons: Dictionary containing the seasons information
    """
    goals_scored = seasons["goals_scored"]
    goals_conceded = seasons["goals_conceded"]
    with st.container():
        # Plot a bar chart with the goals scored and conceded
        fig = go.Figure(data=[
            go.Bar(name="Goals for and against",
                   x=["Goals for", "Goals against"],
                   y=[goals_scored, goals_conceded])
        ])
        fig.update_layout(title="Goals for and against")
        # Insert the values on top of the bars and set the bar colors
        fig.update_traces(text=fig.data[0].y, textposition="inside",
                          textfont=dict(color="#FFFFFF"),
                          marker=dict(color=["#47cc4e", "#ff0000"]))
        # Increase the x axis text size
        fig.update_xaxes(tickfont=dict(size=18))
        # Increase the y axis text size
        fig.update_yaxes(tickfont=dict(size=18))
        # Increase the font size
        fig.update_layout(font=dict(size=24))
        st.plotly_chart(fig, use_container_width=True)


def component_grouped_seasons(seasons: dict):
    """Component containing the grouped seasons information of the club. This
    includes the number of seasons in each division. All this information is
    inside the seasons dictionary.

    Args:
        seasons: Dictionary containing the seasons information
    """
    n_seasons = seasons["n_seasons"]
    titles_won = seasons["titles_won"]
    best_division = seasons["best_division"]
    promotions = seasons["promotions"]
    holds = seasons["holds"]
    relegations = seasons["relegations"]

    with st.container():
        col1, col2, col3 = st.columns(3)
        col1.metric("Seasons", n_seasons)
        col2.metric("Titles", titles_won)
        col3.metric("Best division", best_division)

        col4, col5, col6 = st.columns(3)
        col4.metric("Promotions", promotions)
        col5.metric("Holds", holds)
        col6.metric("Relegations", relegations)


def component_trophies(seasons: dict):
    """Component containing the trophies images of the club. This includes
    the number of league, cup and division trophies. All this information is
    inside the seasons dictionary.

    Args:
        seasons: Dictionary containing the seasons information
    """
    league_wins = seasons["league_wins"]
    div_2_won = seasons["div_2_won"]
    div_3_won = seasons["div_3_won"]
    div_4_won = seasons["div_4_won"]
    with st.container():
        col_1, col_2, col_3, col_4 = st.columns(4)
        with col_1:
            # First division trophies
            st.image("assets/trophies/league_final.png", use_column_width=True)
            st.markdown(
                f"<h3 style='text-align: center;'>{league_wins}</h3>",
                unsafe_allow_html=True)
            st.markdown(
                "<h4 style='text-align: center;'>League wins</h4>",
                unsafe_allow_html=True)
        with col_2:
            # Second and third division trophies
            st.image("assets/trophies/2-3_final.png", use_column_width=True)
            st.markdown(
                f"<h3 style='text-align: center;'>{div_2_won}</h3>",
                unsafe_allow_html=True)
            st.markdown(
                "<h4 style='text-align: center;'>Division 2 and 3</h4>",
                unsafe_allow_html=True)
        with col_3:
            # Fourth to seventh division trophies
            st.image("assets/trophies/4-5-6-7_final.png",
                     use_column_width=True)
            st.markdown(
                f"<h3 style='text-align: center;'>{div_3_won}</h3>",
                unsafe_allow_html=True)
            st.markdown(
                "<h4 style='text-align: center;'>Division 4 to 7</h4>",
                unsafe_allow_html=True)
        with col_4:
            # Eighth to tenth division trophies
            st.image("assets/trophies/8-9-10_final.png", use_column_width=True)
            st.markdown(
                f"<h3 style='text-align: center;'>{div_4_won}</h3>",
                unsafe_allow_html=True)
            st.markdown(
                "<h4 style='text-align: center;'>Division 8 to 10</h4>",
                unsafe_allow_html=True)


def component_last_matches(matches: pd.DataFrame):
    """Component containing the last 10 matches results of the club. This
    includes the results and the opponent club crest. All this information is
    inside the matches dataframe.

    Args:
        matches: Dataframe containing the matches information
    """
    # Create a plotly bar chart with the last 10 matches results.
    fig = go.Figure(data=[
        go.Bar(name="Results",
               x=list(range(10)),
               y=matches["result"].tail(10),
               marker_color=matches["color"].tail(10))
    ])
    fig.update_layout(title="Last 10 games", title_font=dict(size=24),
                      font=dict(size=24))
    fig.update_xaxes(tickfont=dict(size=18), showticklabels=False,
                     showgrid=False)
    fig.update_yaxes(tickfont=dict(size=18), showticklabels=False,
                     range=[np.min(matches["result"]),
                            np.max(matches["result"]) + 1.25],
                     showgrid=False)

    # For each match, include the opponent club crest on top of the bar.
    for i, row in matches.iterrows():
        opponent_club_id = row['opponent_club_id']
        opponent_club = club_info.get_club_info(opponent_club_id)
        # Get the image from the url and add it to the plotly figure
        response = requests.get(opponent_club.crest_path)
        img = Image.open(BytesIO(response.content))

        fig.add_layout_image(
            dict(
                source=img, xref="x", yref="y", x=i-0.25,
                y=np.max(matches["result"]) + 1.2, sizex=1, sizey=1,
                opacity=1, layer="above"
            )
        )

    st.plotly_chart(fig, use_container_width=True)
