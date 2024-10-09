import streamlit as st
import pandas as pd
import pickle
import os


def data_export_page():
    st.header("Export Supply Chain Data")

    # Load the generated data
    try:
        with open('generated_data.pkl', 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        st.error("No generated data found. Please generate data first.")
        return

    # Get available timestamps
    timestamps = list(data['time_series_data'].keys())

    # Let user select data to export
    st.subheader("Select data to export:")
    export_static = st.checkbox("Static Structure")
    export_dynamic = st.checkbox("Time Series Data")

    if export_dynamic:
        selected_timestamp = st.selectbox("Select a timestamp for time series data", timestamps)

    if st.button("Export Data"):
        with st.spinner("Exporting data..."):
            if export_static:
                export_static_data(data['static_structure'])
            if export_dynamic:
                export_dynamic_data(data['time_series_data'][selected_timestamp], selected_timestamp)

        st.success("Data exported successfully!")


def export_static_data(static_data):
    for key, items in static_data.items():
        if key == 'business_group':
            items = [items]
        df = pd.DataFrame(items)
        df.to_csv(f'{key}_static.csv', index=False)
        st.download_button(
            label=f"Download {key} static data",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=f'{key}_static.csv',
            mime='text/csv',
        )


def export_dynamic_data(time_data, timestamp):
    for key, items in time_data.items():
        if key == 'business_group':
            items = [items]
        df = pd.DataFrame(items)
        df.to_csv(f'{key}_{timestamp.strftime("%Y%m%d")}.csv', index=False)
        st.download_button(
            label=f"Download {key} data for {timestamp}",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=f'{key}_{timestamp.strftime("%Y%m%d")}.csv',
            mime='text/csv',
        )