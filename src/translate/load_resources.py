import os
from os import sys, path

# in order to run this script from the command line (e.g., python load_resources.py)
# you need to add the path to the util directory to the system path
# the curr_dir variable is just an easy way to store the current directory
curr_dir = os.path.dirname(os.path.abspath(__file__)) # path to current directory of file
sys.path.append(path.join(path.dirname(curr_dir), 'util')) # util directory
sys.path.append(path.join(path.dirname(curr_dir), '../'))
sys.path.append(path.join(path.dirname(curr_dir), '../../'))
sys.path.append(path.join(path.dirname(curr_dir), '../util'))

# print "path %s" % sys.path # used for debugging

# this module is dynamically loaded based on the sys.path information
# import ohd_label2uri
import src.util.ohd_label2uri as ohd_label2uri

# build ohd turtle template map
ohd_ttl_path = os.path.join(curr_dir, '..', 'util', 'ohd_template.txt')
ohd_ttl = eval(open(ohd_ttl_path).read())

label2uri_path = os.path.join(curr_dir, '..', 'util')
label2uri = ohd_label2uri.load_label2uri(filepath=label2uri_path)

ada_code_map=ohd_label2uri.load_ada_code_map(filepath=label2uri_path)
#load_ada_filling_material_map=ohd_label2uri.load_ada_filling_material_map(filepath=label2uri_path)
#load_ada_endodontic_material_map=ohd_label2uri.load_ada_endodontic_material_map(filepath=label2uri_path)
#load_ada_inlay_material_map=ohd_label2uri.load_ada_inlay_material_map(filepath=label2uri_path)
#load_ada_onlay_material_map=ohd_label2uri.load_ada_onlay_material_map(filepath=label2uri_path)
#load_ada_procedure_map=ohd_label2uri.load_ada_procedure_map(filepath=label2uri_path)
#load_ada_apicoectomy_material_map=ohd_label2uri.load_ada_apicoectomy_material_map(filepath=label2uri_path)
#load_ada_root_amputation_material_map=ohd_label2uri.load_ada_root_amputation_material_map(filepath=label2uri_path)
load_ada_filling_material_map=ohd_label2uri.load_ada_procedure_material_map(filepath=label2uri_path, procedure_type_name='filling')
load_ada_endodontic_material_map=ohd_label2uri.load_ada_procedure_material_map(filepath=label2uri_path, procedure_type_name='endodontic')
load_ada_inlay_material_map=ohd_label2uri.load_ada_procedure_material_map(filepath=label2uri_path, procedure_type_name='inlay')
load_ada_onlay_material_map=ohd_label2uri.load_ada_procedure_material_map(filepath=label2uri_path, procedure_type_name='onlay')
load_ada_procedure_map=ohd_label2uri.load_ada_procedure_map(filepath=label2uri_path)
load_ada_apicoectomy_material_map=ohd_label2uri.load_ada_procedure_material_map(filepath=label2uri_path, procedure_type_name='apicoectomy')
load_ada_root_amputation_material_map=ohd_label2uri.load_ada_procedure_material_map(filepath=label2uri_path, procedure_type_name='root_amputation')
load_ada_crown_material_map=ohd_label2uri.load_ada_procedure_material_map(filepath=label2uri_path, procedure_type_name='crown')