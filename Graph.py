import networkx as nx
import matplotlib.pyplot as plt
import os
import sys

def plot_graph(input_file):
    
    directory, _= os.path.split(input_file)
    
    G = nx.Graph()
    
    try:

        with open(input_file, "r", encoding="utf8") as infile:
            
            line_count=0 # Variable that keeps count of the lines being processed
            desired_number_of_nodes=50 #Desired number of lines that the user wants to process
            
            while line_count<desired_number_of_nodes:
                
                line=infile.readline()
                pair, weight = eval(line.strip())
                word1, word2 = pair

                # Add nodes if they're not already in the graph
                G.add_edge(word1, word2, weight=float(weight))
                line_count+=1
                
        # Draw the graph with spring layout
        plt.figure(figsize=(10, 6))
        pos = nx.spring_layout(G, seed=42, k=50)

        # Draw edges 
        nx.draw_networkx_edges(G, pos, alpha=0.3)

        # Draw nodes with colors depending on their degrees
        node_color = [G.degree[node] for node in G.nodes()]
        cmap = plt.cm.viridis 
        nodes = nx.draw_networkx_nodes(G, pos, node_size=300, node_color=node_color, cmap=cmap, alpha=0.7)

        # Add labels to nodes
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

        plt.title('Word pair network')
        plt.axis('off') 

        sm = plt.cm.ScalarMappable(cmap=cmap)
        sm.set_array(node_color)
        cbar = plt.colorbar(sm, label='Node Degree', ax=plt.gca())

        plt.tight_layout() 
        plt.savefig(f"{directory}/graph.png")
    
    except IOError as err:
        print(err)
        sys.exit(1)
        
    except FileNotFoundError("File does not exist"):
        sys.exit(1)