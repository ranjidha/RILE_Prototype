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

    # Create PyVis network
    net = Network(height='1000px', width='100%', bgcolor='white', font_color='black')
    net.from_nx(G)
    # Add nodes with size proportional to degree
    for node in G.nodes():
        degree = G.degree(node)
        size = 10 + degree * 3  # base size 10, bigger if more connections
        net.add_node(node,
                     title=G.nodes[node].get('title', ''),
                     group=G.nodes[node].get('group', ''),
                     size=size)

    # Add edges
    for source, target, data in G.edges(data=True):
        net.add_edge(source, target, title=data.get('title', ''))

    # Physics for better spacing
    net.barnes_hut()
    net.repulsion(
        node_distance=180,
        central_gravity=0.02,
        spring_length=180,
        spring_strength=0.03,
        damping=0.09
    )

    # Save to HTML
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
    net.save_graph(temp_path.name)

    with open(temp_path.name, 'r', encoding='utf-8') as f:
        html = f.read()
    return html
