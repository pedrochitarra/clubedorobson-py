"""Streamlit components for the club information page. This page contains the
general information of the club, such as the club name, crest, stadium name,
stadium capacity, stadium image, home and away kits, seasons information, goals
information, trophies information and last matches information."""
import streamlit as st
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import pandas as pd
import base64
import plotly.graph_objects as go
import src.utils.club_info as utils_club
import src.utils.image_info as utils_image


def component_general_info(club: utils_club.Club):
    """Component containing the general information of the club. This includes
    the club name, crest, stadium name, stadium capacity and stadium image.
    All this information is inside the Club object.

    Args:
        club: Club object containing the club information
    """
    team_name = f"<h2 style='text-align: center;'>{club.club_name}</h1>"
    st.markdown(team_name, unsafe_allow_html=True)
    # Write in HTML two columns. The first column contains the crest and the
    # second column contains the stadium image, stadium name and stadium
    # capacity.
    st.markdown(
        f"<div style='display: flex; width: 100%;'>"
        f"<div style='width: 50%; text-align: center;'>"
        f"<img src='{club.crest_path}' width='100%'>"
        f"</div>"
        f"<div style='width: 50%; text-align: center;'>"
        f"<img src='{club.stadium_path}' width='100%'>"
        f"<h3>{club.stadium_name}</h3>"
        f"<h3>Capacity: {club.stadium_capacity}</h3>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )


def component_kits(club: utils_club.Club):
    """Component containing the home and away kits of the club. This includes
    the home and away kit images. All this information is inside the Club
    object.

    Args:
        club: Club object containing the club information
    """
    # Write in HTML two columns. The first column contains the home kit and the
    # second column contains the away kit.
    st.markdown(
        f"<div style='display: flex; width: 100%;'>"
        f"<div style='width: 50%; text-align: center;'>"
        f"<img src='{club.home_kit_path}' width='100%'>"
        f"</div>"
        f"<div style='width: 50%; text-align: center;'>"
        f"<img src='{club.away_kit_path}' width='100%'>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )

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
                       y=[wins, draws, losses], hoverinfo='none')
            ])
        # Set the colors of the bars and the text inside the bars
        fig.update_traces(marker=dict(color=["#47cc4e", "#ffcc00", "#ff0000"]),
                          text=fig.data[0].y, textposition="inside")
        # Set the title
        fig.update_layout(title="General history")
        # Increase the font size of the title and the legend
        fig.update_layout(font=dict(size=24), legend=dict(font=dict(size=18)))
        # Disable zoom and pan
        fig.update_layout(
            xaxis=dict(fixedrange=True),
            yaxis=dict(fixedrange=True),
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.image(fig.to_image(format="png"), use_column_width=True)
        # st.plotly_chart(fig, use_container_width=True)


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
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.image(fig.to_image(format="png"), use_column_width=True)


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

    # Write in HTML two columns. The first column contains seasons, titles and
    # best division text and values. The second column contains promotions,
    # holds and relegations text and values.
    st.markdown(
        f"<div style='display: flex; width: 100%;'>"
        f"<div style='width: 50%; text-align: center;'>"
        f"<h1>Seasons</h1>"
        f"<h2>{n_seasons}</h2>"
        f"<h1>Titles</h1>"
        f"<h2>{titles_won}</h2>"
        f"<h1>Best division</h1>"
        f"<h2>{best_division}</h2>"
        f"</div>"
        f"<div style='width: 50%; text-align: center;'>"
        f"<h1>Promotions</h1>"
        f"<h2>{promotions}</h2>"
        f"<h1>Holds</h1>"
        f"<h2>{holds}</h2>"
        f"<h1>Relegations</h1>"
        f"<h2>{relegations}</h2>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )


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

    league_wins_url = utils_image.create_blob_from_file(
        "assets/trophies/league_final.png")

    div_2_won_url = utils_image.create_blob_from_file(
        "assets/trophies/2-3_final.png")

    div_3_won_url = utils_image.create_blob_from_file(
        "assets/trophies/4-5-6-7_final.png")

    div_4_won_url = utils_image.create_blob_from_file(
        "assets/trophies/8-9-10_final.png")

    # Write in HTML 4 columns with the trophies images and the number of
    # trophies, also the name of the trophy.
    st.markdown(
        f"<div style='display: flex; width: 100%;'>"
        f"<div style='width: 25%; text-align: center;'>"
        f"<img src='data:image/png;base64,{league_wins_url}' width='100%'>"
        f"<h3>{league_wins}</h3>"
        f"<h4>League wins</h4>"
        f"</div>"
        f"<div style='width: 25%; text-align: center;'>"
        f"<img src='data:image/png;base64,{div_2_won_url}' width='100%'>"
        f"<h3>{div_2_won}</h3>"
        f"<h4>Division 2 and 3</h4>"
        f"</div>"
        f"<div style='width: 25%; text-align: center;'>"
        f"<img src='data:image/png;base64,{div_3_won_url}' width='100%'>"
        f"<h3>{div_3_won}</h3>"
        f"<h4>Division 4 to 7</h4>"
        f"</div>"
        f"<div style='width: 25%; text-align: center;'>"
        f"<img src='data:image/png;base64,{div_4_won_url}' width='100%'>"
        f"<h3>{div_4_won}</h3>"
        f"<h4>Division 8 to 10</h4>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )


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
        opponent_club = utils_club.get_club_info(opponent_club_id)
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
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # Set width and height of the image
    fig.update_layout(width=1000, height=500)

    last_10_games_url = base64.b64encode(
        fig.to_image(format='png')).decode("utf-8")

    # Write in HTML a image centered with src="a.png"
    st.markdown(
        f"<div style='display: flex; width: 100%;'>"
        f"<div style='width: 100%; text-align: center;'>"
        f"<img src='data:image/png;base64,{last_10_games_url}'"
        f"width='100%'>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )
