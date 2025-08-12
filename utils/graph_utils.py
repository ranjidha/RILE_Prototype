import networkx as nx
from pyvis.network import Network
import pandas as pd
import tempfile

def display_graph(users, connections):
    G = nx.Graph()
    
    for _, row in users.iterrows():
        G.add_node(row['name'], title=row['role'], group=row['interests'])

    for _, row in connections.iterrows():
        G.add_edge(row['from'], row['to'], title=row['relationship_type'])

    net = Network(height='600px', width='100%', notebook=False)
    net.from_nx(G)
    
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
    net.save_graph(temp_path.name)
    with open(temp_path.name, 'r', encoding='utf-8') as f:
        html = f.read()
    return html
