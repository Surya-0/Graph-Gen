# data_generator_page.py

import random
from .config import *
import networkx as nx

class DataGenerator:
    def __init__(self, total_nodes):
        self.total_nodes = max(total_nodes, MIN_NODES)
        self.business_group = None
        self.product_families = []
        self.product_offerings = []
        self.modules = []
        self.parts = []
        self.edges = []
        self.G = nx.DiGraph()

    def generate_data(self):
        self._generate_business_group()
        self._generate_product_families()
        self._generate_product_offerings()
        self._generate_modules_and_parts()
        self._generate_edges()

    def _generate_business_group(self):
        self.business_group = {
            'id': 'BG_001',
            'name': BUSINESS_GROUP,
            'revenue': random.uniform(*COST_RANGE)
        }
        self.G.add_node('BG_001', **self.business_group, type='business_group')

    def _generate_product_families(self):
        for i, pf in enumerate(PRODUCT_FAMILIES, 1):
            pf_data = {
                'id': f'PF_{i:03d}',
                'name': pf,
                'revenue': random.uniform(*COST_RANGE)
            }
            self.product_families.append(pf_data)
            self.G.add_node(pf_data['id'], **pf_data, type='product_family')

    def _generate_product_offerings(self):
        po_counter = 1
        for pf in self.product_families:
            for po in PRODUCT_OFFERINGS[pf['name']]:
                po_data = {
                    'id': f'PO_{po_counter:03d}',
                    'name': po,
                    'inventory': random.randint(*INVENTORY_RANGE),
                    'demand': random.randint(*DEMAND_RANGE),
                    'production_cost': random.uniform(*COST_RANGE),
                    'importance_factor': random.uniform(*IMPORTANCE_FACTOR_RANGE)
                }
                self.product_offerings.append(po_data)
                self.G.add_node(po_data['id'], **po_data, type='product_offering')
                po_counter += 1

    def _generate_modules_and_parts(self):
        remaining_nodes = self.total_nodes - len(self.G.nodes)
        num_modules = int(remaining_nodes * MODULE_PART_RATIO)
        num_parts = remaining_nodes - num_modules

        for i in range(1, num_modules + 1):
            module_data = {
                'id': f'M_{i:03d}',
                'name': f"Module_{i}",
                'inventory': random.randint(*INVENTORY_RANGE),
                'importance_factor': random.uniform(*IMPORTANCE_FACTOR_RANGE),
                'demand': 0,
                'cost': random.uniform(*COST_RANGE)
            }
            self.modules.append(module_data)
            self.G.add_node(module_data['id'], **module_data, type='module')

        for i in range(1, num_parts + 1):
            part_data = {
                'id': f'P_{i:03d}',
                'name': f"Part_{i}",
                'inventory': random.randint(*INVENTORY_RANGE),
                'importance_factor': random.uniform(*IMPORTANCE_FACTOR_RANGE),
                'demand': 0,
                'cost': random.uniform(*COST_RANGE)
            }
            self.parts.append(part_data)
            self.G.add_node(part_data['id'], **part_data, type='part')

    def _generate_edges(self):
        self._connect_business_group_to_product_families()
        self._connect_product_families_to_product_offerings()
        self._connect_product_offerings_to_modules()
        self._connect_modules_to_parts()

    def _connect_business_group_to_product_families(self):
        for pf in self.product_families:
            edge_data = {
                'source_id': self.business_group['id'],
                'target_id': pf['id'],
                'quantity': 1,
                'transportation_cost': 0,
                'transportation_time': 0
            }
            self.edges.append(edge_data)
            self.G.add_edge(edge_data['source_id'], edge_data['target_id'], **edge_data)

    def _connect_product_families_to_product_offerings(self):
        for pf in self.product_families:
            for po in self.product_offerings:
                if po['name'] in PRODUCT_OFFERINGS[pf['name']]:
                    edge_data = {
                        'source_id': pf['id'],
                        'target_id': po['id'],
                        'quantity': 1,
                        'transportation_cost': 0,
                        'transportation_time': 0
                    }
                    self.edges.append(edge_data)
                    self.G.add_edge(edge_data['source_id'], edge_data['target_id'], **edge_data)

    def _connect_product_offerings_to_modules(self):
        for po in self.product_offerings:
            num_connections = max(1, int(po['importance_factor'] * 10))
            potential_modules = random.sample(self.modules, min(num_connections, len(self.modules)))

            for module in potential_modules:
                quantity = random.randint(*QUANTITY_RANGE)
                edge_data = {
                    'source_id': po['id'],
                    'target_id': module['id'],
                    'quantity': quantity,
                    'transportation_cost': random.uniform(*TRANSPORTATION_COST_RANGE),
                    'transportation_time': random.uniform(*TRANSPORTATION_TIME_RANGE)
                }
                self.edges.append(edge_data)
                self.G.add_edge(edge_data['source_id'], edge_data['target_id'], **edge_data)
                module['demand'] += po['demand'] * quantity

    def _connect_modules_to_parts(self):
        for module in self.modules:
            num_connections = max(1, int(module['importance_factor'] * 10))
            potential_parts = random.sample(self.parts, min(num_connections, len(self.parts)))

            for part in potential_parts:
                quantity = random.randint(*QUANTITY_RANGE)
                edge_data = {
                    'source_id': module['id'],
                    'target_id': part['id'],
                    'quantity': quantity,
                    'transportation_cost': random.uniform(*TRANSPORTATION_COST_RANGE),
                    'transportation_time': random.uniform(*TRANSPORTATION_TIME_RANGE)
                }
                self.edges.append(edge_data)
                self.G.add_edge(edge_data['source_id'], edge_data['target_id'], **edge_data)
                part['demand'] += module['demand'] * quantity

    def get_data(self):
        return {
            'business_group': self.business_group,
            'product_families': self.product_families,
            'product_offerings': self.product_offerings,
            'modules': self.modules,
            'parts': self.parts,
            'edges': self.edges
        }

    def get_graph(self):
        return self.G