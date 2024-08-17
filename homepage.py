import streamlit as st


from utilities.load_data import load_data

print("from homepage")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = None
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None
print("st.session_state.logged_in="+str(st.session_state.logged_in))
# if "data" not in st.session_state:
# st.session_state.data = load_data()

if "priviledge" not in st.session_state:
    st.session_state.priviledge = False


login_page = st.Page("authentication/login.py",
                     title="Log in", icon=":material/login:")
logout_page = st.Page("authentication/log_out.py",
                      title="Log out", icon=":material/logout:")
forgot_password = st.Page(
    "authentication/forgot_password.py", title="Forgot Password", icon=":material/logout:")
forgot_username = st.Page(
    "authentication/forgot_username.py", title="Forgot UserName", icon=":material/logout:")
register_user = st.Page("authentication/register.py",
                        title="Register New User")
upload_data = st.Page(
    "pages/upload_page.py", title="Upload Data")
section_vs_location = st.Page(
    "pages/section_vs_location.py", title="Section Vs Location")
trains_vs_section = st.Page(
    "pages/trains_vs_section.py", title="Train")
location_vs_section = st.Page(
    "pages/location_vs_section.py", title="Location")

st.sidebar.image("images/Logo.png", width=100)

if st.session_state["authentication_status"]:
    if st.session_state.priviledge:
        pg = st.navigation(
            {
                "Account": [logout_page, register_user],
                "Reports": [upload_data, section_vs_location, trains_vs_section, location_vs_section],
            }
        )
    else:
        pg = st.navigation(
            {
                "Account": [logout_page],
                "Reports": [upload_data, section_vs_location, trains_vs_section, location_vs_section],
            }
        )
else:
    pg = st.navigation([login_page, forgot_password, forgot_username])

pg.run()
