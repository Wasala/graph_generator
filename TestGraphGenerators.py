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
                                              max_no_of_nodes = 40, max_no_of_edges=40)
generated_common_graph = common_graph_generator.generate_graph()
print "Common graph generated: N %d, E: %d" % (generated_common_graph.number_of_nodes(), generated_common_graph.number_of_edges())
#common_graph_generator.save_nodes_and_edges("./stats.txt")
#common_graph_generator.show()
sub_graph_generator = GraphGenerator(generated_common_graph,
                                     max_no_of_total_nodes=40, max_no_of_total_edges = 60)
sub_graph = sub_graph_generator.generate_graph()
print "Sub graph generated: N %d, E: %d" % (sub_graph .number_of_nodes(), sub_graph.number_of_edges())

sub_graph = sub_graph_generator.generate_graph()
print "Sub graph generated: N %d, E: %d" % (sub_graph .number_of_nodes(), sub_graph.number_of_edges())
sub_graph_generator.show()