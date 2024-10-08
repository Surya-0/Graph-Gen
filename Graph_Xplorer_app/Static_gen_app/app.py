import streamlit as st
from pages import graph_generation, graph_analysis, graph_subgraph, graph_shortest_path

PAGES = {
    "Home": "home",
    "Graph Generation": graph_generation,
    "Graph Analysis": graph_analysis,
    "Subgraph Query": graph_subgraph,
    "Shortest Path Query": graph_shortest_path
}

def home():
    st.title("Supply Chain Network Analysis")
    st.write("""
    Welcome to the Supply Chain Network Analysis application!

    This tool allows you to generate, analyze, and query supply chain network graphs.
    Use the navigation menu on the left to explore different functionalities.

    - **Graph Generation**: Create a new supply chain network graph.
    - **Graph Analysis**: Analyze the properties of the generated graph.
    - **Subgraph Query**: Explore specific nodes and their connections in the graph.
    - **Shortest Path Query**: Find the shortest path between two nodes in the graph.

    Get started by selecting 'Graph Generation' from the menu.
    """)

def main():
    st.set_page_config(page_title="Supply Chain Network Analysis", page_icon="🌐", layout="wide")

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    if selection == "Home":
        home()
    else:
        PAGES[selection].show()

    st.sidebar.markdown("---")

if __name__ == "__main__":
    main()