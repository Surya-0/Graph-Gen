# import streamlit as st
# import pandas as pd
# import pickle
# import os
#
#
# def data_export_page():
#     st.header("Export Supply Chain Data")
#
#     # Load the generated data
#     try:
#         with open('generated_data.pkl', 'rb') as f:
#             data = pickle.load(f)
#     except FileNotFoundError:
#         st.error("No generated data found. Please generate data first.")
#         return
#
#     # Get available timestamps
#     timestamps = list(data['time_series_data'].keys())
#
#     # Let user select data to export
#     st.subheader("Select data to export:")
#     export_static = st.checkbox("Static Structure")
#     export_dynamic = st.checkbox("Time Series Data")
#
#     if export_dynamic:
#         selected_timestamp = st.selectbox("Select a timestamp for time series data", timestamps)
#
#     if st.button("Export Data"):
#         with st.spinner("Exporting data..."):
#             if export_static:
#                 export_static_data(data['static_structure'])
#             if export_dynamic:
#                 export_dynamic_data(data['time_series_data'][selected_timestamp], selected_timestamp)
#
#         st.success("Data exported successfully!")
#
#
# def export_static_data(static_data):
#     for key, items in static_data.items():
#         if key == 'business_group':
#             items = [items]
#         df = pd.DataFrame(items)
#         df.to_csv(f'{key}_static.csv', index=False)
#         st.download_button(
#             label=f"Download {key} static data",
#             data=df.to_csv(index=False).encode('utf-8'),
#             file_name=f'{key}_static.csv',
#             mime='text/csv',
#         )
#
#
# def export_dynamic_data(time_data, timestamp):
#     for key, items in time_data.items():
#         if key == 'business_group':
#             items = [items]
#         df = pd.DataFrame(items)
#         df.to_csv(f'{key}_{timestamp.strftime("%Y%m%d")}.csv', index=False)
#         st.download_button(
#             label=f"Download {key} data for {timestamp}",
#             data=df.to_csv(index=False).encode('utf-8'),
#             file_name=f'{key}_{timestamp.strftime("%Y%m%d")}.csv',
#             mime='text/csv',
#         )


import streamlit as st
import pandas as pd
import pickle
import os
import zipfile
from io import BytesIO

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
            temp_dir = "temp_export"
            os.makedirs(temp_dir, exist_ok=True)
            files_to_zip = []

            if export_static:
                files_to_zip.extend(export_static_data(data['static_structure'], temp_dir))
            if export_dynamic:
                files_to_zip.extend(export_dynamic_data(data['time_series_data'][selected_timestamp], selected_timestamp, temp_dir))

            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for file_path in files_to_zip:
                    zip_file.write(file_path, os.path.basename(file_path))

            zip_buffer.seek(0)
            st.download_button(
                label="Download Exported Data",
                data=zip_buffer,
                file_name="exported_data.zip",
                mime="application/zip"
            )

            # Clean up temporary files
            for file_path in files_to_zip:
                os.remove(file_path)
            os.rmdir(temp_dir)

        st.success("Data exported successfully!")

def export_static_data(static_data, temp_dir):
    files = []
    for key, items in static_data.items():
        if key == 'business_group':
            items = [items]
        df = pd.DataFrame(items)
        file_path = os.path.join(temp_dir, f'{key}_static.csv')
        df.to_csv(file_path, index=False)
        files.append(file_path)
    return files

def export_dynamic_data(time_data, timestamp, temp_dir):
    files = []
    for key, items in time_data.items():
        if key == 'business_group':
            items = [items]
        df = pd.DataFrame(items)
        file_path = os.path.join(temp_dir, f'{key}_{timestamp.strftime("%Y%m%d")}.csv')
        df.to_csv(file_path, index=False)
        files.append(file_path)
    return files