from random import  randint

import matplotlib.pyplot as plt
import networkx as nx

from GraphParameters import GraphParameters


class CommonGraphGenerator:
    def __init__(self, min_no_of_nodes=1, max_no_of_nodes=10, probability_for_edge_creation=0):
        """ Initialize parameters for generating a connected graph G using networkx library.
        Paramters
        ---------
        min_no_of_nodes : minimum number of nodes for the graph, optional
                         default value is 1

        max_no_of_nodes : maxiumum number of nodes for the graph, optional
                         default value is 10

        probability_edge_creation: probability of edge creation, optional
                         default value is 0

        Examples
        --------
        >>> G = CommonGraphGenerator()
        >>> G = CommonGraphGenerator(1,10, 0.1)
        """
        self.min_of_nodes = min_no_of_nodes
        self.max_of_nodes = max_no_of_nodes
        self.probability_for_edge_creation = probability_for_edge_creation
        self.current_graph = None

    def generate_graph(self):
        """
        Generate a networkx connected graph with the parameters entered during the initialization.

        The graphs will be generated using the erdos_renyi_graph algorithm of networkx library.
        If the specified probablity of edge creation is too low, the resultant graph might
        not become a connected graph. To avoid this issue, the probably will be increased
        in 0.05 increments after trying 5 iterations of graph generations with the current
        probability.

        Paramters
        ----------
        None

        Returns
        -------
        networkx graph

        Examples
        --------
        >>> G = CommonGraphGenerator()
        >>> graph = G.generate_graph()
        """
        generated_graph = None
        iteration = 0

        no_of_nodes = randint(self.min_of_nodes, self.max_of_nodes)
        while generated_graph is None or not nx.is_connected(
                generated_graph):  # make sure the generated graph is connected
            generated_graph = nx.erdos_renyi_graph(no_of_nodes, self.probability_for_edge_creation, directed=False)
            iteration += 1
            if iteration > 5:
                self.probability_for_edge_creation += 0.05
                iteration = 0

        self.current_graph = generated_graph
        self.add_attributes_to_nodes()
        return generated_graph

    def add_attributes_to_nodes(self):
        """
        private method that attaches some attributes for nodes (e.g. node type, node name)
        node type is randomly assigned and computed from GraphParameters class.
        """
        for node in self.current_graph.nodes():
            node_type = GraphParameters.get_node_type()
            self.current_graph.node[node]["type"] = node_type
            self.current_graph.node[node]["name"] = "node" + str(node)

    def list_nodes(self):
        """
        This is for debugging purpose. This one lists all the nodes and their types in the console.
        """
        for node in self.current_graph.nodes():
            print "node %d - type = %s" % (node, self.current_graph.node[node]["type"])

    def save_nodes_and_edges(self, file_path):
        """
        Writes nodes and edges of the common graph.
        """
        try:
            with open(file_path, "a") as stat_file:
                stat_file.write("number of nodes:%s \t number of edges:%s\n" % (
                self.current_graph.number_of_nodes(), self.current_graph.number_of_edges()))
                for node in self.current_graph.nodes():
                    stat_file.write("node %d - type = %s\n" % (node, self.current_graph.node[node]["type"]))

                for (fr, to) in self.current_graph.edges():
                    stat_file.write("edge (from, to): (%s, %s)\n" % (fr, to))
                stat_file.write("---end-of-common-graph---\n")
        except IOError:
            raise ("Unable to write to the specified file.")

    def show(self):
        """
        Display a generated connected graph using matplotlib library.

        Paramters
        ----------
        None

        Returns
        -------
        None

        Examples
        --------
        >>> G = CommonGraphGenerator()
        >>> graph = G.generate_graph()
        >>> G.show()
        """
        if self.current_graph:
            # nx.draw_networkx(self.current_graph)
            # plt.show()
            pos = nx.spring_layout(self.current_graph)
            nx.draw(self.current_graph, pos, with_labels=True)
            node_labels = nx.get_node_attributes(self.current_graph, 'type')
            nx.draw_networkx_labels(self.current_graph, pos, labels=node_labels)
            # edge_labels = nx.get_edge_attributes(G,'state')
            # nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)
            plt.show()
        else:
            raise Exception('No graph to visualise!')
