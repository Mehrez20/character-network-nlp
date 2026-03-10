import spacy
import networkx as nx
from pyvis.network import Network

nlp = spacy.load("en_core_web_sm")

with open("data/book.txt", "r", encoding="utf8") as f:
    text = f.read()

chapters = text.split("CHAPTER")

chapter_number = 1

for chapter in chapters:

    if len(chapter.strip()) < 20:
        continue

    doc = nlp(chapter)

    characters = []

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            characters.append(ent.text)

    G = nx.Graph()

    for i in range(len(characters)):
        for j in range(i+1, len(characters)):

            if characters[i] != characters[j]:
                G.add_edge(characters[i], characters[j])

    net = Network(height="750px", width="100%", bgcolor="#111111", font_color="white")

    for node in G.nodes():
        net.add_node(node, label=node)

    for edge in G.edges():
        net.add_edge(edge[0], edge[1])

    filename = f"chapter_{chapter_number}.html"
    net.write_html(filename)

    print("Graph created:", filename)

    chapter_number += 1