# pages/graph_generation.py

import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import io
import os
import csv
import zipfile
from .data_generator import DataGenerator
from .performance_utils import measure_performance, format_performance_metrics

@measure_performance
def generate_graph(total_nodes):
    generator = DataGenerator(total_nodes)
    generator.generate_data()
    return generator.get_data(), generator.get_graph()

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
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(f'Node: {adjacencies[0]}<br># of connections: {len(adjacencies[1])}')

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

def save_to_csv(data, output_dir='output'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for key, items in data.items():
        if key == 'business_group':
            items = [items]  # Convert single dict to list for consistent processing

        filename = os.path.join(output_dir, f'{key}.csv')
        with open(filename, 'w', newline='') as csvfile:
            if items:
                fieldnames = items[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in items:
                    writer.writerow(item)


def generate_csv_files(data):
    csv_files = {}
    for key, items in data.items():
        if key == 'business_group':
            items = [items]  # Convert single dict to list for consistent processing

        output = io.StringIO()
        if items:
            fieldnames = items[0].keys()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for item in items:
                writer.writerow(item)

        csv_files[f"{key}.csv"] = output.getvalue()

    return csv_files

def show():
    st.title("Graph Generation")

    total_nodes = st.slider("Total number of nodes", min_value=26, max_value=1000, value=100)

    if st.button("Generate Graph"):
        with st.spinner("Generating graph..."):
            result = generate_graph(total_nodes)
            data, G = result[0], result[1]
            performance_metrics = result[2]

        st.session_state['data'] = data
        st.session_state['graph'] = G

        st.success(f"Graph generated with {total_nodes} nodes.")

        col1, col2 = st.columns([3, 1])

        with col1:
            st.subheader("Generated Graph Visualization")
            fig = plot_graph(G)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Performance Metrics")
            st.text(format_performance_metrics(performance_metrics))

            with st.expander("Metrics Explanation"):
                st.info(get_metrics_explanation())

            csv_files = generate_csv_files(data)

            # Create a zip file containing all CSV files
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for filename, content in csv_files.items():
                    zip_file.writestr(filename, content)

            # Offer the zip file for download
            st.download_button(
                label="Download CSV files",
                data=zip_buffer.getvalue(),
                file_name="graph_data.zip",
                mime="application/zip"
            )

def get_metrics_explanation():
    return """
    Explanation of metrics:
    - Execution Time: The total time taken to complete the operation, measured in seconds.
    - Memory Used: The additional memory consumed during the operation, measured in megabytes (MB).
    - Peak Memory: The maximum amount of memory used at any point during the operation, measured in megabytes (MB).
    """