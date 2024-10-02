# config.py

BUSINESS_GROUP = 'Etch'

PRODUCT_FAMILIES = ['Kyo', 'Coronus', 'Flex', 'Versys Metal']

PRODUCT_OFFERINGS = {
    'Kyo': ['Versys® Kyo®', 'Versys® Kyo® C Series', 'Kyo® C Series', 'Kyo® E Series', 'Kyo® F Series', 'Kyo® G Series'],
    'Coronus': ['Coronus®', 'Coronus® HP', 'Coronus® DX'],
    'Flex': ['Exelan® Flex®', 'Exelan® Flex45™', 'Flex® D Series', 'Flex® E Series', 'Flex® F Series', 'Flex® G Series', 'Flex® H Series'],
    'Versys Metal': ['Versys® Metal', 'Versys® Metal45™', 'Versys® Metal L', 'Versys® Metal M', 'Versys® Metal N']
}

# Node features
BUSINESS_GROUP_FEATURES = ['id', 'name', 'revenue']
PRODUCT_FAMILY_FEATURES = ['id', 'name', 'revenue']
PRODUCT_OFFERING_FEATURES = ['id', 'name', 'inventory', 'demand', 'production_cost', 'importance_factor']
MODULE_FEATURES = ['id', 'name', 'inventory', 'importance_factor', 'demand', 'cost']
PART_FEATURES = ['id', 'name', 'inventory', 'importance_factor', 'demand', 'cost']

# Edge features
EDGE_FEATURES = ['source_id', 'target_id', 'quantity', 'transportation_cost', 'transportation_time']

# Configuration for random value generation
INVENTORY_RANGE = (50, 1000)
DEMAND_RANGE = (10, 200)
IMPORTANCE_FACTOR_RANGE = (0.1, 1.0)
COST_RANGE = (100, 10000)
QUANTITY_RANGE = (1, 20)
TRANSPORTATION_COST_RANGE = (10, 1000)
TRANSPORTATION_TIME_RANGE = (1, 30)  # in days

# Number of modules and parts to generate
NUM_MODULES = 50
NUM_PARTS = 100

# Probability of connection between nodes
CONNECTION_PROBABILITY = {
    'product_offering_to_module': 0.3,
    'module_to_part': 0.2
}