import streamlit as st
import pandas as pd
from utils.graph_utils import display_graph

# Load data
@st.cache
def load_data():
    users = pd.read_csv('data/users.csv')
    orgs = pd.read_csv('data/organizations.csv')
    projects = pd.read_csv('data/projects.csv')
    connections = pd.read_csv('data/connections.csv')
    return users, orgs, projects, connections

users, orgs, projects, connections = load_data()

# Sidebar - Interest selector and notification checkbox
st.sidebar.title("Filters")
selected_interests = st.sidebar.multiselect("Select Interests", users['interests'].str.split(',').explode().unique())
show_notifications = st.sidebar.checkbox("Enable Notifications", value=True)

# Main App Pages
page = st.sidebar.radio("Go to", ["Home", "Search", "Graph"])

if page == "Home":
    st.title("Welcome!")
    st.write("Select interests to explore users and projects.")
    if selected_interests:
        filtered_users = users[users['interests'].apply(lambda x: any(i in x for i in selected_interests))]
        st.dataframe(filtered_users)

elif page == "Search":
    st.title("Search Users & Projects")
    search_text = st.text_input("Search by name or topic")
    if search_text:
        user_matches = users[users['name'].str.contains(search_text, case=False)]
        project_matches = projects[projects['topic'].str.contains(search_text, case=False)]
        st.subheader("Users")
        st.dataframe(user_matches)
        st.subheader("Projects")
        st.dataframe(project_matches)

elif page == "Graph":
    st.title("Network Graph")
    html_graph = display_graph(users, connections)
    st.components.v1.html(html_graph, height=600, scrolling=True)

# Simulated Notification
if show_notifications:
    st.sidebar.success("🔔 Notifications enabled (simulated)")
