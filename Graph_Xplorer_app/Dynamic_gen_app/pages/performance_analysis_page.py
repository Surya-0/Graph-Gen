import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
from .data_generator import DataGenerator
from datetime import datetime, timedelta


def performance_analysis_page():
    st.header("Performance Analysis: Graph Generation Time")

    # User inputs
    start_nodes = st.number_input("Start number of nodes", min_value=26, value=50)
    end_nodes = st.number_input("End number of nodes", min_value=start_nodes, value=500)
    step = st.number_input("Step size", min_value=1, value=50)

    if st.button("Run Performance Analysis"):
        with st.spinner("Analyzing performance..."):
            nodes = list(range(start_nodes, end_nodes + 1, step))
            times = []

            # Fixed parameters for consistency
            start_date = datetime(2024, 1, 1)
            end_date = datetime(2024, 12, 31)
            interval_days = 7

            for n in nodes:
                num_modules = n // 3
                num_parts = n - num_modules - 26

                start_time = time.time()
                generator = DataGenerator(start_date, end_date, interval_days, num_modules, num_parts)
                generator.generate_data()
                end_time = time.time()

                times.append(end_time - start_time)

            # Create and display the plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(nodes, times, marker='o')
            ax.set_xlabel('Number of Nodes')
            ax.set_ylabel('Generation Time (seconds)')
            ax.set_title('Graph Generation Time vs Number of Nodes')
            ax.grid(True)

            st.pyplot(fig)

            # Display data in a table
            df = pd.DataFrame({'Nodes': nodes, 'Time (seconds)': times})
            st.dataframe(df)

            # Calculate and display growth rate
            growth_rate = (times[-1] - times[0]) / (nodes[-1] - nodes[0])
            st.write(f"Average growth rate: {growth_rate:.4f} seconds per node")