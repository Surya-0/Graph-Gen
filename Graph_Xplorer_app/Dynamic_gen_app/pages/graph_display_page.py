import streamlit as st
import networkx as nx
import plotly.graph_objs as go
import pickle


def graph_display_page():
    st.header("Display Supply Chain Graph")

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

    if st.button("Display Graph"):
        with st.spinner("Generating graph..."):
            G = create_graph(data, selected_timestamp)
            fig = plot_graph(G)
            st.plotly_chart(fig, use_container_width=True)

            # Display some basic graph metrics
            st.subheader("Graph Metrics")
            col1, col2, col3 = st.columns(3)
            col1.metric("Number of Nodes", len(G.nodes()))
            col2.metric("Number of Edges", len(G.edges()))
            col3.metric("Average Degree", round(sum(dict(G.degree()).values()) / len(G), 2))


def create_graph(data, timestamp):
    G = nx.DiGraph()

    # Add nodes
    for node_type in ['business_group', 'product_families', 'product_offerings', 'modules', 'parts']:
        if node_type == 'business_group':
            node_data = [data['time_series_data'][timestamp][node_type]]
        else:
            node_data = data['time_series_data'][timestamp][node_type]

        for node in node_data:
            G.add_node(node['id'], **node, node_type=node_type)

    # Add edges
    for edge in data['time_series_data'][timestamp]['edges']:
        G.add_edge(edge['source_id'], edge['target_id'], **edge)

    return G


def plot_graph(G):
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
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node in G.nodes():
        node_adjacencies.append(len(list(G.neighbors(node))))
        node_text.append(
            f'Node: {node}<br>Type: {G.nodes[node]["node_type"]}<br># of connections: {len(list(G.neighbors(node)))}')

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

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