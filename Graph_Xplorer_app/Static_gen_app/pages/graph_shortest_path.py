import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from .performance_utils import measure_performance, format_performance_metrics, get_metrics_explanation

@measure_performance
def find_shortest_path(G, start_node, end_node):
    if start_node not in G.nodes or end_node not in G.nodes:
        st.error(f"One or both nodes ({start_node}, {end_node}) do not exist in the graph.")
        return None

    try:
        path = nx.shortest_path(G, start_node, end_node)
        return path
    except nx.NetworkXNoPath:
        st.error(f"No path exists between {start_node} and {end_node}")
        return None

def visualize_path(G, path):
    if not path:
        return None

    subgraph = G.subgraph(path)
    pos = nx.spring_layout(subgraph, k=0.5, iterations=50)

    edge_x, edge_y = [], []
    for edge in subgraph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=2, color='#888'), hoverinfo='none', mode='lines')

    node_x, node_y = [], []
    for node in subgraph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text', hoverinfo='text', textposition='top center',
        marker=dict(size=15, color='#1f77b4', line=dict(width=2)),
        text=[f"{node}" for node in subgraph.nodes()]
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Shortest Path',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(text="", showarrow=False, xref="paper", yref="paper", x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    )
                    )
    return fig

def show():
    st.title("Shortest Path Query")

    if 'graph' not in st.session_state:
        st.warning("Please generate a graph first.")
        return

    G = st.session_state['graph']

    col1, col2 = st.columns(2)
    with col1:
        start_node = st.text_input("Enter the start node ID:")
    with col2:
        end_node = st.text_input("Enter the end node ID:")

    if st.button("Find Shortest Path"):
        if start_node in G.nodes and end_node in G.nodes:
            path, performance_metrics = find_shortest_path(G, start_node, end_node)
            if path:
                st.success(f"Shortest path found: {' -> '.join(path)}")
                fig = visualize_path(G, path)
                if fig:
                    st.plotly_chart(fig)

                st.subheader("Performance Metrics")
                st.text(format_performance_metrics(performance_metrics))
        else:
            st.error("One or both nodes not found in the graph.")

    st.info(get_metrics_explanation())