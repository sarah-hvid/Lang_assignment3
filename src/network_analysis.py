"""
A script that performs a simple network analysis on any undirected, weighted edgelist.
"""

# System tools
import os
import glob
import argparse

# Data analysis
import pandas as pd
from collections import defaultdict

# Network analysis tools
import networkx as nx
import matplotlib.pyplot as plt


# function that specifies the required arguments
def parse_args():
    # Initialise argparse
    ap = argparse.ArgumentParser()
    
    # command line parameters
    ap.add_argument("-f", "--file_input", required = True, help = "The filename or directory we want to work with")
    ap.add_argument("-p", "--plot_style", required = False, default = 'standard', help = "The style of the plot to be created by networkx (kamada_kawai, circular, spring)")

    args = vars(ap.parse_args())
    return args


# function that loads the data
def read_df(filepath):
    '''
    function that reads in a CSV file that's tab separated. it also returns the cleaned name of the file.
    
    filepath: the path to the CSV file.
    '''
    df = pd.read_csv(filepath, sep = '\t')
    
    # cleaning filename
    split_filename = filepath.split("/")[-1]
    file_only = split_filename.split(".")[0]
    
    return df, file_only


def plot_network(G, file_name):
    '''
    Function that plots a network graph in different styles and saves it with the filename the graph was created from.
    
    G: a networkx graph object
    file_name: the filename we are working with
    '''
    # grabbing plot argument
    args = parse_args()
    plot_style = args['plot_style']
    
    # drawing the network by style
    if plot_style == 'circular':
        nx.draw_circular(G, with_labels=True, node_size=20, font_size=10)
    
    elif plot_style == 'kamada_kawai':
        nx.draw_kamada_kawai(G, with_labels=True, node_size=20, font_size=10)
        
    elif plot_style == 'spring':
        nx.draw_spring(G, with_labels=True, node_size=20, font_size=10)
    
    elif plot_style == 'standard':
        nx.draw_networkx(G, with_labels=True, node_size=20, font_size=10)
        
    # saving the plot
    outpath = os.path.join('output', f'nx_{plot_style}_{file_name}.png')
    plt.savefig(outpath, dpi=300, bbox_inches='tight')
        
    return
       

def network_analysis(df):
    '''
    Function that performs a network analysis on an edgelist. The graph object is returned along with the degree, eigenvector and betweenness centrality scores.
    
    df: dataframe of an edgelist with columns source, target and weight.
    '''
    # create network
    G = nx.from_pandas_edgelist(df, "Source", "Target", ["Weight"])
     
    # calculating centrality measures
    dg = dict(G.degree())
    ev = nx.eigenvector_centrality(G)
    bc = nx.betweenness_centrality(G)
    
    return G, dg, ev, bc


def network_csv(dg, ev, bc, file_name):
    '''
    function that creates a CSV file for a network
    
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
    
    outpath = os.path.join('output', f'network_{file_name}.csv')
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
        plot_network(G, filename)
        
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
            plot_network(G, filename)
        
        print('[INFO] Script success.')
                

if __name__ == '__main__':
    main()

