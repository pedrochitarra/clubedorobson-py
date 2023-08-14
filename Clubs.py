"""Page containing the club information."""
import src.utils.club_info as utils_club
import src.components.club_info as components_club
import streamlit as st


# Set the page title and icon
st.set_page_config(page_title='Clube do Robson',
                   page_icon="assets/l99150901.png")

clubs = utils_club.get_all_clubs()
# Get CdR (our club), the row with clubId == 6703918
cdr = clubs[clubs["clubId"] == 6703918]
# Get the index of our club
cdr_index = int(cdr.index[0])

# List all clubs and start with CdR selected
selected_club = st.selectbox(
    "Select a club", clubs,
    format_func=lambda x: clubs[clubs["clubId"] == x]["name"].values[0],
    index=cdr_index)

# Create a Club object with the selected club
club = utils_club.get_club_info(selected_club)
# Get the seasons info
seasons = utils_club.get_seasons_info()
# Display the club's general info, such as kits, stadium, etc.
components_club.component_general_info(club)
components_club.component_kits(club)
# If it's our club, there's more information to show
if club.club_id == 6703918:
    # Aggregate the seasons info (wins, draws, losses)
    components_club.component_seasons(seasons)
    # Aggregate the goals info (goals scored, goals conceded)
    components_club.components_goals(seasons)
    # Aggregate the titles and general seasons info (promotions, relegations)
    components_club.component_grouped_seasons(seasons)
    # Aggregate the trophies info and display the trophies
    components_club.component_trophies(seasons)
    # Aggregate the last matches info and display the last matches
    last_matches = utils_club.get_club_last_matches(club.club_id)
    components_club.component_last_matches(last_matches)
