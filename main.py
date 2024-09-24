import streamlit as st
from graph_generation import graph_generation_page
from graph_analysis import graph_analysis_page
from graph_query import graph_query_page
from shortest_path import shortest_path_page


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Graph Generation", "Graph Analysis", "Graph Query", "Shortest Path"])

    if page == "Home":
        st.title("Graph Analysis App")
        st.write("Welcome to the Graph Analysis App. Use the sidebar to navigate between different functionalities.")
    elif page == "Graph Generation":
        graph_generation_page()
    elif page == "Graph Analysis":
        graph_analysis_page()
    elif page == "Graph Query":
        graph_query_page()
    elif page == "Shortest Path":
        shortest_path_page()


if __name__ == "__main__":
    main()

# constants.py
BUSINESS_GROUP = {'BG001': 'Etch'}
PRODUCT_FAMILIES = [
    {'Family_ID': 'PF001', 'Family_Name': 'Kyo'},
    {'Family_ID': 'PF002', 'Family_Name': 'Coronus'},
    {'Family_ID': 'PF003', 'Family_Name': 'Flex'},
    {'Family_ID': 'PF004', 'Family_Name': 'Versys Metal'}
]
PRODUCT_OFFERINGS = [
    {'Offering_ID': 'PO001', 'Offering_Name': 'Versys® Kyo®', 'Family_ID': 'PF001'},
    # ... (other product offerings)
]

COLOR_MAP = {
    'business_group': '#FF9999',
    'family': '#66B2FF',
    'offering': '#99FF99',
    'module': '#FFCC99',
    'make': '#FF99CC',
    'purchase': '#99CCFF'
}