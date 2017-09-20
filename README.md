# Connected Graph Generator

This is a phython program to randomly generate a set of connected graphs for research purposes. The generated graphs can be saved as GraphML files.

  - A set of graphs can be generated to have a common graph.
  - Node and Graph attributes can also be generated randomly.
  
The generator is based on networkx library (based on algorithm Erdős-Rényi graphs). It requires Python 2.7+ with the following libraries pre-installed:

    - pathlib
    - networkx
    - matplotlib

A simple command line interface is avaiable for easy generation of graphs but seperate Classes are avaiable for further customisations.
Once cloned, use the generate_graph.py to generate set of graphs:

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
