from io import BytesIO

from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px


import streamlit as st

import pandas as pd

from utilities.get_trains import get_trains

# Set your train here

if "data" not in st.session_state:
    st.warning("Please upload the relevant data first!")
else:
    data = st.session_state.data

    trains_dict = st.session_state.trains
    trains_list = list(trains_dict.keys())

    train_selection = st.selectbox("Select a train", trains_list)
    train: str = train_selection
    # Extract dates, times, and sections
    data_for_plot = []

    def can_proceed(locations, input_entry):
        if 'between' in input_entry:
            for loc in locations:
                if '-' in loc:
                    places = loc.split("-")
                    if places[0] in input_entry and places[1] in input_entry:
                        return True
        else:
            for loc in locations:
                if '-' not in loc and loc in input_entry:
                    return True
        return False

    def textwrap_html_style(input_text, max_width):
        """
        This function takes a string and inserts '<br>' tags after every max_width characters.

        Args:
        input_text: The string to be processed.
        max_width: The number of characters after which to insert '<br>'.

        Returns:
        The processed string with '<br>' tags inserted.
        """
        result = ""
        for i in range(0, len(input_text), max_width):
            result += input_text[i: i + max_width] + "<br>"
        return result[:-4]  # Remove the trailing '<br>'

    if train is not None:
        for index, entry in data.iterrows():
            if (train in str(entry["Occurrence Location"])):

                # str(entry["Occurrence Location"]).split(" ")[-1]
                section = str(entry["Sections"])
                details = f"Details: {textwrap_html_style(entry['Occurrence Details'],80)}<br>" \
                    f"Occurrence Location: {entry['Occurrence Location']}<br>" \
                    f"Occurrence Date & Time: {entry['Occurrence Date & Time']}<br>" \
                    f"Sections: {entry['Sections']}"  # Customize details as needed
                if "to" in entry["Occurrence Date & Time"]:

                    start, end = entry["Occurrence Date & Time"].split(" to ")
                    start_dt = datetime.strptime(start, "%d/%m/%Y %H:%M")
                    end_dt = datetime.strptime(end, "%d/%m/%Y %H:%M")
                    data_for_plot.extend([
                        {"Date": start_dt, "Section": section, "Details": details},
                        {"Date": end_dt, "Section": section, "Details": details}
                    ])
                else:

                    dt = datetime.strptime(
                        entry["Occurrence Date & Time"], "%d/%m/%Y %H:%M")
                    data_for_plot.append(
                        {"Date": dt, "Section": section, "Details": details})

        print(len(data_for_plot))
        # Create a DataFrame for easier plotting with Plotly
        df = pd.DataFrame(data_for_plot)

        # Create the interactive plot
        fig = go.Figure()

        # Add scatter trace for each train
        for section_name in df['Section']:
            df_section = df[df['Section'] == section_name]
            fig.add_trace(go.Scatter(
                x=df_section['Date'],
                y=df_section['Section'],
                mode='markers',
                name=section_name,
                marker=dict(size=10),
                hoverinfo='text',  # Display custom hover text
                hovertext=df_section['Details'],
                # Store details for click events
                customdata=df_section['Details']
            ))

        # Define click event handler
        fig.update_layout(
            title="Sections vs Date and Time for Train {}".format(train),
            xaxis_title="Date and Time",
            yaxis_title="Sections",
            hovermode='closest'
        )

        st.plotly_chart(fig)

        # Add a button to export the DataFrame as an Excel file
        @st.cache_data
        def to_excel(datadf):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                datadf.to_excel(excel_writer=writer,
                                index=False, sheet_name='Sheet1')
            processed_data = output.getvalue()
            return processed_data

        if st.button('Export to Excel'):
            excel_file = to_excel(df)
            st.download_button(
                label="Download Excel file",
                data=excel_file,
                file_name="dataframe.xlsx",
                mime="application/vnd.ms-excel"
            )
    else:
        st.write("Select a train")
