# data_generator.py

import random
import uuid
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


    # Private methods
    def _generate_business_group(self):
        self.business_group = {
            'id': str(uuid.uuid4()),
            'name': BUSINESS_GROUP,
            'revenue': random.uniform(*COST_RANGE) # Syntax used to unpack the tuple into separate arguments
        }

    def _generate_product_families(self):
        for pf in PRODUCT_FAMILIES:
            self.product_families.append({
                'id': str(uuid.uuid4()),
                'name': pf,
                'revenue': random.uniform(*COST_RANGE)
            })

    def _generate_product_offerings(self):
        for pf in self.product_families:
            for po in PRODUCT_OFFERINGS[pf['name']]:
                self.product_offerings.append({
                    'id': str(uuid.uuid4()),
                    'name': po,
                    'inventory': random.randint(*INVENTORY_RANGE),
                    'demand': random.randint(*DEMAND_RANGE),
                    'production_cost': random.uniform(*COST_RANGE),
                    'importance_factor': random.uniform(*IMPORTANCE_FACTOR_RANGE)
                })

    def _generate_modules(self):
        for _ in range(NUM_MODULES):
            self.modules.append({
                'id': str(uuid.uuid4()),
                'name': f"Module_{_}",
                'inventory': random.randint(*INVENTORY_RANGE),
                'importance_factor': random.uniform(*IMPORTANCE_FACTOR_RANGE),
                'demand': 0,  # Will be calculated later
                'cost': random.uniform(*COST_RANGE)
            })

    def _generate_parts(self):
        for _ in range(NUM_PARTS):
            self.parts.append({
                'id': str(uuid.uuid4()),
                'name': f"Part_{_}",
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
            for module in self.modules:
                if random.random() < CONNECTION_PROBABILITY['product_offering_to_module']:
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
            for part in self.parts:
                if random.random() < CONNECTION_PROBABILITY['module_to_part']:
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