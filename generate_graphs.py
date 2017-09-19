from CommonGraphGenerator import CommonGraphGenerator
from GraphGenerator import GraphGenerator
from pathlib import Path
from GraphUtils import GraphUtils
import os

class MainGraphGenerator:
    """
    Main class for randomly generating connected graphs (with/without common graph).
    """
    def __init__(self):
        self.user_defined_parameters = False
        self.common_graph_min_no_of_nodes = None
        self.common_graph_max_no_of_nodes = None
        self.max_no_of_total_nodes = None

    def set_user_paramters(self, common_graph_min_no_of_nodes, common_graph_max_no_of_nodes, max_no_of_total_nodes):
        self.common_graph_min_no_of_nodes = common_graph_min_no_of_nodes
        self.common_graph_max_no_of_nodes = common_graph_max_no_of_nodes
        self.max_no_of_total_nodes = max_no_of_total_nodes
        self.user_defined_parameters = True

    def generate_graph_set(self, folder_path, no_of_graphs_in_the_set = 1):
        """
        :param folder_path: folder to store the generated graphs
        :param no_of_graphs_in_the_set: number of graphs to be generated as a single set
        :return: None.
        Examples
        --------
        >>> main = MainGraphGenerator()
        >>> main.generate_graph_set("./set1", no_of_graphs_in_the_set = 1)
        """
        if len(folder_path) > 0:
            folder_exists = False
            if Path(folder_path).is_dir():
                print "Warning: folder already exists. Existing graphs will be overwritten."
                folder_exists = True
            else:
                try:
                    os.makedirs(folder_path)
                    folder_exists = True
                except OSError as e:
                    print "Folder creation error."

            if folder_exists:

                try:
                    utils = GraphUtils()
                    #generate a common graph first
                    sub_graph_generator = None
                    if self.user_defined_parameters:
                        common_graph_generator = CommonGraphGenerator(self.common_graph_min_no_of_nodes, self.common_graph_max_no_of_nodes)
                        generated_common_graph = common_graph_generator.generate_graph()
                        sub_graph_generator = GraphGenerator(generated_common_graph, self.max_no_of_total_nodes) #initialize sub-graph generator with the common graph
                    else:
                        common_graph_generator = CommonGraphGenerator()
                        generated_common_graph = common_graph_generator.generate_graph()
                        sub_graph_generator = GraphGenerator(generated_common_graph) #initialize sub-graph generator with the common graph

                    #randomly generate sub-graphs
                    for i in range(1,no_of_graphs_in_the_set+1):
                        suffix = 'th' if 11 <= i <=13 else {1:'st',2:'nd',3:'rd'}.get(i % 10, 'th')
                        file_name = "%s%s_example_graph.graphml" % (i, suffix)
                        path = os.path.join(folder_path, file_name)
                        print "Processing:"+path
                        generated_graph = sub_graph_generator.generate_graph()
                        sub_graph_generator.save_graph(path)

                        #post-processed saved graph
                        utils.post_process_graphml(path)
                        utils.save_file(path+".xml")
                except IOError:
                    print ("Could not save generated graphs.")




A = MainGraphGenerator()
A.generate_graph_set("./set1",15)






