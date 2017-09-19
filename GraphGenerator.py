import networkx as nx
import matplotlib.pyplot as plt
from random import randint, random, choice

from CommonGraphGenerator import CommonGraphGenerator
from GraphParameters import GraphParameters

class GraphGenerator:
    def __init__(self, common_graph = None, min_no_of_nodes = 1, max_no_of_total_nodes  = 15, probability_edge_creation = 0):
        """ Initialize parameters for generating a connected graph G using networkx library.
       Paramters
       ---------
       common_graph : A networkx graph (assumes a CommonGraphGenertor object)
                        default value is None

       min_no_of_nodes : minimum_number of nodes, optional
                        default is 1 but if a common graph is provided, the number of nodes in the
                        common graph will be used as the minimum number of nodes.

       max_no_of_total_nodes : maxiumum number of nodes for the graph, optional
                        default value is 10

       probability_edge_creation: probability of edge creation, optional
                        default value is 0

       Examples
       --------
       >>> G = GraphGenerator()
       >>> G = GraphGenerator(min_no_of_nodes = 1,max_no_of_total_nodes = 10, probability_edge_creation= 0.1)
       """

        self.max_no_of_total_nodes = max_no_of_total_nodes
        self.probability_edge_creation = probability_edge_creation
        self.current_graph = None

        self.common_graph = common_graph
        self.common_graph_no_of_nodes = 0
        self.common_graph_node_set = set()
        self.max_number_of_possible_nodes_to_add = 0
        if self.common_graph:
            self.common_graph_no_of_nodes =  nx.number_of_nodes(self.common_graph)
            self.self_common_graph_node_set = nx.nodes(self.common_graph)
            self.current_graph = self.common_graph
            self.max_number_of_possible_nodes_to_add = self.max_no_of_total_nodes - self.common_graph_no_of_nodes

    def generate_graph(self, display_added_edges=False):

        if not self.common_graph:           #if no common graph has been given, just denerate a connected graph with default settings.
            cg = CommonGraphGenerator()
            self.current_graph = cg.generate_graph()
        else:
            number_of_possible_nodes_to_add = randint(0, self.max_number_of_possible_nodes_to_add) #randomly decide the number of new nodes to be added to current graph

            while self.max_number_of_possible_nodes_to_add > 0 and number_of_possible_nodes_to_add == 0: #try best to add aleast 1 node, if possible
                number_of_possible_nodes_to_add = randint(0, self.max_number_of_possible_nodes_to_add)

            if number_of_possible_nodes_to_add > 0:
                node_id = self.common_graph_no_of_nodes
                added_nodes = set()
                for i in range(number_of_possible_nodes_to_add):
                    node_type = GraphParameters.get_node_type()
                    self.current_graph.add_node(node_id, name="node"+str(node_id), type=node_type)
                    added_nodes.add(node_id)
                    node_id += 1

            if display_added_edges:
                plt.figure(1); plt.clf()
                fig, ax = plt.subplots(2,1, num=1, sharex=True, sharey=True)
                pos = nx.spring_layout(self.current_graph)
                nx.draw_networkx(self.current_graph, pos=pos, ax=ax[0])


            #print self.common_graph_no_of_nodes, self.max_number_of_possible_nodes_to_add, number_of_possible_nodes_to_add
            #for node in self.self_common_graph_node_set:
            #    print node

            is_connected = None
            temp = []
            while is_connected is None or not is_connected: #add edges until the graph is connected
                new_edges = self.add_random_edge()
                temp.extend(new_edges)
                is_connected = nx.is_connected(self.current_graph)

            if display_added_edges:
                # and draw new version and highlight changes
                nx.draw_networkx(self.current_graph, pos=pos, ax=ax[1])
                nx.draw_networkx_edges(self.current_graph, pos=pos, ax=ax[1], edgelist=temp,
                       edge_color='b', width=4)
                plt.show()

        self.add_graph_attributes()
        return self.current_graph

    def add_graph_attributes(self):
        self.current_graph.graph['designName'] = GraphParameters.get_design_name()
        self.current_graph.graph['serie'] = GraphParameters.get_serie()
        self.current_graph.graph['target_market'] = GraphParameters.get_target_market()
        self.current_graph.graph['drive_wheels'] = GraphParameters.get_drive_wheels()
        self.current_graph.graph['battery_type'] = GraphParameters.get_battery_type()
        self.current_graph.graph['price'] = GraphParameters.get_price()
        self.current_graph.graph['horsepower'] = GraphParameters.get_horse_power()
        self.current_graph.graph['mpg'] = GraphParameters.get_mpg()
        self.current_graph.graph['cylinder'] = GraphParameters.get_cylinder()
        self.current_graph.graph['engine_size'] = GraphParameters.get_engine_size()
        self.current_graph.graph['controller'] = GraphParameters.get_controller()
        self.current_graph.graph['isDiesel'] = GraphParameters.get_is_diesel()
        self.current_graph.graph['hasTurbo'] = GraphParameters.get_has_turbo()
        self.current_graph.graph['isPlugin'] = GraphParameters.get_is_plugin()

    def add_random_edge(self, probability_of_new_connection = 0.1):
        """
        based on: https://stackoverflow.com/questions/42591549/add-and-delete-a-random-edge-in-networkx
        :param probability_of_new_connection:
        :return:
        """
        if self.current_graph:
            new_edges = []
            for node in self.current_graph.nodes():
                # find the other nodes this one is connected to
                connected = [to for (fr, to) in self.current_graph.edges(node)]
                # and find the remainder of nodes, which are candidates for new edges
                unconnected = [n for n in self.current_graph.nodes() if not n in connected]

                # probabilistically add a random edge
                if len(unconnected): # only try if new edge is possible
                    if random() < probability_of_new_connection:
                        new = choice(unconnected)
                        self.current_graph.add_edge(node, new)
                        #print "\tnew edge:\t {} -- {}".format(node, new)
                        new_edges.append( (node, new) )
                        # book-keeping, in case both add and remove done in same cycle
                        unconnected.remove(new)
                        connected.append(new)
            return new_edges

    def list_nodes(self):
        for node in self.current_graph.nodes():
            print "node %d - type = %s" % (node, self.current_graph.node[node]["type"])

    def save_graph(self, file_name):
        if self.current_graph:
            try:
                nx.write_graphml(self.current_graph,file_name, prettyprint = True)
            except IOError:
                print 'Unable to save the file.'
        else:
            raise Exception("No graph to save.")

    def show(self, labels = True):
        """
        Display a generated connected graph (using matplotlib library).

        Paramters
        ----------
        None

        Returns
        -------
        None

        Examples
        --------
        >>> G = GraphGenerator()
        >>> graph = G.generate_graph()
        >>> G.show()
        """
        if self.current_graph:
            if not labels:
                nx.draw_networkx(self.current_graph)
                plt.show()
            else:
                pos = nx.spring_layout(self.current_graph)
                nx.draw(self.current_graph, pos)
                node_labels = nx.get_node_attributes(self.current_graph,'type')
                nx.draw_networkx_labels(self.current_graph, pos, labels = node_labels)
                plt.show()

        else:
            raise Exception('No graph to visualise!')



#common_graph_generator = CommonGraphGenerator()
#generated_common_graph = common_graph_generator.generate_graph()

#G = GraphGenerator(generated_common_graph)
#G.generate_graph()
#G.show()
#G.generate_graph()
#G.show()