import streamlit as st
import src.utils.club_info as club_info
import plotly.graph_objects as go
from src.structure import Club
import pandas as pd


def component_general_info(club_name, crest_id, stadium):
    with st.container():
        # Define the text with a big font size using HTML tags
        team_name = f"<h2 style='text-align: center;'>{club_name}</h1>"
        # Render the big text using Markdown
        st.markdown(team_name, unsafe_allow_html=True)
        col_1, col_2 = st.columns(2)
        with col_1:
            crest_image = club_info.get_crest_image(crest_id)
            st.image(crest_image, use_column_width=True)

        with col_2:
            stadium_image = club_info.get_stadium_image(stadium["stadium_id"])
            st.image(stadium_image, use_column_width=True)
            stadium_name = f"<p style='text-align: center;'>{stadium['name']}</p>"
            st.markdown(stadium_name, unsafe_allow_html=True)
            st.markdown(
                f"""<p style='text-align: center;'>Capacity:
                {stadium['capacity']}</p>""",
                unsafe_allow_html=True)


def component_kits(club: Club):
    with st.container():
        root_folder = 'https://www.ea.com/fifa/ultimate-team/web-app/content/'
        mobile_folder = '21D4F1AC-91A3-458D-A64E-895AA6D871D1/2021/fut/items'
        home_kit_folder = '/images/mobile/kits/home/'
        away_kit_folder = '/images/mobile/kits/away/'
        home_kit_path = mobile_folder + home_kit_folder + \
            f'j0_{club.standard_crest_id}_0.png'
        away_kit_path = mobile_folder + away_kit_folder + \
            f'j1_{club.standard_crest_id}_0.png'

        col_1, col_2 = st.columns(2)
        with col_1:
            st.image(root_folder + home_kit_path, use_column_width=True)
        with col_2:
            st.image(root_folder + away_kit_path, use_column_width=True)


def component_seasons(seasons: dict):
    wins = seasons["wins"]
    draws = seasons["draws"]
    losses = seasons["losses"]
    with st.container():
        # Create a plotly pie chart
        fig = go.Figure(data=[go.Pie(labels=["Vitórias", "Empates", "Derrotas"],
                                     values=[wins, draws, losses])])
        # Set wins color to light green, draws to yellow and losses to red
        fig.update_traces(marker=dict(colors=["#47cc4e", "#ffff00", "#ff0000"]))
        # Increase the font size
        fig.update_layout(font=dict(size=18))
        # Set the text to the absolute value of the percentage
        fig.update_traces(textinfo="value")
        # Set the title
        fig.update_layout(title="Desempenho do Clube do Robson")
        # Increase the font size of the title
        fig.update_layout(font=dict(size=24))
        # Increase the font size of the legend
        fig.update_layout(legend=dict(font=dict(size=18)))
        st.plotly_chart(fig)


def components_goals(seasons: dict):
    goals_scored = seasons["goals_scored"]
    goals_conceded = seasons["goals_conceded"]
    with st.container():
        # Plot a bar chart with the goals scored and conceded
        fig = go.Figure(data=[
            go.Bar(name="Gols marcados", x=["Gols marcados", "Gols sofridos"],
                   y=[goals_scored, goals_conceded])
        ])
        fig.update_layout(title="Gols marcados e sofridos")
        # Set the colors of the bars
        fig.update_traces(marker=dict(color=["#47cc4e", "#ff0000"]))
        # Set the font size
        fig.update_layout(font=dict(size=18))
        # Insert the values on top of the bars
        fig.update_traces(text=fig.data[0].y, textposition="outside")
        fig.update_traces(textposition="inside", textfont=dict(color="#FFFFFF"))
        # Increase the x axis text size
        fig.update_xaxes(tickfont=dict(size=18))
        # Increase the y axis text size
        fig.update_yaxes(tickfont=dict(size=18))
        # Increase the font size of the title
        fig.update_layout(font=dict(size=24))
        st.plotly_chart(fig)


def component_grouped_seasons(seasons: dict):
    n_seasons = seasons["n_seasons"]
    titles_won = seasons["titles_won"]
    best_division = seasons["best_division"]
    promotions = seasons["promotions"]
    holds = seasons["holds"]
    relegations = seasons["relegations"]

    with st.container():
        col1, col2, col3 = st.columns(3)
        col1.metric("Temporadas", n_seasons)
        col2.metric("Títulos", titles_won)
        col3.metric("Melhor divisão", best_division)

        col4, col5, col6 = st.columns(3)
        col4.metric("Acessos", promotions)
        col5.metric("Manutenções", holds)
        col6.metric("Rebaixamentos", relegations)


def component_trophies(seasons: dict):
    league_wins = seasons["league_wins"]
    div_2_won = seasons["div_2_won"]
    div_3_won = seasons["div_3_won"]
    div_4_won = seasons["div_4_won"]
    with st.container():
        # TODO: Set all the images to the same size
        col_1, col_2, col_3, col_4 = st.columns(4)
        with col_1:
            st.image("assets/trophies/league_final.png", use_column_width=True)
            st.markdown(f"<h3 style='text-align: center;'>{league_wins}</h3>",
                        unsafe_allow_html=True)
        with col_2:
            st.image("assets/trophies/2-3_final.png", use_column_width=True)
            st.markdown(f"<h3 style='text-align: center;'>{div_2_won}</h3>",
                        unsafe_allow_html=True)
        with col_3:
            st.image("assets/trophies/4-5-6-7_final.png", use_column_width=True)
            st.markdown(f"<h3 style='text-align: center;'>{div_3_won}</h3>",
                        unsafe_allow_html=True)
        with col_4:
            st.image("assets/trophies/8-9-10_final.png", use_column_width=True)
            st.markdown(f"<h3 style='text-align: center;'>{div_4_won}</h3>",
                        unsafe_allow_html=True)
