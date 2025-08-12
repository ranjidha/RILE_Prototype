import networkx as nx
from pyvis.network import Network
import pandas as pd
import tempfile

def display_graph(users, connections):
    G = nx.Graph()

    # Clean user names: make sure they are strings and drop NaNs
    users = users.dropna(subset=['name'])
    users['name'] = users['name'].astype(str)

    # Add nodes
    for _, row in users.iterrows():
        name = str(row['name'])  # Ensure node ID is a string
        title = row.get('role', '')
        group = row.get('interests', '')
        G.add_node(name, title=title, group=group)

    # Add edges with safe string conversion
    for _, row in connections.iterrows():
        source = str(row['from'])
        target = str(row['to'])
        label = row.get('relationship_type', '')
        G.add_edge(source, target, title=label)

    net = Network(height='600px', width='100%', notebook=False)
    net.from_nx(G)

    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
    net.save_graph(temp_path.name)

    with open(temp_path.name, 'r', encoding='utf-8') as f:
        html = f.read()
    return html
