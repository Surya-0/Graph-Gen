import streamlit as st
import networkx as nx
import plotly.graph_objs as go
import pickle

def graph_analysis_page():
    st.header("Graph Analysis and Querying")

    # Load the generated data
    try:
        with open('generated_data.pkl', 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        st.error("No generated data found. Please generate data first.")
        return

    # Get available timestamps
    timestamps = list(data['time_series_data'].keys())

    # Let user select a timestamp
    selected_timestamp = st.selectbox("Select a timestamp", timestamps)

    G = create_graph(data, selected_timestamp)

    st.subheader("Graph Analysis Options")
    analysis_option = st.radio("Choose an analysis option:",
                               ["Subgraph Visualization", "Shortest Path", "Centrality Measures"])

    if analysis_option == "Subgraph Visualization":
        subgraph_visualization(G)
    elif analysis_option == "Shortest Path":
        shortest_path_visualization(G)
    elif analysis_option == "Centrality Measures":
        centrality_measures(G)

def subgraph_visualization(G):
    st.write("Visualize a subgraph based on a selected node")
    node_id = st.selectbox("Select a node", list(G.nodes()))
    levels = st.slider("Select the number of levels to explore:", min_value=1, max_value=5, value=2)

    if st.button("Visualize Subgraph"):
        fig = query_subgraph(G, node_id, levels)
        st.plotly_chart(fig, use_container_width=True)

def query_subgraph(G, node_id, levels=2):
    if node_id not in G.nodes:
        st.error(f"Node {node_id} does not exist in the graph.")
        return None

    subgraph_nodes = {node_id}
    current_level_nodes = {node_id}

    for _ in range(levels):
        next_level_nodes = set()
        for node in current_level_nodes:
            next_level_nodes.update(G.neighbors(node))
        subgraph_nodes.update(next_level_nodes)
        current_level_nodes = next_level_nodes

    subgraph = G.subgraph(subgraph_nodes)

    pos = nx.spring_layout(subgraph, k=0.5, iterations=50)

    edge_x, edge_y = [], []
    for edge in subgraph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')

    node_x, node_y = [], []
    for node in subgraph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers', hoverinfo='text',
        marker=dict(
            showscale=True, colorscale='YlGnBu', reversescale=True, color=[], size=10,
            colorbar=dict(thickness=15, title='Node Connections', xanchor='left', titleside='right'),
            line_width=2
        )
    )

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(subgraph.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(f"Node: {subgraph.nodes[adjacencies[0]]['id']}<br>Type: {subgraph.nodes[adjacencies[0]]['node_type']}<br># of connections: {len(adjacencies[1])}")

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=f'Subgraph for node: {node_id} (Levels: {levels})',
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

def shortest_path_visualization(G):
    st.write("Find and visualize the shortest path between two nodes")

    nodes = list(G.nodes())
    source = st.selectbox("Select source node", nodes)
    target = st.selectbox("Select target node", nodes)

    if st.button("Find Shortest Path"):
        try:
            path = nx.shortest_path(G, source, target)
            st.success(f"Shortest path: {' -> '.join(path)}")

            path_edges = list(zip(path, path[1:]))
            subgraph = G.subgraph(path)

            fig = plot_graph(G, highlight_path=path)
            st.plotly_chart(fig, use_container_width=True)
        except nx.NetworkXNoPath:
            st.error("No path exists between the selected nodes.")

def centrality_measures(G):
    st.write("Calculate and visualize centrality measures")

    centrality_option = st.selectbox("Choose a centrality measure",
                                     ["Degree Centrality", "Betweenness Centrality", "Closeness Centrality"])

    if centrality_option == "Degree Centrality":
        centrality = nx.degree_centrality(G)
    elif centrality_option == "Betweenness Centrality":
        centrality = nx.betweenness_centrality(G)
    elif centrality_option == "Closeness Centrality":
        centrality = nx.closeness_centrality(G)

    nx.set_node_attributes(G, centrality, 'centrality')

    fig = plot_graph(G, color_by='centrality')
    st.plotly_chart(fig, use_container_width=True)

    st.write("Top 10 nodes by centrality measure:")
    top_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    for node, score in top_nodes:
        st.write(f"{node}: {score:.4f}")

def create_graph(data, timestamp):
    G = nx.DiGraph()

    for node_type in ['business_group', 'product_families', 'product_offerings', 'modules', 'parts']:
        if node_type == 'business_group':
            node_data = [data['time_series_data'][timestamp][node_type]]
        else:
            node_data = data['time_series_data'][timestamp][node_type]

        for node in node_data:
            G.add_node(node['id'], **node, node_type=node_type)

    for edge in data['time_series_data'][timestamp]['edges']:
        G.add_edge(edge['source_id'], edge['target_id'], **edge)

    return G

def plot_graph(G, highlight_path=None, color_by=None):
    pos = nx.spring_layout(G)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x, node_y = [], []
    for node in G.nodes():
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
                title='Node Metric',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node in G.nodes():
        if color_by:
            node_adjacencies.append(G.nodes[node].get(color_by, 0))
        else:
            node_adjacencies.append(len(list(G.neighbors(node))))
        node_text.append(
            f'Node: {node}<br>Type: {G.nodes[node]["node_type"]}<br># of connections: {len(list(G.neighbors(node)))}')

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    # Highlight the path if provided
    if highlight_path:
        path_edge_x, path_edge_y = [], []
        for i in range(len(highlight_path) - 1):
            x0, y0 = pos[highlight_path[i]]
            x1, y1 = pos[highlight_path[i + 1]]
            path_edge_x.extend([x0, x1, None])
            path_edge_y.extend([y0, y1, None])

        path_trace = go.Scatter(
            x=path_edge_x, y=path_edge_y,
            line=dict(width=2, color='red'),
            hoverinfo='none',
            mode='lines')

        fig = go.Figure(data=[edge_trace, node_trace, path_trace],
                        layout=go.Layout(
                            title='Supply Chain Network',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                text="",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
    else:
        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='Supply Chain Network',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                text="",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )
    return fig