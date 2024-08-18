import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import (CredentialsError,
                                               ForgotError,
                                               Hasher,
                                               LoginError,
                                               RegisterError,
                                               ResetError,
                                               UpdateError)

config = st.session_state.config
authenticator = st.session_state.authenticator

print("from lofout page="+str(st.session_state["authentication_status"]))

st.title("Hi "+str(st.session_state["username"])+"!")
# Creating an update user details widget
if st.session_state["authentication_status"]:
    try:
        if authenticator.update_user_details(st.session_state["username"], key='update_user_details_form'):
            st.success('Entries updated successfully')
    except UpdateError as e:
        st.error(e)
# Creating a password reset widget
if st.session_state["authentication_status"]:
    try:
        if authenticator.reset_password(st.session_state["username"], key='reset_password_form'):
            st.success('Password modified successfully')
    except ResetError as e:
        st.error(e)
    except CredentialsError as e:
        st.error(e)
# Saving config file
with open('config.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(config, file, default_flow_style=False)

if st.session_state.authenticator.logout("Logout", "main"):
    st.session_state.priviledge = False
    st.rerun()
