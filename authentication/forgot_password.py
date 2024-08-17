
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
# Creating a forgot password widget
try:
    (username_of_forgotten_password,
     email_of_forgotten_password,
     new_random_password) = authenticator.forgot_password()
    if username_of_forgotten_password:
        st.success('New password sent securely')
        # Random password to be transferred to the user securely
    elif not username_of_forgotten_password:
        st.error('Username not found')
except ForgotError as e:
    st.error(e)

# Saving config file
with open('config.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(config, file, default_flow_style=False)
