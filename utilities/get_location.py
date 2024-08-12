import pandas as pd
import streamlit as st


def extract_location_code(data: pd.core.frame.DataFrame):
    """
    This function would return all the unique locations
    """
    locations: list = []
    for _, entry in data.iterrows():
        temp = str(entry["Occurrence Location"])
        if 'between' in temp:
            temp = temp.split("between")
            temp = temp[1].strip().split(" ")
            temp = temp[0]+"-" + temp[2]
            if temp not in locations:
                locations.append(temp)
        else:
            temp = temp.split(" ")
            for i in temp:
                if (len(i) == 3 or len(i) == 4) and i.isupper() and i.isalpha():
                    if i not in locations:
                        locations.append(i)
    return locations


def extract_location_code_freq(data: pd.core.frame.DataFrame):
    """
    This function would return all the unique locations with frequency
    """
    locations = {}
    st.session_state.maxcase = 0
    st.session_state.caseAvg = 0
    for _, entry in data.iterrows():
        temp = str(entry["Occurrence Location"])
        if 'between' in temp:
            temp = temp.split("between")
            temp = temp[1].strip().split(" ")
            temp = temp[0]+"-" + temp[2]
            if temp not in locations:
                locations[temp] = 0
            locations[temp] += 1
        else:
            temp = temp.split(" ")
            for i in temp:
                if (len(i) == 3 or len(i) == 4) and i.isupper() and i.isalpha():
                    if i not in locations:
                        locations[i] = 0
                    locations[i] += 1
    summ = 0
    for _, value in locations.items():
        st.session_state.maxcase = max(st.session_state.maxcase, value)
        summ += value
    st.session_state.caseAvg = summ/len(locations)
    sd = 0
    for _, value in locations.items():
        sd += (value-st.session_state.caseAvg)**2
    sd /= len(locations)
    st.session_state.sd = sd
    return locations
