
import plotly.express as px
import streamlit as st
from utilities.get_location import extract_location_code, extract_location_code_freq
from utilities.map_utilities import get_location_lat_long, get_map_data
from utilities.get_trains import get_trains
from utilities.get_section import get_section
import pandas as pd
import pydeck as pdk
st.title("Upload Railway Act Data")

if "location_lat_long" not in st.session_state:
    latlong = pd.read_excel("data/station_data.xlsx")
    st.session_state.location_lat_long = get_location_lat_long(latlong)


upload_form = st.form("upload_form", clear_on_submit=True, border=True)
uploaded_file = upload_form.file_uploader(
    "Please submit a excel file (.xls) containing the data to be analyzed here:", type=['xls'])
submit = upload_form.form_submit_button("Submit")

if submit:
    if uploaded_file:
        data = pd.read_excel(uploaded_file, sheet_name=None)
        data = pd.concat(data.values(), ignore_index=True)
        st.session_state.data = data

    else:
        st.warning("Please upload the relevant data!")

if "data" in st.session_state:
    data = st.session_state.data
    st.write(data)
    location_list = extract_location_code(data)
    st.session_state.location_list = location_list
    st.session_state.trains = get_trains(data)
    st.session_state.sections = get_section(data)
    st.title("Map of Places")
    casecount = extract_location_code_freq(data)
    hex_layer, arc_layer, scatter_layer, text_layer, column_layer, text_layer_arcs = get_map_data(
        casecount)
    # Set the viewport location
    view_state = pdk.ViewState(
        longitude=91.123,
        latitude=26.123,
        zoom=5,
        pitch=50,
    )
    # Render the map
    r = pdk.Deck(
        layers=[column_layer, arc_layer,
                scatter_layer],
        initial_view_state=view_state,
        tooltip={"text": "{station}: {count} incidents"},
        map_style='mapbox://styles/mapbox/light-v10'
    )
    st.pydeck_chart(r)

    st.success("The data has been uploaded successfully!!")
