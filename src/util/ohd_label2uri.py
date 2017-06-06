import os
import rdflib
from rdflib import ConjunctiveGraph, URIRef, RDFS, Literal
from datetime import datetime

def load_label2uri(force=False, filepath=__file__, filename='label2uri.txt'):
    # create and the lable2uri under the following two coditions:
    # the file does NOT exist OR force is True
    # label2uri_full_name = os.path.join(filepath, filename)
    label2uri_full_name = os.path.join(os.path.abspath('.'), filename)
    if force == True or os.path.exists(label2uri_full_name) == False:
        # print "creating map"
        # make the label2uri map
        label2uri = make_ohd_label2uri()

        # write label2uri to file
        write_label2uri(label2uri, label2uri_full_name)

    # otherwise read label2uri from file
    else:
        # print "load from file"
        label2uri = eval(open(label2uri_full_name).read())

    # return label2uri
    return label2uri

def write_label2uri(label2uri, filename='label2uri.txt'):
    # save label2uri to file
    with open(filename, 'w') as f:
        f.write(str(label2uri)) # note: label2uri is converted to string

def make_ohd_label2uri():
    # get path to ohd onotology
    curr_dir = os.path.join(os.path.dirname(__file__)) # path to current directory of file
    ohd_path = os.path.join(curr_dir, '..', '..', 'ontology', 'NDPBRN.owl')

    # build graph
    g = rdflib.Graph()
    g.parse(ohd_path)

    # add mapping: lowercase label -> uri
    label2uri = {}
    for uri, p, label in g.triples((None, RDFS.label, None)):
        label2uri[str(label).lower()] = str(uri)

    # add mapping to ADA universal tooth number (e.g., tooth 1, tooth 2, etc.)
    # http://purl.obolibrary.org/obo/OHD_0000065 is uri for the 'ADA universal tooth number' annotation
    for (uri, tooth_num) in g.query(
            "select ?uri ?tooth_num where {?uri <http://purl.obolibrary.org/obo/OHD_0000065> ?tooth_num}"):
        label2uri[str(tooth_num).lower()] = str(uri)

    # add mapping from CDT Code (e.g., D2140) to the uri of the CDT Code class
    # e.g.: 'D2140' -> http://purl.obolibrary.org/obo/CDT_0002140
    # http://purl.org/dc/elements/1.1/identifier is uri for the 'dc:identifier' annotation
    for (uri, cdt_code) in g.query(
            "select ?uri ?cdt_code where {?uri <http://purl.org/dc/elements/1.1/identifier> ?cdt_code}"):
        label2uri[str(cdt_code).lower()] = str(uri)

    # add mapping to prosthetic tooth numbers (e.g., prosthetic tooth 1, prosthetic tooth 2, etc.)
    # http://purl.obolibrary.org/obo/OHD_0000302 is the uri for the class 'prothetic tooth'
    # http://purl.obolibrary.org/obo/IAO_0000118 is uri for the 'alternaive term' annotation
    for (uri, tooth_num) in g.query(
            "select ?uri ?tooth_num where { " +
                    "?uri rdfs:subClassOf <http://purl.obolibrary.org/obo/OHD_0000302> . " +
                    "?uri <http://purl.obolibrary.org/obo/IAO_0000118> ?tooth_num . }"):
        label2uri[str(tooth_num).lower()] = str(uri)

    # return label2uri map
    return label2uri

def load_ada_code_map(filepath=os.path.dirname(__file__), filename='ada_code_map.txt'):
    file_full_name = os.path.join(filepath, filename)
    ada_code_map = eval(open(file_full_name).read())

    return ada_code_map

#def load_ada_filling_material_map(filepath=os.path.dirname(__file__), filename='ada_code_filling_material_map.txt'):
#    file_full_name = os.path.join(filepath, filename)
#    ada_filling_material_map = eval(open(file_full_name).read())
#
#    return ada_filling_material_map

#def load_ada_endodontic_material_map(filepath=os.path.dirname(__file__), filename='ada_code_endodontic_material_map.txt'):
#    file_full_name = os.path.join(filepath, filename)
#    ada_endodontic_material_map = eval(open(file_full_name).read())
#
#    return ada_endodontic_material_map

#def load_ada_inlay_material_map(filepath=os.path.dirname(__file__), filename='ada_code_inlay_material_map.txt'):
#    file_full_name = os.path.join(filepath, filename)
#    ada_inlay_material_map = eval(open(file_full_name).read())
#
#    return ada_inlay_material_map

#def load_ada_onlay_material_map(filepath=os.path.dirname(__file__), filename='ada_code_onlay_material_map.txt'):
#    file_full_name = os.path.join(filepath, filename)
#    ada_onlay_material_map = eval(open(file_full_name).read())
#
#    return ada_onlay_material_map

#def load_ada_apicoectomy_material_map(filepath=os.path.dirname(__file__), filename='ada_code_apicoectomy_material_map.txt'):
#    file_full_name = os.path.join(filepath, filename)
#    ada_apicoectomy_material_map = eval(open(file_full_name).read())

#    return ada_apicoectomy_material_map

#def load_ada_root_amputation_material_map(filepath=os.path.dirname(__file__), filename='ada_code_root_amputation_material_map.txt'):
#    file_full_name = os.path.join(filepath, filename)
#    ada_root_amputation_material_map = eval(open(file_full_name).read())
#
#    return ada_root_amputation_material_map

def load_ada_procedure_material_map(filepath=os.path.dirname(__file__), procedure_type_name='filling'):
    filename = 'ada_code_' + procedure_type_name + '_material_map.txt'
    file_full_name = os.path.join(filepath, filename)
    ada_material_map = eval(open(file_full_name).read())

    return ada_material_map

def load_ada_procedure_map(filepath=os.path.dirname(__file__), filename='ada_code_procedure_map.txt'):
    file_full_name = os.path.join(filepath, filename)
    ada_procedure_map = eval(open(file_full_name).read())

    return ada_procedure_map

def test_label2uri():
    d = make_ohd_label2uri()
    print d['surface enamel of tooth'] # works
    print d['tooth 1'] # works
    print d['d2140'] # works
    print d['occlusal surface enamel of tooth']

def get_date_str(date_input_str):
    try:
        date_str = str(datetime.strptime(date_input_str, '%Y-%m-%d').date())
    except Exception as ex:
        date_str = 'invalid date'
    return date_str

load_label2uri(force=True)
# test_label2uri()
# load_ada_code_map()
# test_map = load_ada_procedure_map()
# print test_map()