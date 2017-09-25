from random import randint, random, choice
import copy
import matplotlib.pyplot as plt
import networkx as nx

from CommonGraphGenerator import CommonGraphGenerator
from GraphParameters import GraphParameters


class GraphGenerator:
    def __init__(self, common_graph=None, min_no_of_nodes=1, max_no_of_total_nodes=15, probability_edge_creation=0, max_no_of_total_edges = 80):
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
       >>> G = GraphGenerator(min_no_of_nodes = 1,max_no_of_total_nodes = 10, probability_edge_creation= 0.1, max_no_of_total_edges = 60)
       """

        self.max_no_of_total_nodes = max_no_of_total_nodes
        self.max_no_of_total_edges = max_no_of_total_edges
        self.probability_edge_creation = probability_edge_creation
        self.current_graph = None

        self.common_graph = common_graph
        self.common_graph_no_of_nodes = 0
        self.common_graph_node_set = set()
        self.max_number_of_possible_nodes_to_add = 0

        self.max_number_of_possible_nodes_to_add = 0

        if self.common_graph:
            self.common_graph_no_of_nodes = nx.number_of_nodes(self.common_graph)
            self.self_common_graph_node_set = nx.nodes(self.common_graph)
            self.current_graph = copy.deepcopy(self.common_graph)
            self.max_number_of_possible_nodes_to_add = self.max_no_of_total_nodes - self.common_graph_no_of_nodes
            self.max_number_of_possible_edges_to_add = max(self.max_no_of_total_edges - self.common_graph.number_of_edges(),0)


    def generate_graph(self, display_added_edges=False, display_removed_edges=False):
        """
        Main method for generating graphs. It will generate a connected graph with the pre-initialized settings (through the constructor).
        :param display_added_edges:  whether to show two diagram with pre and post status after adding edges (for debugging purpose)
        :return: returns generated networkx graph.
        """

        if not self.common_graph:  # if no common graph has been given, just denerate a connected graph with default settings.
            cg = CommonGraphGenerator()
            self.current_graph = cg.generate_graph()
        else:
            self.current_graph = copy.deepcopy(self.common_graph)
            number_of_possible_nodes_to_add = randint(0,
                                                      self.max_number_of_possible_nodes_to_add)  # randomly decide the number of new nodes to be added to current common graph

            while self.max_number_of_possible_nodes_to_add > 0 and number_of_possible_nodes_to_add == 0:  # try best to add aleast 1 node, if possible
                number_of_possible_nodes_to_add = randint(0, self.max_number_of_possible_nodes_to_add)

            if number_of_possible_nodes_to_add > 0:
                node_id = self.common_graph_no_of_nodes  # start node_id from the number of nodes already in the common graph (note that the node ids are numbered from 0)
                # so if there were 5 nodes in the common graph (0,1,2,3,4) start adding new nodes from node 5 on wards
                added_nodes = set()
                for i in range(number_of_possible_nodes_to_add):
                    node_type = GraphParameters.get_node_type()  # generate random node type
                    self.current_graph.add_node(node_id, name="node" + str(node_id), type=node_type)
                    added_nodes.add(node_id)
                    node_id += 1

            if self.max_number_of_possible_edges_to_add >= 0:
                number_of_possible_edges_to_add = randint(0, self.max_number_of_possible_edges_to_add)
                while self.max_number_of_possible_edges_to_add > 0 and number_of_possible_edges_to_add == 0:  # try best to add aleast 1 node, if possible
                    number_of_possible_edges_to_add = randint(0, self.max_number_of_possible_edges_to_add)
            else:
                raise Exception("Unable to add more edges as total count of edges of common graph equal or exceeds the maxium number of edges of the graph.")
                number_of_possible_edges_to_add = 80

            if display_added_edges or display_removed_edges:  # this is for showing the pre-status before adding random edges between nodes
                plt.figure(1);
                plt.clf()
                fig, ax = plt.subplots(2, 1, num=1, sharex=True, sharey=True)
                pos = nx.spring_layout(self.current_graph)
                nx.draw_networkx(self.current_graph, pos=pos, ax=ax[0])

            is_connected = None
            all_added_edges = []  # holds a list of randomly added edges
            all_removed_edges = []  # holds a list of randomly added edges
            #print "Trying to add %d edges. Common graph already has %d edges." % (number_of_possible_edges_to_add,self.current_graph.number_of_edges())
            added_edge_count = 0
            attempt = 0
            while is_connected is None or not is_connected:  # randomly add edges until the graph is connected
                attempt  += 1
                if attempt > 20000: #nasty hack. if stuck, regeneate the whole graph.
                    return self.generate_graph()
                if added_edge_count > number_of_possible_edges_to_add:
                        if all_added_edges:
                            number_of_edges_to_remove = randint(1, len(all_added_edges))
                            for i in range(number_of_edges_to_remove):
                                removed_edge = choice(all_added_edges)
                                added_edge_count -= 1
                                all_added_edges.remove(removed_edge)
                                node, edge = removed_edge
                                self.current_graph.remove_edge(node, edge)
                else:
                    new_edges = self.add_random_edge()
                    if new_edges:
                        added_edge_count += 1
                        all_added_edges.extend(new_edges)
                #    all_removed_edges.extend(removed_edges)

                #print "edge count: %d" % added_edge_count
                is_connected = nx.is_connected(self.current_graph)

            if display_added_edges:
                # draw a new version of the graph and highlight changes for debugging purpose
                nx.draw_networkx(self.current_graph, pos=pos, ax=ax[1])
                nx.draw_networkx_edges(self.current_graph, pos=pos, ax=ax[1], edgelist=all_added_edges,
                                       edge_color='b', width=4)
                plt.show()
            if display_removed_edges:
                # draw a new version of the graph and highlight changes for debugging purpose
                nx.draw_networkx(self.current_graph, pos=pos, ax=ax[1])
                nx.draw_networkx_edges(self.current_graph, pos=pos, ax=ax[1], edgelist=all_removed_edges,
                                       edge_color='b', width=4)
                plt.show()


    # now add all the other GRAPH attributes (note the node attributes)
        self.add_graph_attributes()

        return self.current_graph

    def add_graph_attributes(self):
        # add graph specific attributes
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

    def add_random_edge(self, probability_of_new_connection=0.1):
        """
        randomly adds edges between nodes with no existing edges.
        based on: https://stackoverflow.com/questions/42591549/add-and-delete-a-random-edge-in-networkx
        :param probability_of_new_connection:
        :return: None
        """
        if self.current_graph:
            new_edges = []
            edge_added = False
            attempt = 0
            while not edge_added:
                node = choice(self.current_graph.nodes())
                # find the other nodes this one is connected to
                connected = [to for (fr, to) in self.current_graph.edges(node)]
                # and find the remainder of nodes, which are candidates for new edges
                unconnected = [n for n in self.current_graph.nodes() if not n in connected]

                # probabilistically add a random edge
                if len(unconnected):  # only try if new edge is possible
                    #if random() < probability_of_new_connection:
                    new = choice(unconnected)
                    self.current_graph.add_edge(node, new)
                    new_edges.append((node, new))
                    # book-keeping, in case both add and remove done in same cycle
                    unconnected.remove(new)
                    connected.append(new)
                    edge_added = True
                #if not edge_added and attempt > 2000:
            return new_edges

    def remove_random_edge(self, probability_of_delete_connection=0.1):
        """
        randomly adds edges between nodes with no existing edges.
        based on: https://stackoverflow.com/questions/42591549/add-and-delete-a-random-edge-in-networkx
        :param probability_of_new_connection:
        :return: None
        """
        if self.current_graph:
            removed_edges = []
            for node in self.current_graph.nodes():
                # find the other nodes this one is connected to
                connected = [to for (fr, to) in self.current_graph.edges(node)]
                # and find the remainder of nodes, which are candidates for new edges
                unconnected = [n for n in self.current_graph.nodes() if not n in connected]

                # probabilistically add a random edge
                if len(connected):  # only try if new edge is possible
                    if random() < probability_of_delete_connection:
                        remove = choice(connected)
                        self.current_graph.remove_edge(node, remove)
                        removed_edges.append((node, remove))
                        # book-keeping, in case both add and remove done in same cycle
                        connected.remove(remove)
                        unconnected.append(remove)
            return removed_edges

    def list_nodes(self):
        """
        list all the node and node types of the current graph for debugging purpose.
        :return: None.
        """
        for node in self.current_graph.nodes():
            print "node %d - type = %s" % (node, self.current_graph.node[node]["type"])

    def save_graph(self, file_name):
        """
        :param file_name: Save the current graph to a graphml file - file_name is the path to the file.
        :return: None.
        """
        if self.current_graph:
            try:
                nx.write_graphml(self.current_graph, file_name, prettyprint=True)
            except IOError:
                print 'Unable to save the file.'
        else:
            raise Exception("No graph to save.")

    def show(self, labels=True):
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
                node_labels = nx.get_node_attributes(self.current_graph, 'type')
                nx.draw_networkx_labels(self.current_graph, pos, labels=node_labels)
                plt.show()

        else:
            raise Exception('No graph to visualise!')
