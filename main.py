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

