import pandas as pd
import streamlit as st
import pydeck as pdk
import numpy as np
from utilities.get_location import extract_location_code_for_given_section


def get_location_lat_long(data: pd.core.frame.DataFrame):
    '''
        This function would return dictionary of location and thier respective latitude and longitude

        returns:
        dict
    '''
    latlong: dict = {}
    for _, entry in data.iterrows():
        latitude = entry["Latitude"]
        if not pd.isna(latitude):
            latlong[entry["Station Code"]] = (
                entry["Latitude"], entry["Longitude"])
    return latlong


def calculate_radius(count):
    max_radius = 10000
    return min(max_radius, 2500 * np.log1p(count))


def calculate_elevation(count):
    max_elevation = 200
    return min(max_elevation, 50 * np.log1p(count))

# Function to safely convert coordinates


def safe_float_conversion(value):
    '''
        Safe Float Conversion: Added a safe_float_conversion function to handle both float and string types, stripping the BOM character if necessary.
    '''
    if isinstance(value, float):
        return value
    return float(value.strip('\ufeff'))


def calculate_color(count, caseavg):
    """
    This function works as follows:

        For ratio values less than 0.5, the color transitions from green to yellow.
        For ratio values greater than or equal to 0.5, the color transitions from yellow to red.
    """
    max_count = caseavg
    ratio = min(count / max_count, 1)

    if ratio < 0.5:
        # Transition from green to yellow
        green = int(255 * (1 - 2 * ratio))
        red = int(255 * (2 * ratio))
        return [red, green, 0, 160]
    else:
        # Transition from yellow to red
        red = 255
        green = int(255 * (1 - 2 * (ratio - 0.5)))
        return [red, green, 0, 160]


# @st.cache_data
def get_map_data(incident_counts: dict):
    """
        Inputs location and the frequency of the cases
        returns:
            hexlayer
            arclayer
    """
    station_coords = st.session_state.location_lat_long

    column_data = []

    for station, count in incident_counts.items():
        if '-' not in station:
            if station in station_coords:
                lat, lon = station_coords[station]
                column_data.append({
                    'coordinates': [lon, lat],
                    'count': count,
                    'elevation': calculate_elevation(count),
                    'station': station,
                    'color': calculate_color(count, st.session_state.caseAvg)
                })
            # Create ColumnLayer
    column_layer = pdk.Layer(
        'ColumnLayer',
        data=column_data,
        get_position='coordinates',
        get_elevation='elevation',
        elevation_scale=100,
        radius=1000,
        get_fill_color='color',
        pickable=True,
        extruded=True,
        auto_highlight=True,
    )

    hex_data = []
    for station, count in incident_counts.items():
        if '-' not in station:
            if station in station_coords:
                lat, lon = station_coords[station]
                hex_data.append({"lat": lat,
                                 "lon": lon,
                                 'count': count,
                                 'station': station})
                # hex_data.append([lon, lat, count])
        else:
            station = station.split('-')
            if station[0] in station_coords:
                lat, lon = station_coords[station[0]]
                hex_data.append({"lat": lat,
                                 "lon": lon,
                                 'count': count,
                                 'station': station[0]})
            if station[1] in station_coords:
                lat, lon = station_coords[station[1]]
                hex_data.append({"lat": lat,
                                 "lon": lon,
                                 'count': count,
                                 'station': station[1]})

    arc_data = []

    for route, count in incident_counts.items():
        if '-' in route:
            start, end = route.split('-')
            if (start in station_coords) and (end in station_coords):
                start_lat, start_lon = map(
                    safe_float_conversion, station_coords[start])
                end_lat, end_lon = map(
                    safe_float_conversion, station_coords[end])
                mid_lat = (start_lat + end_lat) / 2
                mid_lon = (start_lon + end_lon) / 2

                arc_data.append({
                    'start': [start_lon, start_lat],
                    'end': [end_lon, end_lat],
                    'count': count,
                    'route': route,
                    'midpoint': [mid_lon, mid_lat]
                })

    hex_layer = pdk.Layer(
        'HexagonLayer',
        data=hex_data,
        get_position=["lon", "lat"],
        get_elevation=2,
        radius=10000,
        elevation_scale=50,
        elevation_range=[0, 3000],
        pickable=True,
        extruded=True,
    )
    arc_layer = pdk.Layer(
        'ArcLayer',
        data=arc_data,
        get_source_position='start',
        get_target_position='end',
        get_source_color=[255, 0, 0, 160],
        get_target_color=[0, 0, 255, 160],
        auto_highlight=True,
        width_scale=0.3,
        get_width='count',
    )
    text_layer_arcs = pdk.Layer(
        'TextLayer',
        data=arc_data,
        get_position='midpoint',
        get_text='route',
        get_size=16,
        get_color=[0, 0, 0],
        get_angle=0,
        get_text_anchor='middle',
        get_alignment_baseline='center'
    )
    scatter_data = []

    for station, count in incident_counts.items():
        if '-' not in station:
            if station in station_coords:
                lat, lon = station_coords[station]
                scatter_data.append({
                    'coordinates': [lon, lat],
                    'count': count,
                    'station': station,
                    'radius': calculate_radius(count),
                    'color': calculate_color(count, st.session_state.caseAvg)
                })
        else:
            station = station.split('-')
            if station[0] in station_coords:
                lat, lon = station_coords[station[0]]
                scatter_data.append({
                    'coordinates': [lon, lat],
                    'count': count,
                    'station': station[0],
                    'radius': calculate_radius(count),
                    'color': calculate_color(count, st.session_state.caseAvg)
                })
            if station[1] in station_coords:
                lat, lon = station_coords[station[1]]
                scatter_data.append({
                    'coordinates': [lon, lat],
                    'count': count,
                    'station': station[1],
                    'radius': calculate_radius(count),
                    'color': calculate_color(count, st.session_state.caseAvg)
                })

    scatter_layer = pdk.Layer(
        'ScatterplotLayer',
        data=scatter_data,
        get_position='coordinates',
        get_radius='radius',
        get_fill_color='color',
        pickable=True,
    )
    text_layer = pdk.Layer(
        'TextLayer',
        data=column_data,
        get_position='coordinates',
        get_text='station',
        get_size=2000,
        get_color=[0, 0, 0],
        get_angle=0,
        get_text_anchor='middle',
        get_alignment_baseline='center'
    )


# Set the viewport location
    return hex_layer, arc_layer, scatter_layer, text_layer, column_layer, text_layer_arcs


def get_map_data_for_section(data: pd.core.frame.DataFrame, section: str):
    """
        Inputs location and the frequency of the cases
        returns:
            hexlayer
            arclayer
    """
    incident_counts, _, caseAvg, _ = extract_location_code_for_given_section(
        data, section)
    station_coords = st.session_state.location_lat_long

    column_data = []

    for station, count in incident_counts.items():
        if '-' not in station:
            if station in station_coords:
                lat, lon = station_coords[station]
                column_data.append({
                    'coordinates': [lon, lat],
                    'count': count,
                    'elevation': calculate_elevation(count),
                    'station': station,
                    'color': calculate_color(count, caseAvg)
                })
            # Create ColumnLayer
    column_layer = pdk.Layer(
        'ColumnLayer',
        data=column_data,
        get_position='coordinates',
        get_elevation='elevation',
        elevation_scale=100,
        radius=1000,
        get_fill_color='color',
        pickable=True,
        extruded=True,
        auto_highlight=True,
    )

    hex_data = []
    for station, count in incident_counts.items():
        if '-' not in station:
            if station in station_coords:
                lat, lon = station_coords[station]
                hex_data.append({"lat": lat,
                                 "lon": lon,
                                 'count': count,
                                 'station': station})
                # hex_data.append([lon, lat, count])
        else:
            station = station.split('-')
            if station[0] in station_coords:
                lat, lon = station_coords[station[0]]
                hex_data.append({"lat": lat,
                                 "lon": lon,
                                 'count': count,
                                 'station': station[0]})
            if station[1] in station_coords:
                lat, lon = station_coords[station[1]]
                hex_data.append({"lat": lat,
                                 "lon": lon,
                                 'count': count,
                                 'station': station[1]})

    arc_data = []

    for route, count in incident_counts.items():
        if '-' in route:
            start, end = route.split('-')
            if (start in station_coords) and (end in station_coords):
                start_lat, start_lon = map(
                    safe_float_conversion, station_coords[start])
                end_lat, end_lon = map(
                    safe_float_conversion, station_coords[end])
                mid_lat = (start_lat + end_lat) / 2
                mid_lon = (start_lon + end_lon) / 2

                arc_data.append({
                    'start': [start_lon, start_lat],
                    'end': [end_lon, end_lat],
                    'count': count,
                    'route': route,
                    'midpoint': [mid_lon, mid_lat]
                })

    hex_layer = pdk.Layer(
        'HexagonLayer',
        data=hex_data,
        get_position=["lon", "lat"],
        get_elevation=2,
        radius=10000,
        elevation_scale=50,
        elevation_range=[0, 3000],
        pickable=True,
        extruded=True,
    )
    arc_layer = pdk.Layer(
        'ArcLayer',
        data=arc_data,
        get_source_position='start',
        get_target_position='end',
        get_source_color=[255, 0, 0, 160],
        get_target_color=[0, 0, 255, 160],
        auto_highlight=True,
        width_scale=0.3,
        get_width='count',
    )
    text_layer_arcs = pdk.Layer(
        'TextLayer',
        data=arc_data,
        get_position='midpoint',
        get_text='route',
        get_size=16,
        get_color=[0, 0, 0],
        get_angle=0,
        get_text_anchor='middle',
        get_alignment_baseline='center'
    )
    scatter_data = []

    for station, count in incident_counts.items():
        if '-' not in station:
            if station in station_coords:
                lat, lon = station_coords[station]
                scatter_data.append({
                    'coordinates': [lon, lat],
                    'count': count,
                    'station': station,
                    'radius': calculate_radius(count),
                    'color': calculate_color(count, caseAvg)
                })
        else:
            station = station.split('-')
            if station[0] in station_coords:
                lat, lon = station_coords[station[0]]
                scatter_data.append({
                    'coordinates': [lon, lat],
                    'count': count,
                    'station': station[0],
                    'radius': calculate_radius(count),
                    'color': calculate_color(count, caseAvg)
                })
            if station[1] in station_coords:
                lat, lon = station_coords[station[1]]
                scatter_data.append({
                    'coordinates': [lon, lat],
                    'count': count,
                    'station': station[1],
                    'radius': calculate_radius(count),
                    'color': calculate_color(count, caseAvg)
                })

    scatter_layer = pdk.Layer(
        'ScatterplotLayer',
        data=scatter_data,
        get_position='coordinates',
        get_radius='radius',
        get_fill_color='color',
        pickable=True,
    )
    text_layer = pdk.Layer(
        'TextLayer',
        data=column_data,
        get_position='coordinates',
        get_text='station',
        get_size=2000,
        get_color=[0, 0, 0],
        get_angle=0,
        get_text_anchor='middle',
        get_alignment_baseline='center'
    )


# Set the viewport location
    return hex_layer, arc_layer, scatter_layer, text_layer, column_layer, text_layer_arcs
