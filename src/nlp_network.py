import pandas as pd
import networkx as nx
from pyvis.network import Network
import community as community_louvain

print("Loading dataset...")

df = pd.read_csv("data/got_book1.csv")

# -------------------------
# CREATE GRAPH
# -------------------------

G = nx.from_pandas_edgelist(
    df,
    source="Source",
    target="Target",
    edge_attr="weight"
)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

# -------------------------
# IMPORTANCE (PAGERANK)
# -------------------------

pagerank = nx.pagerank(G)

TOP_N = 40

top_characters = sorted(
    pagerank,
    key=pagerank.get,
    reverse=True
)[:TOP_N]

G = G.subgraph(top_characters)

print("Filtered Nodes:", G.number_of_nodes())

# -------------------------
# COMMUNITY DETECTION
# -------------------------

partition = community_louvain.best_partition(G)

# -------------------------
# FAMILY DETECTION
# -------------------------

def get_family(name):

    parts = name.split("-")

    if len(parts) > 1:
        return parts[-1]

    return "Unknown"

# -------------------------
# COLORS
# -------------------------

colors = {
"Stark": "#1f77b4",
"Lannister": "#d62728",
"Targaryen": "#e600ff",
"Baratheon": "#ffcc00"
}

print("Generating graph...")

net = Network(
    height="900px",
    width="100%",
    bgcolor="#111111",
    font_color="white"
)

net.barnes_hut()

# -------------------------
# ADD NODES
# -------------------------

for node in G.nodes():

    family = get_family(node)

    color = colors.get(family, "#aaaaaa")

    size = 20 + pagerank[node] * 600

    tooltip = f"""
    Character: {node}
    Family: {family}
    PageRank: {pagerank[node]:.3f}
    Community: {partition[node]}
    """

    net.add_node(
        node,
        label=node,
        size=size,
        color=color,
        title=tooltip,
        group=family
    )

# -------------------------
# ADD EDGES
# -------------------------

for source, target, data in G.edges(data=True):

    net.add_edge(
        source,
        target,
        value=data["weight"]
    )

# -------------------------
# PHYSICS
# -------------------------

net.set_options("""
var options = {
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -14000,
      "springLength": 120
    }
  }
}
""")

# -------------------------
# EXPORT HTML
# -------------------------

net.write_html("network.html")

# -------------------------
# ADD LEGEND + FILTER
# -------------------------

legend_html = """
<div style="
position: fixed;
bottom: 50px;
left: 50px;
width: 220px;
background-color: #222;
color: white;
padding: 10px;
border-radius: 8px;
font-family: Arial;
">

<b>Families</b><br><br>

<span style="color:#1f77b4;">●</span> Stark<br>
<span style="color:#d62728;">●</span> Lannister<br>
<span style="color:#e600ff;">●</span> Targaryen<br>
<span style="color:#ffcc00;">●</span> Baratheon<br>

</div>
"""

with open("network.html","r",encoding="utf-8") as f:
    html = f.read()

html = html.replace("</body>", legend_html + "</body>")

with open("network.html","w",encoding="utf-8") as f:
    f.write(html)

print("Graph generated: network.html")