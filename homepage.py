import streamlit as st


from utilities.load_data import load_data


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

#if "data" not in st.session_state:
    #st.session_state.data = load_data()


def login():
    """
    For login
    """
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()


def logout():
    """
    For logout
    """
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()


login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

upload_data = st.Page(
    "pages/upload_page.py", title="Upload Data")
section_vs_location = st.Page(
    "pages/section_vs_location.py", title="Section Vs Location")
trains_vs_section = st.Page(
    "pages/trains_vs_section.py", title="Train")
location_vs_section = st.Page(
    "pages/location_vs_section.py", title="Location")

st.sidebar.image("images/Logo.png", width=100)

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Reports": [upload_data, section_vs_location, trains_vs_section, location_vs_section],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()
