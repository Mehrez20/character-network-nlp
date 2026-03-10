import pandas as pd
import networkx as nx
from pyvis.network import Network
from networkx.algorithms import community

# charger dataset
data = pd.read_csv("data/got_book1.csv")

# créer graphe
G = nx.Graph()

for _, row in data.iterrows():
    source = row["Source"]
    target = row["Target"]
    weight = row["weight"]

    G.add_edge(source, target, weight=weight)

print("\n===== NETWORK STATS =====")

print("Nodes (characters):", G.number_of_nodes())
print("Edges (relationships):", G.number_of_edges())
print("Density:", nx.density(G))

# centralité simple
degree_centrality = nx.degree_centrality(G)

# influence
betweenness = nx.betweenness_centrality(G)

# tri personnages
top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
top_between = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]

print("\n===== MOST CONNECTED CHARACTERS =====\n")

for char, score in top_degree:
    print(char, round(score,4))

print("\n===== MOST INFLUENTIAL CHARACTERS =====\n")

for char, score in top_between:
    print(char, round(score,4))

# communautés
communities = community.greedy_modularity_communities(G)

print("\nCommunities detected:", len(communities))

community_map = {}

for i, comm in enumerate(communities):
    for node in comm:
        community_map[node] = i

# graph interactif
net = Network(
    height="800px",
    width="100%",
    bgcolor="#222222",
    font_color="white"
)

for node in G.nodes():

    size = degree_centrality[node] * 150
    group = community_map[node]

    net.add_node(
        node,
        label=node,
        size=size,
        group=group
    )

for source, target, data in G.edges(data=True):

    net.add_edge(
        source,
        target,
        value=data["weight"]
    )

net.write_html("network.html")

print("\nGraph generated: network.html")