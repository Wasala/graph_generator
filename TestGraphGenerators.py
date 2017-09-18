from CommonGraphGenerator import CommonGraphGenerator
from GraphGenerator import GraphGenerator
import networkx as nx
from GraphParameters import GraphParameters
from GraphUtils import GraphUtils

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

utils = GraphUtils()
utils.post_process_graphml("./graph1.graphml")
utils.save_file('./graph2.graphml')
