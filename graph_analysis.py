import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter


def graph_analysis_page():
    st.title("Graph Analysis")

    if 'graph' not in st.session_state:
        st.warning("Please generate a graph first.")
        return

    G = st.session_state['graph']

    st.subheader("Graph Statistics")
    st.write(f"Number of nodes: {G.number_of_nodes()}")
    st.write(f"Number of edges: {G.number_of_edges()}")
    st.write(f"Average degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.2f}")

    st.subheader("Node Type Distribution")
    node_types = [data['group'] for _, data in G.nodes(data=True)]
    type_counts = Counter(node_types)
    fig, ax = plt.subplots()
    ax.bar(type_counts.keys(), type_counts.values())
    ax.set_xlabel("Node Type")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of Node Types")
    plt.xticks(rotation=45)
    st.pyplot(fig)