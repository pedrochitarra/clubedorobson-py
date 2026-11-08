"""Clube do Robson — painel do clube de Pro Clubs. Rodar com: streamlit run app.py"""
import streamlit as st

from src import ui

st.set_page_config(page_title="Clube do Robson", page_icon="static/crests/99150901.png", layout="wide")
ui.inject_css()

st.logo("static/crests/99150901.png", size="large")

pages = [
    st.Page("paginas/clube.py", title="Clube", icon=":material/shield:", url_path="clube", default=True),
    st.Page("paginas/jogadores.py", title="Jogadores", icon=":material/groups:", url_path="jogadores"),
    st.Page("paginas/partidas.py", title="Partidas", icon=":material/sports_soccer:", url_path="partidas"),
]
nav = st.navigation(pages, position="top")

# Link direto no GitHub Pages: o index.html troca /clubedorobson-py/jogadores?x=1 por ?pagina=jogadores&x=1,
# porque o stlite não acha a página pelo caminho quando o site fica num subcaminho.
alvo = st.query_params.get("pagina")
if alvo:
    resto = {k: v for k, v in st.query_params.to_dict().items() if k != "pagina"}
    destino = next((p for p in pages if p.url_path == alvo), None)
    if destino:
        st.switch_page(destino, query_params=resto)
    st.query_params.from_dict(resto)

nav.run()

st.html("<p style='text-align:center;color:#a99cc0;font-size:.8rem;margin-top:40px'>"
        "Pro Clubs · FIFA 21 · dados até 24/02/2021</p>")
