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
        st.write("""
        ### Welcome to the Graph Generation App

        This app creates **dynamic supply chain graphs** using advanced **random generation techniques**. Here’s how the process works:

        #### Node Creation and Structure
        - We start with a **base of 26 nodes**, including one **Business Group**, multiple **Product Families**, and their associated **Product Offerings**.
        - From there,we can add how many ever nodes we want based on our requirement by entering into the **user input** placeholder.

        #### Randomized Node and Link Generation
        Our unique graph generation process employs **two key randomization steps**:

        1. **Density Factor Influence**:
           - Each **Product Offering** is assigned a **Density Factor** (a value between 0 and 1) that determines the likelihood of forming a **link**. A higher density factor means more connections, while a lower density factor limits links.
           - This first randomization ensures that the structure of the graph is unique and adaptive to each node.

        2. **Poisson/Normal Distribution**:
           - Once the possibility of a link is determined, the number of **Modules** and **Parts** linked to each **Product Offering** is calculated using **Poisson** or **Normal distribution**. This adds an element of **natural randomness** in the number of nodes generated, mimicking real-world supply chain dynamics.
           - The **Density Factor** also governs the number of connections added. High-density offerings receive more links, while low-density offerings generate fewer.

        Through this process, the graph grows organically, reflecting realistic and varied supply chain relationships. 🎯

        Please start exploring and generating your own **supply chain network** now!!
        """)

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
