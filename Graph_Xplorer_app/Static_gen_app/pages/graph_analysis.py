# pages/graph_analysis.py

import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from .graph_analyzer import analyze_graph
from .performance_utils import measure_performance, format_performance_metrics

@measure_performance
def run_analysis(G):
    return analyze_graph(G)

def plot_degree_distribution(in_degree_dist, out_degree_dist):
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=in_degree_dist, name='In-degree', marker_color='#F63366'))
    fig.add_trace(go.Histogram(x=out_degree_dist, name='Out-degree', marker_color='#6ED0F6'))
    fig.update_layout(
        title='Degree Distribution',
        xaxis_title='Degree',
        yaxis_title='Frequency',
        barmode='overlay',
        bargap=0.1,
        bargroupgap=0.2
    )
    return fig

def show():
    st.title("Graph Analysis")

    if 'graph' not in st.session_state:
        st.warning("Please generate a graph first.")
        return

    G = st.session_state['graph']

    if st.button("Run Analysis"):
        with st.spinner("Analyzing graph..."):
            analysis, performance_metrics = run_analysis(G)

        st.success("Analysis complete!")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Basic Statistics")
            st.write(f"Number of nodes: {analysis['num_nodes']}")
            st.write(f"Number of edges: {analysis['num_edges']}")

            st.subheader("Node Types")
            for node_type, count in analysis['node_types'].items():
                st.write(f"{node_type}: {count}")

        with col2:
            st.subheader("Connectivity Analysis")
            st.write(f"Is the graph strongly connected? {analysis['is_strongly_connected']}")
            st.write(f"Number of strongly connected components: {analysis['num_strongly_connected_components']}")

            if 'avg_shortest_path_length' in analysis:
                st.write(f"Average shortest path length: {analysis['avg_shortest_path_length']:.4f}")
            else:
                st.write(f"Average shortest path length in the largest strongly connected component: {analysis['avg_shortest_path_length_largest_scc']:.4f}")

        st.subheader("Degree Distribution")
        fig = plot_degree_distribution(analysis['in_degree_dist'], analysis['out_degree_dist'])
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Centrality Measures"):
            st.write("Top 5 nodes by degree centrality:")
            for node, centrality in analysis['top_degree_centrality']:
                st.write(f"{node}: {centrality:.4f}")

            st.write("Top 5 nodes by betweenness centrality:")
            for node, centrality in analysis['top_betweenness_centrality']:
                st.write(f"{node}: {centrality:.4f}")

        with st.expander("Community Detection"):
            st.write(f"Number of communities detected: {analysis['num_communities']}")
            st.write(f"Modularity: {analysis['modularity']:.4f}")

        st.subheader("Performance Metrics")
        st.text(format_performance_metrics(performance_metrics))

        with st.expander("Metrics Explanation"):
            st.info(get_metrics_explanation())

def get_metrics_explanation():
    return """
    Explanation of metrics:
    - Execution Time: The total time taken to complete the operation, measured in seconds.
    - Memory Used: The additional memory consumed during the operation, measured in megabytes (MB).
    - Peak Memory: The maximum amount of memory used at any point during the operation, measured in megabytes (MB).
    """