#'''''''''''''''''''''''''''''''''''''''''''
# GLOBAL IMPORTS
#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

import argparse
import pprint
from lxml import etree

#'''''''''''''''''''''''''''''''''''''''''''
# GLOBAL VARIABLES
#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

VERBOSE = False

#'''''''''''''''''''''''''''''''''''''''''''
# ARGUMENTS
#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

def _GetArguments():
    '''
    Reterive parsed arguments.
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        help="increase output verbosity")

    parser.add_argument("files", nargs="*")

    args = parser.parse_args()

    if args.verbose:
        global VERBOSE
        VERBOSE = True
        _vprint("VERBOSE MODE is on.")

    return args

#'''''''''''''''''''''''''''''''''''''''''''
# UTILITY FUNCTIONS
#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

def _vprint(data, info = ''):
    global VERBOSE
    if VERBOSE:
        if info == '':
            pprint.pprint(data)
        else:
            pprint.pprint(info + " - " + data)

#'''''''''''''''''''''''''''''''''''''''''''
# CLASSES
#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

class XMLParser(object):
    _INDENT_ELEMENT = '----'
    _INDENT_ATTRIB  = '-'
    _ATTRIBDICT     = '_attrib'

    def __init__(self, filename):
        '''
        Description
            xml parser object with useful XML Parsing functions
            
        Core functions
            Dendrogram() : print XML in dendrogram style
            AsDict()     : return XML as python dict
        '''
        self._filename = filename
        self._file = None
        self._tree = None
    
    @property
    def filename(self):
        return self.filename

    @filename.setter
    def filename(self, filename):
        self.filename = filename

    def OpenXML(self):
        _vprint(self._filename, "Loaded filename")
        self._file = open(self._filename, 'r')
        
    def LoadXML(self):
        content = self._file.read()
        _vprint(content, "Loaded content of XML")
        self._tree = etree.XML(content)

    def CloseXML(self):
        _vprint("Closing the XML...")
        self._file.close()
    
    def Dendrogram(self):
        self._PrintXML(self, self._tree)
    
    def _Dendro(node, indent = ''):
        '''
           Recursive function to print all the XML data
           As Dendrogram style
           -----------------------
           Root
                Child -tag
                Child -attrib
                    Child-tag
                    Child-attrib
                        ...(so on)
           -----------------------
        '''
        if node is None:
            return
        
        for child in node:
            indent = indent + self._INDENT_ELEMENT
            print indent, child.tag
            print indent + self._INDENT_ATTRIB, child.text
            print indent + self._INDENT_ATTRIB, child.attrib
            self._Dendro(child, indent)

    def AsDict(self):
        tmpDict = {}
        self._AsDict(self, self._tree, tmpDict)


    def _AsDict(self, node, dict):
        '''
            Recursive function to store all the XML data
            into python dictionary
            -----------------------
                Elem -tag    : string (tag's text info)
                Elem -attrib : dict   (attrib comes in as dict)
                Elem -child  : dict   (name will be dict_tag)
                    Elem -tag    : string
                    Elem -attrib : dict
                    Elem -child  : dict
                        ...(so on)
            -----------------------
        '''
        if node is None:
            return
    
        dict[node.tag] = node.text
        if node.attrib:
            # attrib comes as dict so store it under node tag_attrib
            dict[node.tag + self._ATTRIBDICT] = node.attrib
    
        for child in node:
            dict[node.tag + child.tag] = {}
            self._AsDict(child, dict[node.tag + child.tag])

#'''''''''''''''''''''''''''''''''''''''''''
# MAIN FUNCTIONS
#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

def main():
    # Parse arg init
    args = _GetArguments()
    xmlDicts = []

    for file in args.files:
        xmlTest = XMLPrinter(file)
        xmlTest.OpenXML()
        xmlTest.LoadXML()
        xmlTest.Dendrogram()
        xmlDicts.append(xmlTest.AsDict())
        xmlTest.CloseXML()

    for dict in xmlDicts:
        pprint.pprint(dict)

if __name__ == "__main__":
    sys.exit(main())

        
        
    
    
