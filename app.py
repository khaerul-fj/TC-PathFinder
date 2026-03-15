import streamlit as st
import heapq
import networkx as nx
import matplotlib.pyplot as plt
import json

# ------------------------------------------------------------------------------
# PROJECT: TURING CODE PATHFINDER
# ------------------------------------------------------------------------------

class TuringNavigationEngine:
    """Core engine optimized for cloud deployment."""
    def __init__(self, adjacency_map):
        self.graph = adjacency_map

    def solve_astar(self, start, goal, heuristics):
        if start not in self.graph or goal not in self.graph and goal not in [v for sub in self.graph.values() for v in sub]:
            return None, 0
        queue = [(heuristics.get(start, 0), 0, start, [])]
        visited = {}
        while queue:
            (f, g, current, path) = heapq.heappop(queue)
            if current in visited and visited[current] <= g: continue
            path = path + [current]
            if current == goal: return path, g
            visited[current] = g
            for neighbor, attrs in self.graph.get(current, {}).items():
                new_g = g + attrs['dist']
                new_f = new_g + heuristics.get(neighbor, 0)
                heapq.heappush(queue, (new_f, new_g, neighbor, path))
        return None, float('inf')

    def solve_dijkstra(self, start, goal):
        if start not in self.graph: return None, 0
        queue = [(0, start, [])]
        visited = {}
        while queue:
            (g, current, path) = heapq.heappop(queue)
            if current in visited and visited[current] <= g: continue
            path = path + [current]
            if current == goal: return path, g
            visited[current] = g
            for neighbor, attrs in self.graph.get(current, {}).items():
                heapq.heappush(queue, (g + attrs['dist'], neighbor, path))
        return None, float('inf')

# ------------------------------------------------------------------------------
# UI FRAMEWORK
# ------------------------------------------------------------------------------

st.set_page_config(page_title="TC Command Center", layout="wide")

# CSS Profesional untuk Online Branding
st.markdown("""
    <style>
    .main { background-color: #0b0e14; }
    div.stButton > button {
        background: linear-gradient(135deg, #2563eb, #1e40af);
        color: white; border-radius: 8px; padding: 0.75rem; font-weight: bold; width: 100%;
    }
    [data-testid="stExpander"] { background-color: #161b22; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("⚡ TC System Panel")
    algo_choice = st.selectbox("Engine Protocol", ["A* Search", "Dijkstra Algorithm"])
    st.divider()
    node_data = st.text_area("Nodes (JSON)", '{"A":20, "B":15, "C":10, "D":5, "E":0}', height=100)
    edge_data = st.text_area("Edges (JSON)", '{"A":{"B":{"dist":5}, "C":{"dist":10}}, "B":{"D":{"dist":8}}, "C":{"D":{"dist":2}, "E":{"dist":15}}, "D":{"E":{"dist":5}}}', height=100)
    st.divider()
    c1, c2 = st.columns(2)
    start_pt = c1.text_input("Origin", "A").upper()
    target_pt = c2.text_input("Target", "E").upper()
    execute = st.button("RUN ANALYSIS")

st.title("🚒 Emergency Response: TC PathFinder")

try:
    h_map = json.loads(node_data)
    g_map = json.loads(edge_data)
    G = nx.DiGraph()
    for u, neighbors in g_map.items():
        for v, info in neighbors.items():
            G.add_edge(u, v, weight=info['dist'])

    pos = nx.spring_layout(G, k=6.0, iterations=100, seed=42)
    engine = TuringNavigationEngine(g_map)
    path, cost = (engine.solve_astar(start_pt, target_pt, h_map) if "A*" in algo_choice 
                  else engine.solve_dijkstra(start_pt, target_pt))

    col_map, col_res = st.columns([2.5, 1])

    with col_map:
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='#0b0e14')
        ax.set_facecolor('#0b0e14')
        
        # Base Layers
        nx.draw_networkx_edges(G, pos, edge_color='#1e293b', width=1.8, arrows=True, 
                              arrowsize=25, connectionstyle='arc3,rad=0.3', ax=ax)
        nx.draw_networkx_nodes(G, pos, node_size=4000, node_color='#1e1b4b', 
                              edgecolors='#3b82f6', linewidths=2.5, ax=ax)
        nx.draw_networkx_labels(G, pos, font_color='#f8fafc', font_size=12, font_weight='bold', ax=ax)
        
        # Edge Labels
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=11, 
                                    font_color='#60a5fa', label_pos=0.5, rotate=True,
                                    bbox=dict(facecolor='#0b0e14', alpha=0.95, edgecolor='none', pad=2.0))

        if execute and path:
            p_edges = list(zip(path, path[1:]))
            nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='#2563eb', node_size=4000, ax=ax)
            nx.draw_networkx_edges(G, pos, edgelist=p_edges, edge_color='#60a5fa', 
                                  width=7, connectionstyle='arc3,rad=0.3', ax=ax)

        plt.axis('off')
        st.pyplot(fig)
        plt.close(fig) # Memory Management: Tutup figure setelah render

    with col_res:
        st.subheader("📊 Metrics")
        if execute:
            if path:
                st.metric("Total Distance", f"{cost} KM")
                st.success(" -> ".join(path))
            else:
                st.error("Route not found. Check Node labels.")

    st.divider()
    with st.expander("🔍 TECHNICAL AUDIT DATA"):
        t1, t2 = st.columns(2)
        t1.json(h_map)
        t2.json(g_map)

except Exception as e:
    st.error(f"System Error: {e}")

st.caption("© 2024 Turing Code Solutions | Deployment Ready v2.0")