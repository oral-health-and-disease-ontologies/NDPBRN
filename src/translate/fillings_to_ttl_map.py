import pandas as pds
import logging
import os
from load_resources import curr_dir, ohd_ttl, label2uri, load_ada_material_map, load_ada_procedure_map

import pandas as pd

def field_map(practice_id='1', filename='filling_mapped.ttl'):
    fmap = \
        {
            "tooth": {
                "triples": [
                    {
                        "subj": "tooth:{tooth_id}",
                        "pred": "rdf:type",
                        "obj": "<{tooth_type}>"
                    },
                    {
                        "subj": "tooth:{tooth_id}",
                        "pred": "rdf:type",
                        "obj": "<http://purl.obolibrary.org/obo/OHD_0000189>"
                    },
                    {
                        "subj": "tooth:{tooth_id}",
                        "pred": "rdfs:label",
                        "obj": "\"{tooth_label}\"^^xsd:string"
                    }
                ]
            },
            "surface":{
                "triples": [
                    {
                        "subj": "surface:{surface_id}",
                        "pred": "rdf:type",
                        "obj": "<{surface_of_tooth}>"
                    },
                    {
                        "subj": "surface:{surface_id}",
                        "pred": "rdf:type",
                        "obj": "<http://purl.obolibrary.org/obo/OHD_0000208>"
                    },
                    {
                        "subj": "surface:{surface_id}",
                        "pred": "rdfs:label",
                        "obj": "\"{surface_label}\"^^xsd:string"
                    }
                ]
            },
            "surfacing_role":{
                "triples": [
                    {
                        "subj": "surfacing_role:{surface_filling_role_id}",
                        "pred": "rdf:type",
                        "obj": "obo:OHD_0000207"
                    },
                    {
                        "subj": "surfacing_role:{surface_filling_role_id}",
                        "pred": "rdfs:label",
                        "obj": "\"{surfacing_role_label}\"^^xsd:string"
                    }
                ]
            },
            "filling_role":{
                "triples": [
                    {
                        "subj": "filling_role:{filling_role_id}",
                        "pred": "rdf:type",
                        "obj": "<http://purl.obolibrary.org/obo/OHD_0000008>"
                    },
                    {
                        "subj": "filling_role:{filling_role_id}",
                        "pred": "rdfs:label",
                        "obj": "\"{filling_role_label}\"^^xsd:string"
                    }
                ]
            },
            "restoration_procedure":{
                "triples": [
                    {
                        "subj": "restoration_procedure:{cdt_code_id}",
                        "pred": "rdf:type",
                        "obj": "obo:{tooth_restoration_procedure}"
                    },
                    {
                        "subj": "restoration_procedure:{cdt_code_id}",
                        "pred": "rdfs:label",
                        "obj": "\"{restoration_procedure_label}\"^^xsd:string"
                    }
                ]
            },
            "restoration_material":{
                "triples": [
                    {
                        "subj": "restoration_material:{cdt_code_id}",
                        "pred": "rdf:type",
                        "obj": "obo:{tooth_restoration_material}"
                    },
                    {
                        "subj": "restoration_material:{cdt_code_id}",
                        "pred": "rdfs:label",
                        "obj": "\"{restoration_material_label}\"^^xsd:string"
                    }
                ]
            },
            "cdt_code":{
                "triples": [
                    {
                        "subj": "cdt_code:{cdt_code_id}",
                        "pred": "rdf:type",
                        "obj": "<{billing_code}>"
                    },
                    {
                        "subj": "cdt_code:{cdt_code_id}",
                        "pred": "rdfs:label",
                        "obj": "\"{billing_code_label}\"^^xsd:string"
                    }
                ]
            }
        }

    df_path = os.path.join(curr_dir, '..', 'data', 'Practice1_Fillings.xlsx')
    df = pds.ExcelFile(df_path).parse()

    with open(filename, 'w') as f:
        with open('filling_err_mapped.txt', 'w') as f_err:

            # output prefixes for ttl file
            prefix_str = ohd_ttl['prefix'].format(practice_id=practice_id)
            print prefix_str
            f.write(prefix_str)

            df = tooth_and_surface_rows_df(df, f_err)
            for (x, practiceId, locationId, pid, tooth_data, surface, p_date, prov_id, tableName, ada_code,
                 patient_id, tooth_id, tooth_type, tooth_label, surface_id, surface_of_tooth, surface_label) in df.itertuples():
                print_triples(f, fmap, "tooth", tooth_id=tooth_id, tooth_type=tooth_type, tooth_label=tooth_label)
                print_triples(f, fmap, "surface", surface_id=surface_id, surface_of_tooth=surface_of_tooth, surface_label=surface_label)

def print_triples(file, fmap, field, **kwargs):

    triples = fmap[field]["triples"]

    for triple in triples:

        subj = triple["subj"].format(**kwargs)
        pred = triple["pred"].format(**kwargs)
        obj = triple["obj"].format(**kwargs)

        print subj + " " + pred + " " + obj
        file.write(subj + " " + pred + " " + obj + "\n")


def tooth_and_surface_rows_df(df, f_err):
    surface_map = {'m': 'Mesial surface enamel of tooth',
                   'o': 'Occlusal surface enamel of tooth',
                   'b': 'Buccal surface enamel of tooth',
                   'd': 'Distal surface enamel of tooth',
                   'i': 'Incisal surface enamel of tooth',
                   'f': 'Labial surface enamel of tooth',
                   'l': 'Lingual surface enamel of tooth'}

    def output_err(value_str):
        f_err.write(value_str)
        f_err.write('\n')

    ## iterate over df and create a new list containing patient, tooth, and a surface letter
    results = []
    for (x, practiceId, locationId, pid, tooth_data, surface, p_date, ada_code, prov_id, tableName) in df[
            ['PBRN_PRACTICE', 'DB_PRACTICE_ID', 'PATIENT_ID', 'TOOTH_DATA', 'BILLED_SURFACE', 'TRAN_DATE', 'ADA_CODE',
             'PROVIDER_ID', 'TABLE_NAME']].itertuples():
        if tableName.lower() == 'transactions':
            row = [practiceId, locationId, pid, tooth_data, surface, p_date, prov_id, tableName]

            ada_code = str(ada_code)
            # sometimes it has 'D' in front of numbers, sometimes there's no D
            if not ada_code.startswith('D'):
                ada_code = str('D') + ada_code

            row = row + [ada_code]

            tooth_char = list(tooth_data)

            tooth_idx = 0;
            for (tooth_yn) in tooth_char:
                if tooth_yn.lower() == 'y':
                    tooth_num = tooth_idx + 1
                    tooth_id = str(practiceId) + "_" + str(locationId) + "_" + str(pid) + "_" + str(tooth_num)

                    row = row + [tooth_id]

                    patient_id = str(practiceId) + "_" + str(locationId) + "_" + str(pid)
                    tooth_label = "tooth " + str(tooth_num) + " of patient " + str(pid)  # "tooth 13 of patient 1"
                    tooth_type = label2uri['tooth ' + str(tooth_num)]

                    row = row + [patient_id]
                    row = row + [tooth_type]
                    row = row + [tooth_label]

                    if pds.notnull(surface):
                        surface_char = list(surface)
                        for (single_surface) in surface_char:
                            try:
                                surface_id = tooth_id + "_" + single_surface

                                surface_label = surface_map[single_surface.lower()] + " for " + tooth_label  # "Mesial surface enamel of tooth for tooth 1 of patient 1"

                                specific_surface_str = surface_map[single_surface.lower()]

                                surface_of_tooth=label2uri[specific_surface_str.lower()]

                                results.append(row + [surface_id] + [surface_of_tooth] + [surface_label])
                            except Exception as ex1:
                                output_err("Problem surface: " + surface_id)
                                print("Problem surface: " + surface_id)
                                logging.exception("message")

    return pd.DataFrame(results, columns=['practiceId', 'locationId', 'pid', 'tooth_data', 'surface', 'p_date',
                                          'prov_id', 'tableName', 'ada_code', 'patient_id', 'tooth_id', 'tooth_type',
                                          'tooth_label', 'surface_id', 'surface_of_tooth', 'surface_label'])


field_map()