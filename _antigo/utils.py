import base64

import streamlit as st

from PATHS import NAVBAR_PATHS


def inject_custom_css():
    with open('assets/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def get_current_route():
    return st.query_params.get('nav')


def navbar_component():
    with open("assets/images/CDR.png", "rb") as image_file:
        cdr_png = base64.b64encode(image_file.read()).decode("utf-8")

    navbar_items = ''.join(
        f'<div class="navitem"><a class="navitem" href="/?nav={value}" target="_self">{key}</a></div>'
        for key, value in NAVBAR_PATHS.items()
    )

    component = f'''
            <nav class="container navbar" id="navbar">
                <img class="imgcdr" src="data:image/png;base64, {cdr_png}"/>
                <div class="navlist">
                {navbar_items}
                </div>
            </nav>
            '''
    st.markdown(component, unsafe_allow_html=True)
