import streamlit as st

import utils as utl
from views import clube, configuration, jogadores, options, partidas

st.set_page_config(layout="wide", page_title='Clube do Robson')
utl.inject_custom_css()
utl.navbar_component()

ROUTES = {
    "clube": clube,
    "jogadores": jogadores,
    "partidas": partidas,
    "options": options,
    "configuration": configuration,
}


def navigation():
    route = utl.get_current_route()
    ROUTES.get(route, clube).load_view()


navigation()
