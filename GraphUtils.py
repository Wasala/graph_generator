from pathlib import Path
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

class GraphUtils:
    def __init__(self):
        self.xml_doc = None
        self.namespaces = {'gml': 'http://graphml.graphdrawing.org/xmlns'} # add more as needed
        self.file_name = "temp"

    def replace_id(self, attribute_name, graph = True):
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
                self.file_name = e.text.lower().replace(' ','_')+"_graph"
            if attribute_name == 'price':
                val = float(e.text)
                e.text = "%.2f" % val
            if attribute_name == 'mpg' or attribute_name== 'horsepower':
                val = float(e.text)
                e.text = "%.1f" % val


    def remove_graph_name(self):
        root = self.xml_doc.getroot()
        for e in  self.xml_doc.findall(".//gml:key[@attr.name='name'][@for='graph']", self.namespaces):
            id = e.attrib.get('id')
            root.remove(e)

        graph_element = root.find('gml:graph', self.namespaces)

        for e in  self.xml_doc.findall(".//gml:data[@key='"+id+"']", self.namespaces):
            graph_element.remove(e)

    def add_graph_id(self, file_name):
        root = self.xml_doc.getroot()
        graph_element = root.find('gml:graph', self.namespaces)
        graph_element.set('id',file_name)

    def re_compute_node_ids(self):
        for e in  self.xml_doc.findall(".//gml:node", self.namespaces):
            id = int(e.attrib.get('id'))+1
            e.set('id', str(id))

    def add_edge_ids(self):
        id = 0
        for e in  self.xml_doc.findall(".//gml:edge", self.namespaces):
            id += 1
            e.set('id', str(id))
            source_id = str(int(e.attrib.get('source'))+1)
            target_id = str(int(e.attrib.get('target'))+1)
            e.set('source', source_id)
            e.set('target', target_id)


    def remove_namespace(self):
        """Remove namespace in the passed document in place."""
        ns = u'{http://graphml.graphdrawing.org/xmlns}'
        nsl = len(ns)
        for elem in self.xml_doc.getiterator():
            if elem.tag.startswith(ns):
                elem.tag = elem.tag[nsl:]

    def add_namespace(self):
        root = self.xml_doc.getroot()
        root.set('xlmns','http://graphml.graphdrawing.org/xmlns')

    def post_process_graphml(self, file_path):
            if file_path:
                path = Path(file_path)
                if path.is_file():

                    try:
                        self.xml_doc = ET.parse(file_path)
                        attributes = ['designName','serie','target_market','drive_wheels','battery_type','price','horsepower','mpg','cylinder',
                                     'engine_size','controller','isDiesel','hasTurbo', 'isPluging']
                        for attribute in attributes:
                            self.replace_id(attribute)

                        #process node attributes
                        attributes = ['name','type']
                        for attribute in attributes:
                            self.replace_id(attribute,False)

                        self.remove_graph_name()

                        file_name = self.file_name#path.name[:path.name.rfind('.graphml')]+".xml"
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
        self.xml_doc.write(open(file_name,'w'), encoding='utf8')
        #self.xml_doc.write(file_name, pretty_print = True, encoding='utf8')

