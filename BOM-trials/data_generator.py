# data_generator.py

import random
from config import *


class DataGenerator:
    def __init__(self):
        self.business_group = None
        self.product_families = []
        self.product_offerings = []
        self.modules = []
        self.parts = []
        self.edges = []

    def generate_data(self):
        self._generate_business_group()
        self._generate_product_families()
        self._generate_product_offerings()
        self._generate_modules()
        self._generate_parts()
        self._generate_edges()

    def _generate_business_group(self):
        self.business_group = {
            'id': 'BG_001',
            'name': BUSINESS_GROUP,
            'revenue': random.uniform(*COST_RANGE)
        }

    def _generate_product_families(self):
        for i, pf in enumerate(PRODUCT_FAMILIES, 1):
            self.product_families.append({
                'id': f'PF_{i:03d}',
                'name': pf,
                'revenue': random.uniform(*COST_RANGE)
            })

    def _generate_product_offerings(self):
        po_counter = 1
        for pf in self.product_families:
            for po in PRODUCT_OFFERINGS[pf['name']]:
                self.product_offerings.append({
                    'id': f'PO_{po_counter:03d}',
                    'name': po,
                    'inventory': random.randint(*INVENTORY_RANGE),
                    'demand': random.randint(*DEMAND_RANGE),
                    'production_cost': random.uniform(*COST_RANGE),
                    'importance_factor': random.uniform(*IMPORTANCE_FACTOR_RANGE)
                })
                po_counter += 1

    def _generate_modules(self):
        for i in range(1, NUM_MODULES + 1):
            self.modules.append({
                'id': f'M_{i:03d}',
                'name': f"Module_{i}",
                'inventory': random.randint(*INVENTORY_RANGE),
                'importance_factor': random.uniform(*IMPORTANCE_FACTOR_RANGE),
                'demand': 0,  # Will be calculated later
                'cost': random.uniform(*COST_RANGE)
            })

    def _generate_parts(self):
        for i in range(1, NUM_PARTS + 1):
            self.parts.append({
                'id': f'P_{i:03d}',
                'name': f"Part_{i}",
                'inventory': random.randint(*INVENTORY_RANGE),
                'importance_factor': random.uniform(*IMPORTANCE_FACTOR_RANGE),
                'demand': 0,  # Will be calculated later
                'cost': random.uniform(*COST_RANGE)
            })

    def _generate_edges(self):
        self._connect_business_group_to_product_families()
        self._connect_product_families_to_product_offerings()
        self._connect_product_offerings_to_modules()
        self._connect_modules_to_parts()

    def _connect_business_group_to_product_families(self):
        for pf in self.product_families:
            self.edges.append({
                'source_id': self.business_group['id'],
                'target_id': pf['id'],
                'quantity': 1,
                'transportation_cost': 0,
                'transportation_time': 0
            })

    def _connect_product_families_to_product_offerings(self):
        for pf in self.product_families:
            for po in self.product_offerings:
                if po['name'] in PRODUCT_OFFERINGS[pf['name']]:
                    self.edges.append({
                        'source_id': pf['id'],
                        'target_id': po['id'],
                        'quantity': 1,
                        'transportation_cost': 0,
                        'transportation_time': 0
                    })

    def _connect_product_offerings_to_modules(self):
        for po in self.product_offerings:
            num_connections = max(1, int(po['importance_factor'] * 10))  # Ensure at least one connection
            potential_modules = random.sample(self.modules, min(num_connections, len(self.modules)))

            for module in potential_modules:
                quantity = random.randint(*QUANTITY_RANGE)
                self.edges.append({
                    'source_id': po['id'],
                    'target_id': module['id'],
                    'quantity': quantity,
                    'transportation_cost': random.uniform(*TRANSPORTATION_COST_RANGE),
                    'transportation_time': random.uniform(*TRANSPORTATION_TIME_RANGE)
                })
                module['demand'] += po['demand'] * quantity

    def _connect_modules_to_parts(self):
        for module in self.modules:
            num_connections = max(1, int(module['importance_factor'] * 10))  # Ensure at least one connection
            potential_parts = random.sample(self.parts, min(num_connections, len(self.parts)))

            for part in potential_parts:
                quantity = random.randint(*QUANTITY_RANGE)
                self.edges.append({
                    'source_id': module['id'],
                    'target_id': part['id'],
                    'quantity': quantity,
                    'transportation_cost': random.uniform(*TRANSPORTATION_COST_RANGE),
                    'transportation_time': random.uniform(*TRANSPORTATION_TIME_RANGE)
                })
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

