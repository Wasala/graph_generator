import getopt
import os
import sys

from pathlib import Path

from CommonGraphGenerator import CommonGraphGenerator
from GraphGenerator import GraphGenerator
from GraphUtils import GraphUtils


class MainGraphGenerator:
    """
    Main class for randomly generating connected graphs (with/without common graph).
    """

    def __init__(self):
        self.user_defined_parameters = False
        self.common_graph_min_no_of_nodes = None
        self.common_graph_max_no_of_nodes = None
        self.common_graph_max_no_of_edges = None
        self.max_no_of_total_edges = None
        self.max_no_of_total_nodes = None

    def set_user_paramters(self, common_graph_min_no_of_nodes, common_graph_max_no_of_nodes, max_no_of_total_nodes, common_graph_max_no_of_edges, max_no_of_total_edges):
        self.common_graph_min_no_of_nodes = common_graph_min_no_of_nodes
        self.common_graph_max_no_of_nodes = common_graph_max_no_of_nodes
        self.common_graph_max_no_of_edges = common_graph_max_no_of_edges
        self.max_no_of_total_nodes = max_no_of_total_nodes
        self.max_no_of_total_edges = max_no_of_total_edges
        self.user_defined_parameters = True

    def generate_graph_set(self, folder_path, no_of_graphs_in_the_set=1):
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
                    # generate a common graph first
                    sub_graph_generator = None
                    if self.user_defined_parameters:
                        common_graph_generator = CommonGraphGenerator(min_no_of_nodes=self.common_graph_min_no_of_nodes,
                                                                      max_no_of_nodes=self.common_graph_max_no_of_nodes, max_no_of_edges=self.common_graph_max_no_of_edges)
                        generated_common_graph = common_graph_generator.generate_graph()
                        sub_graph_generator = GraphGenerator(generated_common_graph,
                                                             max_no_of_total_nodes=self.max_no_of_total_nodes, max_no_of_total_edges = self.max_no_of_total_edges)  # initialize sub-graph generator with the common graph
                        common_graph_generator.save_nodes_and_edges(os.path.join(folder_path, "common_graph_info.txt"))
                    else:
                        common_graph_generator = CommonGraphGenerator()
                        generated_common_graph = common_graph_generator.generate_graph()
                        sub_graph_generator = GraphGenerator(
                                generated_common_graph)  # initialize sub-graph generator with the common graph
                        common_graph_generator.save_nodes_and_edges(os.path.join(folder_path, "common_graph_info.txt"))
                    print "Common graph generated: N %d, E: %d" % (generated_common_graph.number_of_nodes(), generated_common_graph.number_of_edges())
                    # randomly generate sub-graphs
                    for i in range(1, no_of_graphs_in_the_set + 1):
                        suffix = 'th' if 11 <= i <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(i % 10, 'th')
                        file_name = "%s%s_example_graph.graphml" % (i, suffix)
                        path = os.path.join(folder_path, file_name)
                        print "Processing:" + path
                        generated_graph = sub_graph_generator.generate_graph()
                        sub_graph_generator.save_graph(path)
                        print "Sub graph generated: N %d, E: %d" % (generated_graph.number_of_nodes(), generated_graph.number_of_edges())
                        # post-processed saved graph
                        utils.post_process_graphml(path)
                        utils.save_file(path + ".xml")
                except IOError:
                    print ("Could not save generated graphs.")

    def main(self, argv, generator):
        # process command line arguments
        number_of_graphs = 100
        common_graph_min_no_nodes = 25
        common_graph_max_no_nodes = 40
        common_graph_max_no_edges = 40
        max_no_total_nodes = 40
        max_no_total_edges = 60
        output_folder = "./SetA3"
        error_occurred = False
        instruction = "generate_graphs.py -n <number of graphs> -o <output folder> -m <min no.of nodes of common graph> -x <max no. of nodes of common graph> -t <max total no. of nodes of graphs> " \
                      "-e <max number of edges> -c <common graph max no. edges>"
        try:
            opts, args = getopt.getopt(argv, "hn:o:m:x:t:e:c:",
                                       ["no_of_graphs=", "output=", "common_graph_min_no_of_nodes=",
                                        "common_graph_max_no_of_nodes=", "total_no_of_nodes=", "max_no_of_edges=","common_graph_max_no_edges="])
        except getopt.GetoptError:
            print instruction
            sys.exit(2)

        try:
            for opt, arg in opts:
                if opt == '-h':
                    print instruction
                    sys.exit()
                elif opt in ("-o", "--output"):
                    output_folder = arg
                elif opt in ("-n", "--no_of_graphs"):
                    number_of_graphs = int(arg)
                elif opt in ("-m", "--common_graph_min_no_of_nodes"):
                    common_graph_min_no_nodes = int(arg)
                elif opt in ("-x", "--common_graph_max_no_of_nodes"):
                    common_graph_max_no_nodes = int(arg)
                elif opt in ("-t", "--total_no_of_nodes"):
                    max_no_total_nodes = int(arg)
                elif opt in ("-e", "--max_no_of_edges"):
                    max_no_total_edges = int(arg)
                elif opt in ("-c", "--common_graph_max_no_of_nodes"):
                    common_graph_max_no_edges = int(arg)


        except Exception as e:
            error_occurred = True
            print "Seems like there is a problem with the command-line parameters. Please confrom to the following specification:"
            print instruction
            print "e.g. generate_graphs.py -n 15 -o ./output -m 25 -x 40 -t 40 -e 60 -c 40 "

        if len(opts) == 0:
            print "Warning: Graphs will be generated using the default settings."
        if not error_occurred:
            print "No. of graphs: %d\nMinimum no. of nodes of common graph: %d\nMaximum no. of nodes of common graph: %d\n" \
                  "Maxiumum total number of nodes of graph: %d\nOutput folder: %s\n" % (
                      number_of_graphs, common_graph_min_no_nodes, common_graph_max_no_nodes, max_no_total_nodes,
                      output_folder)

            try:
                generator.set_user_paramters(common_graph_min_no_nodes, common_graph_max_no_nodes, max_no_total_nodes, common_graph_max_no_edges, max_no_total_edges)
                generator.generate_graph_set(output_folder, number_of_graphs)
            except Exception as e:
                print "An error occurred. Please try again with different parameters and ensure the output folder has write permission."
            print "done."


if __name__ == '__main__':
    graph_generator = MainGraphGenerator()
    graph_generator.main(sys.argv[1:], graph_generator)
