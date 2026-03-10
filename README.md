# Game of Thrones Character Network Analysis

This project analyzes relationships between characters in Game of Thrones using network analysis and NLP.

## Project Overview

We build a character interaction network from the Game of Thrones dataset.

Each node represents a character and each edge represents interactions between characters.

We apply network analysis techniques such as:

- PageRank
- Community detection (Louvain)
- Graph visualization

## Technologies

Python  
NetworkX  
PyVis  
Pandas  

## Dataset

The dataset contains interactions between characters from the first book.

Columns include:

Source  
Target  
Weight  
Book  

## Visualization

The network graph highlights:

- Character importance using PageRank
- Families using color
- Communities detected using Louvain algorithm

## Example Characters

- Jon Snow
- Tyrion Lannister
- Eddard Stark
- Daenerys Targaryen
- Cersei Lannister

## Run the Project

Install dependencies

```bash
pip install pandas networkx pyvis python-louvain