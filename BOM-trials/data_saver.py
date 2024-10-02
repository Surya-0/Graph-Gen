# data_saver.py

import csv
import os
import networkx as nx
import pickle

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
        print(f"Saved {filename}")

def save_graph(data, filename='supply_chain_graph.pkl'):
    G = nx.DiGraph()

    # Add nodes
    G.add_node(data['business_group']['id'], **data['business_group'], type='business_group')
    for pf in data['product_families']:
        G.add_node(pf['id'], **pf, type='product_family')
    for po in data['product_offerings']:
        G.add_node(po['id'], **po, type='product_offering')
    for module in data['modules']:
        G.add_node(module['id'], **module, type='module')
    for part in data['parts']:
        # part_type = 'make_part' if 'Make' in part['name'] else 'purchase_part'
        G.add_node(part['id'], **part, type='part')

    # Add edges
    for edge in data['edges']:
        G.add_edge(edge['source_id'], edge['target_id'], **edge)

    # Save the graph
    with open(filename, 'wb') as f:
        pickle.dump(G, f)
    print(f"Saved graph to {filename}")

def main(data):
    save_to_csv(data)
    save_graph(data)

