# -*- coding: utf-8 -*-
import xmlschema
from pprint import pprint


def LerXML(arq):
    xs = xmlschema.XMLSchema('instancia2.xsd')
    #print "XML válido: {}".format(xs.is_valid(arq))
    b = xs.to_dict(arq)
    #pprint(b)
    my_dict = xs.to_dict(arq)
    return my_dict

def LerXMLGen(arq):
    xs = xmlschema.XMLSchema('gerafile.xsd')
    print(xs.is_valid(arq))
    pprint(xs.to_dict(arq))
    my_dict = xs.to_dict(arq)
    return my_dict

def LerXMLConf(arq):
    xs = xmlschema.XMLSchema('conf.xsd')
    print(xs.is_valid(arq))
    pprint(xs.to_dict(arq))
    my_dict = xs.to_dict(arq)
    return my_dict
