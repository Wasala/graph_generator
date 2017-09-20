from CommonGraphGenerator import CommonGraphGenerator
from GraphGenerator import GraphGenerator
import networkx as nx
from GraphParameters import GraphParameters
from GraphUtils import GraphUtils

###################################################################
#Simple Test Program TODO:Unit tests                              #
###################################################################

#common_graph_generator = CommonGraphGenerator()
#generated_common_graph = common_graph_generator.generate_graph()
##common_graph_generator.show()
##common_graph_generator.list_nodes()

#G = GraphGenerator(generated_common_graph)
#g1 = G.generate_graph()
#nx.write_graphml(g1,"graph1.graphml", prettyprint = True)
#print g1.graph
#print "--------------------"
#G.list_nodes()

#utils = GraphUtils()
#utils.post_process_graphml("./graph1.graphml")
#utils.save_file('./graph2.graphml')


common_graph_generator = CommonGraphGenerator(min_no_of_nodes = 25,
                                              max_no_of_nodes = 40)
generated_common_graph = common_graph_generator.generate_graph()

common_graph_generator.save_nodes_and_edges("./stats.txt")
common_graph_generator.show()
