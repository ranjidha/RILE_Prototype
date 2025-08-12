import pandas as pd
import networkx as nx
from pyvis.network import Network
import tempfile

def display_graph(users: pd.DataFrame, connections: pd.DataFrame) -> str:
    def to_node_id(x):
        """Return an int (if cleanly convertible) or a stripped string; None if NA."""
        if pd.isna(x):
            return None
        # Treat pure numeric IDs as ints so PyVis is happy; else string
        try:
            # only cast to int if it doesn't change the value when stringified
            xi = float(x)
            if xi.is_integer():
                return int(xi)
        except (TypeError, ValueError):
            pass
        s = str(x).strip()
        return s if s else None

    # --- Clean users ---
    users = users.copy()
    if 'name' not in users.columns:
        raise ValueError("`users` must include a 'name' column.")
    users['name_id'] = users['name'].apply(to_node_id)
    users = users.dropna(subset=['name_id'])

    # Optional attributes
    for col in ['role', 'interests']:
        if col not in users.columns:
            users[col] = ''
        users[col] = users[col].fillna('').astype(str).str.strip()

    # --- Clean connections ---
    connections = connections.copy()
    for col in ['from', 'to']:
        if col not in connections.columns:
            raise ValueError("`connections` must include 'from' and 'to' columns.")
        connections[col] = connections[col].apply(to_node_id)

    # drop edges with missing endpoints and self-loops
    connections = connections.dropna(subset=['from', 'to'])
    connections = connections[connections['from'] != connections['to']]

    if 'relationship_type' not in connections.columns:
        connections['relationship_type'] = ''
    connections['relationship_type'] = (
        connections['relationship_type'].fillna('').astype(str).str.strip()
    )

    # --- Build graph ---
    G = nx.Graph()

    # Add user nodes
    for _, r in users.iterrows():
        G.add_node(
            r['name_id'],
            title=r['role'],
            group=r['interests']
        )

    # Ensure nodes from edges exist (even if not in users)
    all_ids = set(G.nodes)
    for _, r in connections.iterrows():
        for nid in (r['from'], r['to']):
            if nid not in all_ids:
                G.add_node(nid, title='', group='')
                all_ids.add(nid)

    # Add edges (drop exact duplicates)
    seen_edges = set()
    for _, r in connections.iterrows():
        a, b = r['from'], r['to']
        key = tuple(sorted((a, b)))
        if key in seen_edges:
            continue
        seen_edges.add(key)
        G.add_edge(a, b, title=r['relationship_type'])

    # --- Render with PyVis ---
    net = Network(height='1000px', width='100%', bgcolor='white', font_color='black')
    net.from_nx(G)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
    net.save_graph(tmp.name)
    with open(tmp.name, 'r', encoding='utf-8') as f:
        html = f.read()
    return html
