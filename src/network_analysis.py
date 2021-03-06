"""
A script that performs a simple network analysis on any undirected, weighted edgelist.
"""

# System tools
import os
import sys
import glob
import argparse

# Data analysis
import pandas as pd
import math
import numpy as np
from collections import defaultdict

# Network analysis tools
import networkx as nx
import matplotlib.pyplot as plt


def parse_args():
    '''
    Function that specifies the available arguments
    '''
    # Initialise argparse
    ap = argparse.ArgumentParser()
    
    # command line parameters
    ap.add_argument("-f", "--file_input", required = True, help = "The filename or directory we want to work with")
    ap.add_argument("-l", "--layout", required = False, default = 'spring', help = "The layout of the plot to be created by networkx (spring, kamada_kawai, circular, random)")
    ap.add_argument("-node", "--node_size", required = False, default = 0, type = bool, help = "specifies whether the size of the nodes should be based on the degree of the node")
    ap.add_argument("-edge", "--edge_width", required = False, default = 0, type = bool, help = "specifies whether the width of the edges should be based on the weight of the connection")

    args = vars(ap.parse_args())
    return args


def read_df(filepath):
    '''
    Function that reads in a CSV file that's tab separated. it also returns the cleaned name of the file.
    
    filepath: the path to the CSV file.
    '''
    df = pd.read_csv(filepath, sep = '\t')
    
    # cleaning filename
    split_filename = filepath.split("/")[-1]
    file_only = split_filename.split(".")[0]
    
    return df, file_only


def scale(x, a, b):
    '''
    Function that contains a formulat that scales an array of values to a range between a and b.
    
    x: array to be scaled
    a: the minimum value of the new scale
    b: the maximum value of the new scale
    '''
    xnormalized = ((b - a) * ((x - min(x)) / (max(x) - min(x))) + a)  
    return xnormalized
       

def network_analysis(df):
    '''
    Function that performs a network analysis on an edgelist. The graph object is returned along with the degree, eigenvector and betweenness centrality scores.
    
    df: dataframe of an edgelist with columns: source, target and weight.
    '''
    # create network
    G = nx.from_pandas_edgelist(df, "Source", "Target", ["Weight"])
     
    # calculating centrality measures
    dg = dict(G.degree())
    ev = nx.eigenvector_centrality(G)
    bc = nx.betweenness_centrality(G)
    
    return G, dg, ev, bc


def plot_network(G, df, file_name):
    '''
    Function that plots a network graph in different styles and saves it with the filename the graph was created from. Dependent on user input the nodesizes can vary by degree and the edge width can vary by weight.
    
    G: a networkx graph object
    file_name: the filename we are working with
    '''
    # grabbing plot argument
    args = parse_args()
    plot_style = args['layout']
    n = args['node_size']
    e = args['edge_width']
    
    # calculate degree values for the node size 
    dg = dict(G.degree())
    node_sizes = []
    for k,v in dg.items():
        node_sizes.append(v)

    # scale values
    node_sizes = np.array(node_sizes)
    node_sizes = scale(node_sizes, 1200, 3500)

    # get weight for edge width
    weight = df['Weight'].values
    weight = scale(weight, 0.6, 7)
    
    # setting standard values if the user input is 0
    if args['node_size'] == 0:
        node_sizes = 2000
        
    if args['edge_width'] == 0:
        weight = 0.75
        
    f = plt.figure(figsize=(10,10))
    f.tight_layout()

    # drawing the network by style
    if plot_style == 'circular':
        nx.draw_circular(G, with_labels=True, width = weight,
                         alpha = 0.9, node_size = node_sizes,
                         node_color = 'lightgrey', font_size=10,
                         edgecolors = 'blue')
    
    elif plot_style == 'kamada_kawai':
        nx.draw_kamada_kawai(G, with_labels=True, width = weight,
                             alpha = 0.9, node_size = node_sizes,
                             node_color = 'lightgrey', font_size=10,
                             edgecolors = 'blue')
        
    elif plot_style == 'spring': # default
        nx.draw_spring(G, with_labels=True, width = weight,
                         alpha = 0.9, node_size = node_sizes,
                         node_color = 'lightgrey', font_size=10,
                         edgecolors = 'blue')
    
    elif plot_style == 'random':
        nx.draw_random(G, with_labels=True, width = weight,
                         alpha = 0.9, node_size = node_sizes,
                         node_color = 'lightgrey', font_size=10,
                         edgecolors = 'blue')
        
    # saving the plot
    outpath = os.path.join('output', f'{file_name}_{plot_style}_{n}_{e}.png')
    plt.savefig(outpath, bbox_inches='tight')
    return


def network_csv(dg, ev, bc, file_name):
    '''
    Function that creates a CSV file for a network containing centrality measures.
    
    dg: dict of degree centrality scores
    ev: dict of eigen vector centrality scores
    bc: dict of betweenness centrality scores 
    '''
    # creating dict
    dd = defaultdict(list)
    
    # listing input dicts, and matching by key in each
    for d in (dg, ev, bc): 
        for key, value in d.items():
            dd[key].append(value)
    
    # creating pandas dataframe from the dictionary        
    df_network = pd.DataFrame.from_dict(dd, orient = 'index', columns = ['Degree', 'Eigenvector','Betweenness'])
    df_network = df_network.rename_axis("Name").reset_index()
    
    outpath = os.path.join('output', f'{file_name}_network.csv')
    df_network.to_csv(outpath, index = False)
    
    return
 
    
def main():
    '''
    The process of the script.
    '''
    # parse arguments
    args = parse_args()
    input_name = args['file_input']
    
    isFile = os.path.isfile(input_name)
    if isFile == True:
        
        print('[INFO] Input is a file. Network analysis ...')
        df, filename = read_df(input_name)
        G, dg, ev, bc = network_analysis(df)
        network_csv(dg, ev, bc, filename)
        plot_network(G, df, filename)
        
        print('[INFO] Script success.')

    # if path provided is a directory:
    isDirectory = os.path.isdir(input_name)
    if isDirectory == True:
        # get the full path of each CSV file
        joined_paths = glob.glob(os.path.join(input_name, '*.csv'))
        
        print('[INFO] Input is a directory. Network analysis ...')
        for file in joined_paths:
            df, filename = read_df(file)
            G, dg, ev, bc = network_analysis(df)
            network_csv(dg, ev, bc, filename)
            plot_network(G, df, filename)
        
        print('[INFO] Script success.')
                

if __name__ == '__main__':
    main()