import streamlit as st

print("from lofout page="+str(st.session_state["authentication_status"]))
if st.session_state.authenticator.logout("Logout", "main"):
    st.session_state.priviledge = False
    st.rerun()
