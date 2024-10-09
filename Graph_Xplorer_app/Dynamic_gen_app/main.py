import streamlit as st
from datetime import datetime, timedelta
import time
from pages.data_generator_page import data_generator_page
from pages.graph_display_page import graph_display_page
from pages.data_export_page import data_export_page
from pages.graph_analysis_page import graph_analysis_page

st.set_page_config(page_title="Supply Chain Graph Generator", layout="wide")

def main():
    st.title("Supply Chain Graph Generator")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Generate Data", "Display Graph", "Graph Analysis", "Export Data"])

    if page == "Generate Data":
        data_generator_page()
    elif page == "Display Graph":
        graph_display_page()
    elif page == "Graph Analysis":
        graph_analysis_page()
    elif page == "Export Data":
        data_export_page()

if __name__ == "__main__":
    main()