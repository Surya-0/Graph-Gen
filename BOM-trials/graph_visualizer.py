# # graph_visualizer.py

import networkx as nx
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import csv
import os
import pickle

def load_graph(filename='supply_chain_graph.pkl'):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def create_node_trace(pos, node_types, node_sizes):
    node_x = []
    node_y = []
    for node in pos:
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=node_sizes,
            colorbar=dict(
                thickness=15,
                title='Node Type',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    return node_trace

def create_edge_trace(pos, edges):
    edge_x = []
    edge_y = []
    for edge in edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    return edge_trace

def visualize_graph(G):
    pos = nx.spring_layout(G, k=0.5, iterations=50)

    plt.figure(figsize=(20, 12))

    # Define node colors based on type
    color_map = {
        'business_group': '#FF9999',
        'product_families': '#66B2FF',
        'product_offerings': '#99FF99',
        'modules': '#FFCC99',
        'parts': '#FF99FF'
    }

    # Draw nodes
    for node_type, color in color_map.items():
        nx.draw_networkx_nodes(G, pos,
                               nodelist=[node for node, data in G.nodes(data=True) if data['type'] == node_type],
                               node_color=color, node_size=300, alpha=0.8)

    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20, width=0.5, alpha=0.5)

    # Draw labels
    nx.draw_networkx_labels(G, pos, {node: data['name'] for node, data in G.nodes(data=True)}, font_size=8)

    plt.title("Supply Chain Network", fontsize=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("supply_chain_graph.png", dpi=300, bbox_inches='tight')
    plt.show()

def main():
    G = load_graph()
    visualize_graph(G)

if __name__ == "__main__":
    main()