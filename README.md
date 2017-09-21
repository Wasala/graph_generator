# Connected Graph Generator

This is a Python program to randomly generate sets of connected graphs for research purposes. The generated graphs can be exported as GraphML files.

  - A set of graphs can be generated to have a common graph.
  - Node and Graph attributes can also be generated randomly.
  
The generator is based on networkx library (and based on algorithm Erdős-Rényi graphs). It requires Python 2.7+ with the following libraries pre-installed:

    - pathlib
    - networkx
    - matplotlib

A simple command line interface is avaiable for easy generation of graphs, but Classes can be used directly for further customisations.
Once cloned this repository, use the generate_graph.py to generate set of graphs. Command line syntax given below:

```sh
generate_graphs.py -n <number of graphs> -o <output folder> -m <min no.of nodes of common graph> -x <max no. of nodes of common graph> -t <max total no. of nodes of graphs>"
```

### Classes
generate_grahs (MainGraphGenerator) - main driver program
CommonGraphGenerator - used to generate a common graph
GraphGenerator - generate random graphs either with a common graph or not
GraphParameters - custom attribute provider for generated graphs
GraphUtils - post-processor for generated .GraphML files.

#### License
GPL

#### Author/Contact
Asanka Wasala 
