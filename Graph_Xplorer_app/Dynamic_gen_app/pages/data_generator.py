import random
from datetime import datetime, timedelta
import math
from .config import *

class DataGenerator:
    def __init__(self, start_date, end_date, interval_days, num_modules, num_parts):
        self.start_date = start_date
        self.end_date = end_date
        self.interval_days = interval_days
        self.timestamps = self.generate_timestamps()
        self.business_group = None
        self.product_families = []
        self.product_offerings = []
        self.modules = []
        self.parts = []
        self.edges = []
        self.time_series_data = {}
        self.num_modules = num_modules
        self.num_parts = num_parts

    def generate_timestamps(self):
        current_date = self.start_date
        timestamps = []
        while current_date <= self.end_date:
            timestamps.append(current_date)
            current_date += timedelta(days=self.interval_days)
        return timestamps

    def generate_data(self):
        self._generate_static_structure()
        self._generate_time_series_data()

    def _generate_static_structure(self):
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
        for i in range(1, self.num_modules + 1):
            self.modules.append({
                'id': f'M_{i:03d}',
                'name': f"Module_{i}",
                'inventory': random.randint(*INVENTORY_RANGE),
                'importance_factor': random.uniform(*IMPORTANCE_FACTOR_RANGE),
                'demand': 0,  # Will be calculated later
                'cost': random.uniform(*COST_RANGE)
            })

    def _generate_parts(self):
        for i in range(1, self.num_parts + 1):
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

    def _generate_time_series_data(self):
        for timestamp in self.timestamps:
            self.time_series_data[timestamp] = {
                'business_group': self._generate_time_variant_data(self.business_group, timestamp),
                'product_families': [self._generate_time_variant_data(pf, timestamp) for pf in self.product_families],
                'product_offerings': [self._generate_time_variant_data(po, timestamp) for po in self.product_offerings],
                'modules': [self._generate_time_variant_data(module, timestamp) for module in self.modules],
                'parts': [self._generate_time_variant_data(part, timestamp) for part in self.parts],
                'edges': [self._generate_time_variant_edge_data(edge, timestamp) for edge in self.edges]
            }

    def _generate_time_variant_data(self, item, timestamp):
        time_variant_item = item.copy()
        for key, value in item.items():
            if isinstance(value, (int, float)):
                if key == 'inventory':
                    # For inventory, we want to simulate realistic changes
                    change = random.randint(-10, 10)  # Inventory can go up or down
                    time_variant_item[key] = max(0, value + change)  # Ensure non-negative
                elif key == 'demand':
                    # Demand might follow seasonal patterns
                    season_factor = 1 + 0.2 * math.sin(2 * math.pi * self.timestamps.index(timestamp) / len(self.timestamps))
                    time_variant_item[key] = max(0, int(value * season_factor * random.uniform(0.9, 1.1)))
                elif key in ['cost', 'price', 'revenue', 'production_cost']:
                    # Costs and prices might have small fluctuations
                    time_variant_item[key] = value * random.uniform(0.95, 1.05)
                elif key == 'importance_factor':
                    # Importance factor might change slightly over time
                    time_variant_item[key] = min(1, max(0, value + random.uniform(-0.05, 0.05)))
        return time_variant_item

    def _generate_time_variant_edge_data(self, edge, timestamp):
        time_variant_edge = edge.copy()
        for key in ['transportation_cost', 'transportation_time']:
            if key in edge:
                # Transportation costs and times might fluctuate due to various factors
                variation = random.uniform(0.9, 1.2)  # Allowing for potentially larger increases
                time_variant_edge[key] = edge[key] * variation
        return time_variant_edge

    def get_data(self):
        return {
            'static_structure': {
                'business_group': self.business_group,
                'product_families': self.product_families,
                'product_offerings': self.product_offerings,
                'modules': self.modules,
                'parts': self.parts,
                'edges': self.edges
            },
            'time_series_data': self.time_series_data
        }

# Example usage
if __name__ == "__main__":
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    interval_days = 7  # Weekly data
    num_modules = 100
    num_parts = 200

    generator = DataGenerator(start_date, end_date, interval_days, num_modules, num_parts)
    generator.generate_data()
    data = generator.get_data()

    print(f"Generated time series data for {len(data['time_series_data'])} time points")
    print("Static structure:")
    for key, value in data['static_structure'].items():
        if isinstance(value, list):
            print(f"  {key}: {len(value)} items")
        else:
            print(f"  {key}: 1 item")
    print("\nTime series data:")
    for timestamp, time_data in list(data['time_series_data'].items())[:5]:  # Print first 5 timestamps
        print(f"  {timestamp}:")
        for key, value in time_data.items():
            if isinstance(value, list):
                print(f"    {key}: {len(value)} items")
            else:
                print(f"    {key}: 1 item")
    print("  ...")  # Indicate that there's more data