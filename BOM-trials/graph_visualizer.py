# graph_visualizer.py

import networkx as nx
import matplotlib.pyplot as plt
import csv
import os

def load_csv_data(directory):
    data = {}
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            entity_type = filename[:-4]  # Remove '.csv'
            data[entity_type] = []
            with open(os.path.join(directory, filename), 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data[entity_type].append(row)
    return data


def create_graph(data):
    G = nx.DiGraph()

    # Add nodes
    for entity_type in ['business_group', 'product_families', 'product_offerings', 'modules', 'parts']:
        for item in data[entity_type]:
            G.add_node(item['id'], type=entity_type, **item)

    # Add edges
    for edge in data['edges']:
        G.add_edge(edge['source_id'], edge['target_id'], **edge)

    return G

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
    data = load_csv_data('output')
    G = create_graph(data)
    visualize_graph(G)


if __name__ == "__main__":
    main()