import streamlit as st
import networkx as nx
import plotly.graph_objects as go


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
        node_text.append(f"Node: {subgraph.nodes[adjacencies[0]]['label']}<br># of connections: {len(adjacencies[1])}")

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


def graph_query_page():
    st.title("Graph Query")

    if 'graph' not in st.session_state:
        st.warning("Please generate a graph first.")
        return

    G = st.session_state['graph']

    node_id = st.text_input("Enter a node ID to query:")
    levels = st.slider("Select the number of levels to explore:", min_value=1, max_value=5, value=2)

    if st.button("Query Subgraph"):
        if node_id in G.nodes:
            fig = query_subgraph(G, node_id, levels)
            st.plotly_chart(fig)
        else:
            st.error(f"Node {node_id} not found in the graph.")
