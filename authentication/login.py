"""
Script description: This script imports tests the Streamlit-Authenticator package. 

Libraries imported:
- yaml: Module implementing the data serialization used for human readable documents.
- streamlit: Framework used to build pure Python web applications.
"""

import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import (CredentialsError,
                                               ForgotError,
                                               Hasher,
                                               LoginError,
                                               RegisterError,
                                               ResetError,
                                               UpdateError)
print("from login page")
# Loading config file
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Hashing all plain text passwords once
# Hasher.hash_passwords(config['credentials'])

# Creating the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

if "authenticator" not in st.session_state:
    st.session_state.authenticator = authenticator

# Creating a login widget
try:
    name, authentication_status, username = authenticator.login()
except LoginError as e:
    st.error(e)

if st.session_state["authentication_status"]:
    st.write(f'Welcome *{st.session_state["name"]}*')
    # authenticator.logout("Logout", "sidebar")
    if username == "nfrmain":
        st.session_state.priviledge = True
    else:
        st.session_state.priviledge = False
    st.rerun()
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
print(st.session_state["authentication_status"])
# Creating a password reset widget
if st.session_state["authentication_status"]:
    try:
        if authenticator.reset_password(st.session_state["username"]):
            st.success('Password modified successfully')
    except ResetError as e:
        st.error(e)
    except CredentialsError as e:
        st.error(e)


# Creating an update user details widget
if st.session_state["authentication_status"]:
    try:
        if authenticator.update_user_details(st.session_state["username"]):
            st.success('Entries updated successfully')
    except UpdateError as e:
        st.error(e)

# Saving config file
with open('config.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(config, file, default_flow_style=False)
