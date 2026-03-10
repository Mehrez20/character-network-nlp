import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import community as community_louvain
import streamlit.components.v1 as components

st.title("Game of Thrones Character Network")

df = pd.read_csv("data/got_book1.csv")

# create graph
G = nx.from_pandas_edgelist(
    df,
    source="Source",
    target="Target",
    edge_attr="weight"
)

pagerank = nx.pagerank(G)

# slider top characters
top_n = st.slider("Top Characters", 10, 100, 40)

top_characters = sorted(
    pagerank,
    key=pagerank.get,
    reverse=True
)[:top_n]

G = G.subgraph(top_characters)

# detect families
def get_family(name):

    parts = name.split("-")

    if len(parts) > 1:
        return parts[-1]

    return "Unknown"

families = list(set(get_family(n) for n in G.nodes()))

selected_family = st.selectbox(
    "Filter by family",
    ["All"] + families
)

colors = {
"Stark": "#1f77b4",
"Lannister": "#d62728",
"Targaryen": "#e600ff",
"Baratheon": "#ffcc00"
}

partition = community_louvain.best_partition(G)

net = Network(height="700px", width="100%", bgcolor="#111111", font_color="white")

net.barnes_hut()

for node in G.nodes():

    family = get_family(node)

    if selected_family != "All" and family != selected_family:
        continue

    color = colors.get(family, "#aaaaaa")

    size = 20 + pagerank[node] * 600

    net.add_node(
        node,
        label=node,
        size=size,
        color=color,
        title=f"{node} | Family: {family}"
    )

for source, target, data in G.edges(data=True):

    if source in net.node_ids and target in net.node_ids:

        net.add_edge(
            source,
            target,
            value=data["weight"]
        )

net.save_graph("graph.html")

HtmlFile = open("graph.html", "r", encoding="utf-8")

components.html(HtmlFile.read(), height=700)