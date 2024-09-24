import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import random


def visualize_shortest_path(G, node1, node2):
    try:
        path = nx.shortest_path(G, source=node1, target=node2)
        st.success(f"Shortest path from {node1} to {node2}: {' -> '.join(path)}")

        # Create the subgraph containing only the nodes in the shortest path
        subgraph_nodes = set(path)
        subgraph = G.subgraph(subgraph_nodes)

        pos = nx.spring_layout(subgraph, k=0.5, iterations=50)

        edge_x, edge_y = [], []
        for edge in subgraph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='red'),
            hoverinfo='none',
            mode='lines'
        )

        node_x, node_y = [], []
        for node in subgraph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='Viridis',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2
            )
        )

        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(subgraph.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append(
                f"Node: {subgraph.nodes[adjacencies[0]]['label']}<br># of connections: {len(adjacencies[1])}")

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text

        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title=f'Shortest Path from {node1} to {node2}',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                annotations=[dict(
                    text="",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002
                )],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
        )
        st.plotly_chart(fig)

    except nx.NetworkXNoPath:
        st.error(f"No path exists between {node1} and {node2}")
    except nx.NodeNotFound as e:
        st.error(f"Node not found: {str(e)}")


def shortest_path_page():
    st.title("Shortest Path Visualization")

    if 'graph' not in st.session_state:
        st.warning("Please generate a graph first in the 'Graph Generation' page.")
        return

    G = st.session_state['graph']

    st.write("This page allows you to visualize the shortest path between two nodes in the graph.")

    col1, col2 = st.columns(2)

    with col1:
        node1 = st.text_input("Enter the first node ID:", key="node1_input")

    with col2:
        node2 = st.text_input("Enter the second node ID:", key="node2_input")

    if st.button("Visualize Shortest Path"):
        if not node1 or not node2:
            st.error("Please enter both node IDs.")
        elif node1 == node2:
            st.error("Please enter two different node IDs.")
        else:
            visualize_shortest_path(G, node1, node2)

    st.write("---")
    st.subheader("Node Information")
    st.write("Here's a list of some nodes in the graph for reference:")

    # Display a sample of nodes from different groups
    sample_nodes = []
    for group in ['business_group', 'family', 'offering', 'module', 'make', 'purchase']:
        nodes = [node for node, data in G.nodes(data=True) if data.get('group') == group]
        sample_nodes.extend(random.sample(nodes, min(5, len(nodes))))

    for node in sample_nodes:
        st.write(f"- Node ID: {node}, Label: {G.nodes[node]['label']}, Group: {G.nodes[node]['group']}")

    st.write("Note: This is just a sample. Your graph may contain many more nodes.")