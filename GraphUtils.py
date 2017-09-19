from pathlib import Path
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

class GraphUtils:
    """
    This class post process generated .graphml files. It will perform a number of operations:
    1) replace networkx generated attribute keys with predefined(user defined) attribute_names (key and data)
    2) remove auto generated graph name attribute and relevant data
    3) adds custom defined graph name for the graph
    TODO: Currently uses xpath to locate features of the xml file to be post-processed. This needs optimisation.
    TODO: Implements minimal validation of external input. Need to fix this.
    """
    def __init__(self):
        self.xml_doc = None                                                 # holds currently parsed xml document
        self.namespaces = {'gml': 'http://graphml.graphdrawing.org/xmlns'}  # namespace used, add more as needed
        self.file_name = "temp"                                             # file name to save the postprocessed output

    def replace_id(self, attribute_name, graph = True):
        """
        :param attribute_name: attribute_name to be replaced as an id
        :param graph: whether attribute is applicable for graph or for nodes
        :return: None
        """
        if graph:
            element = "graph"
        else:
            element = "node"

        for e in  self.xml_doc.findall(".//gml:key[@attr.name='"+attribute_name+"'][@for='"+element+"']", self.namespaces):
            id = e.attrib.get('id')
            e.set('id', attribute_name)


        for e in  self.xml_doc.findall(".//gml:data[@key='"+id+"']", self.namespaces):
            e.set('key', attribute_name)
            if attribute_name == 'designName':
                #extract designName while we process the replacement of ids. This will be used for file name
                self.file_name = e.text.lower().replace(' ','_')+"_graph"
            if attribute_name == 'price':
                #format price with two decimal places
                val = float(e.text)
                e.text = "%.2f" % val
            if attribute_name == 'mpg' or attribute_name== 'horsepower':
                #format horsepower as one decimal place
                val = float(e.text)
                e.text = "%.1f" % val


    def remove_graph_name(self):
        """
        Remove auto-generated networkx graph name and data elements.
        :return: None
        """
        root = self.xml_doc.getroot()
        for e in  self.xml_doc.findall(".//gml:key[@attr.name='name'][@for='graph']", self.namespaces):
            id = e.attrib.get('id')
            root.remove(e)

        graph_element = root.find('gml:graph', self.namespaces)

        for e in  self.xml_doc.findall(".//gml:data[@key='"+id+"']", self.namespaces):
            graph_element.remove(e)

    def add_graph_id(self, file_name):
        """
        Add custom defined graph id - set it to file_name
        :param file_name: file path
        :return:None
        """
        root = self.xml_doc.getroot()
        graph_element = root.find('gml:graph', self.namespaces)
        graph_element.set('id',file_name)

    def re_compute_node_ids(self):
        for e in  self.xml_doc.findall(".//gml:node", self.namespaces):
            id = int(e.attrib.get('id'))+1
            e.set('id', str(id))

    def add_edge_ids(self):
        """
        By default generated edges have no ids. So create them sequentially.
        :return: None
        """
        id = 0
        for e in  self.xml_doc.findall(".//gml:edge", self.namespaces):
            id += 1
            e.set('id', str(id))
            #node ids are initally numbered from 0, make them starting 1 (in edges)
            source_id = str(int(e.attrib.get('source'))+1)
            target_id = str(int(e.attrib.get('target'))+1)
            e.set('source', source_id)
            e.set('target', target_id)


    def remove_namespace(self):
        """Remove namespace in the passed document in place before saving the postprocssed XML"""
        ns = u'{http://graphml.graphdrawing.org/xmlns}'
        nsl = len(ns)
        for elem in self.xml_doc.getiterator():
            if elem.tag.startswith(ns):
                elem.tag = elem.tag[nsl:]

    def add_namespace(self):
        """
        Only add the graphml namespace as the default.
        :return: None
        """
        root = self.xml_doc.getroot()
        root.set('xlmns','http://graphml.graphdrawing.org/xmlns')

    def post_process_graphml(self, file_path):
        """
        Main procedure for postprocessing generated .graphml (convert from .graphml to .xml)
        :param file_path: generated .graphml file to be post-processed
        :return:None.
        """
        if file_path:
            path = Path(file_path)
            if path.is_file():

                try:
                    self.xml_doc = ET.parse(file_path)
                    attributes = ['designName','serie','target_market','drive_wheels','battery_type','price','horsepower','mpg','cylinder',
                                 'engine_size','controller','isDiesel','hasTurbo', 'isPlugin']
                    for attribute in attributes:
                        self.replace_id(attribute) #replace ids of all the pre-defined attributes with attribute name

                    #process node attributes
                    attributes = ['name','type']
                    for attribute in attributes:
                        self.replace_id(attribute,False)

                    self.remove_graph_name()

                    file_name = self.file_name #path.name[:path.name.rfind('.graphml')]+".xml"
                    self.add_graph_id(file_name)

                    self.re_compute_node_ids()

                    self.add_edge_ids()

                    self.remove_namespace()

                    self.add_namespace()
                except ParseError:
                    print("Unable to parse the given GraphML file.")


            else:
                raise IOError("File path error! Could not locate file in: " + file_path + ".")
        else:
            raise Exception("Empty file path!")

    def save_file(self, file_name):
        """
        :param file_name: file to be saved (save a copy of the postprocessed file)
        :return: None
        """
        self.xml_doc.write(open(file_name,'w'), encoding='utf8')
        #self.xml_doc.write(file_name, pretty_print = True, encoding='utf8')

