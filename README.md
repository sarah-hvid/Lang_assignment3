# Assignment 3 - Network analysis
 
Link to GitHub of this assignment: https://github.com/sarah-hvid/Lang_assignment3

## Assignment description
The purpose of this assignment is to perform a network analysis. The ```.py``` created should function on _any_ input data, as long as the input format is correct; an undirected, weighted edgelist with the same column names (source, type, target, weight). The script should also function with a single file or an entire directory as input. For any file the script should save a visualisation of the network and a CSV file showing centrality scores for each node.\
The full assignment description is available in the ```assignment3.md``` file.

## Methods
Initially, the user must specify either a CSV file or directory of CSV files as input (*note* these should be tab delimited). The same steps are then applied for each file specified, regardless of the input type. The file is loaded as a ```pandas``` dataframe. The ```Networkx``` module is then used to conduct the network analysis itself. Three centrality scores are calculated and saved in a CSV file; degree centrality, eigen vector centrality and betweenness centrality. The CSV file will be saved in the ```output``` folder, and the name will vary depending on the input file name. A plot will also be created of the network graph. The user may specify the following parameters:
- layout (-l): *kamada_kawai*, *circular*, *spring* or *random*. *Spring* is the default.
- node_size (-n): boolean input, **0** makes all nodes the same size, **1** bases the nodesize on the number of degrees a node has. **0** is the default.
- edge_width (-e): boolean input, **0** makes all edges the same width, **1** bases the width on the weight between two nodes. **0** is the default.

A scaling function is used to fit the values of degree and weight within a specified range. The plot will be saved in the ```output``` folder and named according to input file name, layout, nodesize value and edge width value. 

## Usage
In order to run the script, certain modules need to be installed. These are available in the ```requirements.txt``` file. The folder structure must be the same as in this GitHub repository (ideally, clone the repository).
```bash
git clone https://github.com/sarah-hvid/Lang_assignment3.git
cd Lang_assignment3
pip install -r requirements.txt
```
The data used in the assignment is the files in the folder called ```network_data```. The data is available in the shared ```CDS-LANG``` folder. The files must be placed in the ```data``` folder in order to replicate the results of this assignment.\
The current working directory when running the script must be the one that contains the ```data```, ```output``` and ```src``` folder.\
\
How to run the script from the command line: 

__The network anaysis script__\
Specified file:
```bash
python src/network_analysis.py -f data/H5.csv
```
Specified file and layout:
```bash
python src/network_analysis.py -f data/H5.csv -l kamada_kawai
```
Specified directory, layout, node_size and edge_width:
```bash
python src/network_analysis.py -f data -l circular -n 1 -e 1
```

Examples of the outputs of the script can be found in the ```output``` folder. 

## Results
The results of the script are as expected. The plots and CSV files are created as they should. As this script does not attempt to analyse any particular data but rather functions on any _'random'_ data, there are no results to discuss per se.\
The output is the result:\
\
[**CSV file**](/output/H8_network.csv)

| Name  | Degree | Eigenvector  | Betweenness |
| ------------- | ------------- | ------------- | ------------- |
| Buckingham  | 9  | 0.12232958324001253  | 0.2264562834249246  |
| Norfolk  | 11  | 0.300241533764166  | 0.15881797902703826 |
| Abergavenny  | 3  | 0.05305190189311667  | 0.009290264516745358 |
| ...  | ...  | ...  | ... |

**Standard plot**

<img src="/output/KJ_spring_0_0.png" width="500" height="400">

**Circular plot, nodesize**

<img src="/output/H8_circular_True_0.png" width="500" height="400">

**Kamada_kawai, nodesize and edgewidth**

<img src="/output/KJ_kamada_kawai_True_True.png" width="500" height="400">

**Random, edgewidth**

<img src="/output/H8_random_0_True.png" width="500" height="400">





