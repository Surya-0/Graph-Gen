import streamlit as st
from datetime import datetime, timedelta
import time
from .data_generator import DataGenerator
import pickle


def data_generator_page():
    st.header("Generate Supply Chain Data")

    # User inputs
    num_nodes = st.number_input("Number of nodes (minimum 26)", min_value=26, value=100)
    start_date = st.date_input("Start date", datetime(2024, 1, 1))
    end_date = st.date_input("End date", datetime(2024, 12, 31))
    interval_days = st.number_input("Interval (days)", min_value=1, value=7)

    if st.button("Generate Data"):
        with st.spinner("Generating data..."):
            start_time = time.time()

            # Adjust the number of modules and parts based on user input
            total_nodes = num_nodes
            num_modules = total_nodes // 3
            num_parts = total_nodes - num_modules - 26  # 26 is the minimum number of fixed nodes

            generator = DataGenerator(start_date, end_date, interval_days, num_modules, num_parts)
            generator.generate_data()
            data = generator.get_data()

            end_time = time.time()
            time_taken = end_time - start_time

            st.success(f"Data generated successfully in {time_taken:.2f} seconds!")

            # Save the generated data to session state
            st.session_state['generated_data'] = data

            # # Save the data to a file
            with open('generated_data.pkl', 'wb') as f:
                pickle.dump(data, f)
            #
            st.info("Data saved to 'generated_data.pkl'. You can now view the graph or export the data.")

    if 'generated_data' in st.session_state:
        st.write("Data has been generated. Navigate to 'Display Graph' or 'Export Data' to proceed.")