import streamlit as st
import pandas as pd
from utils.graph_utils import display_graph

# Set page config
st.set_page_config(page_title="Collaboration Graph App", layout="wide")

# Load and clean data
@st.cache_data
def load_data():
    users = pd.read_csv('data/users.csv')
    orgs = pd.read_csv('data/organizations.csv')
    projects = pd.read_csv('data/projects.csv')
    connections = pd.read_csv('data/connections.csv')

    # Basic cleanup
    users = users.dropna(subset=['name']).copy()
    users['name'] = users['name'].astype(str)
    users['interests'] = users['interests'].fillna("Unknown")
    users['role'] = users['role'].fillna("N/A")
    users['projects'] = users['projects'].fillna("None")

    orgs['related_users'] = orgs['related_users'].fillna("")
    orgs['type'] = orgs['type'].fillna("Unknown")

    projects['topic'] = projects['topic'].fillna("General")
    projects['org'] = projects['org'].fillna("Independent")
    projects['team_members'] = projects['team_members'].fillna("")

    connections = connections.dropna(subset=['from', 'to']).copy()
    connections['relationship_type'] = connections['relationship_type'].fillna("connected")

    return users, orgs, projects, connections

# Load data
users, orgs, projects, connections = load_data()

# Sidebar filters
st.sidebar.title("🔍 Filters & Options")

interests = users['interests'].str.split(',').explode().str.strip().unique()
selected_interests = st.sidebar.multiselect("Filter by Interest", sorted(interests))

show_notifications = st.sidebar.checkbox("Enable Notifications", value=True)
page = st.sidebar.radio("Navigation", ["🏠 Home", "🔎 Search", "🌐 Graph"])

# --- PAGE LOGIC ---

if page == "🏠 Home":
    st.title("Home: User Explorer")
    if selected_interests:
        filtered_users = users[users['interests'].apply(
            lambda x: any(i.strip() in x for i in selected_interests)
        )]
        st.success(f"Showing {len(filtered_users)} users with selected interests.")
        st.dataframe(filtered_users)
    else:
        st.write("Select one or more interests from the sidebar to view filtered users.")
        st.dataframe(users)

elif page == "🔎 Search":
    st.title("Search Users or Projects")
    query = st.text_input("Enter name, topic, or keyword:")
    if query:
        matched_users = users[users['name'].str.contains(query, case=False, na=False)]
        matched_projects = projects[projects['topic'].str.contains(query, case=False, na=False)]
        st.subheader("User Matches")
        st.dataframe(matched_users)
        st.subheader("Project Matches")
        st.dataframe(matched_projects)

elif page == "🌐 Graph":
    st.title("Collaboration Network")
    st.info("Generating the graph. This may take a few seconds if the dataset is large...")
    html_graph = display_graph(users, connections)
    st.components.v1.html(html_graph, height=1000, scrolling=False)


# Simulated notifications
if show_notifications:
    st.sidebar.success("🔔 Notifications Enabled (Simulated)")
