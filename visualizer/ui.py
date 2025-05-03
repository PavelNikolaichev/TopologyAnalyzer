import streamlit as st
import networkx as nx
import plotly.graph_objects as go

def draw_topology(G: nx.Graph):
    pos = nx.spring_layout(G)
    edge_x, edge_y, edge_colors = [], [], []
    for u, v, data in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        color = {'ICMP': 'blue', 'UDP': 'green', 'TCP': 'red'}.get(data['protocol'], 'gray')
        edge_colors.append(color)
    node_x, node_y, labels = [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        labels.append(f"{node}\n{G.nodes[node].get('hostname', '')}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(color='gray', width=1), hoverinfo='none'))
    fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text', text=labels, textposition='bottom center', marker=dict(size=10, color='lightblue'), hoverinfo='text'))
    st.plotly_chart(fig)
