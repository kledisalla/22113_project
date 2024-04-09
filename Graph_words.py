import networkx as nx
import matplotlib.pyplot as plt
import os

def plot_graph(input_file):
    
    directory,filename = os.path.split(input_file)
    
    if filename=='':
        raise FileNotFoundError("File does not exist.")
        
    

    G = nx.Graph()

    with open(input_file) as infile:
        for line in infile:
            # Parse each line
            pair, weight = eval(line.strip())
            word1, word2 = pair

            # Add nodes if they're not already in the graph
            G.add_edge(word1, word2, weight=float(weight))

    # Find the node with the highest degree (most edges)
    node_most_edges = max(G.nodes(), key=G.degree)

    # Draw the graph with spring layout
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42, k=50)

    # Draw edges with widths proportional to the weights
    nx.draw_networkx_edges(G, pos, alpha=0.3)

    # Draw nodes with colors depending on their degrees
    node_degree = dict(G.degree())
    node_color = [G.degree[node] for node in G.nodes()]
    cmap = plt.cm.viridis  # You can choose any colormap you prefer
    nodes = nx.draw_networkx_nodes(G, pos, node_size=300, node_color=node_color, cmap=cmap, alpha=0.7)

    # Add labels to nodes
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

    plt.title('Weighted Graph')
    plt.axis('off')  # Disable axis

    # Create a dummy scatter plot for generating the colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap)
    sm.set_array(node_color)
    cbar = plt.colorbar(sm, label='Node Degree', ax=plt.gca())  # Specify the axes (ax=plt.gca())

    plt.tight_layout()  # Adjust layout
    plt.savefig("graph.png")


