from io import BytesIO
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from utilities.get_location import extract_location_code
import pandas as pd
st.header("Upload Railway Act Data")

upload_form = st.form("upload_form", clear_on_submit=True, border=True)
uploaded_file = upload_form.file_uploader("Please submit a excel file (.xls) containing the data to be analyzed here:", type=['xls'])
submit = upload_form.form_submit_button("Submit")

if submit:
    if uploaded_file:
        data= pd.read_excel(uploaded_file)
        st.write(data)
        location_list = extract_location_code(data)
        st.write(location_list)
        # Sample data: list of places with their coordinates
        data = {
            "Place": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
            "Latitude": [40.7128, 34.0522, 41.8781, 29.7604, 33.4484],
            "Longitude": [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740],
        }

        # Convert data to a DataFrame
        df = pd.DataFrame(data)

        # Create a Plotly map
        fig = px.scatter_mapbox(
            df,
            lat="Latitude",
            lon="Longitude",
            hover_name="Place",
            zoom=3,
            height=600,
        )

        # Set mapbox style
        fig.update_layout(mapbox_style="open-street-map")

        # Hide the legend and margins
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

        # Display the map in Streamlit
        st.title("Map of Places")
        st.plotly_chart(fig)

        st.session_state.data = data
        st.success("The data has been uploaded successfully!!")
    else:
        st.warning("Please upload the relevant data!")