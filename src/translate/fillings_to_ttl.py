import pandas as pds
import logging
import os
from load_resources import curr_dir, ohd_ttl, label2uri, load_ada_material_map, load_ada_procedure_map

def print_filling_ttl(practice_id='3', filename='filling.ttl', print_ttl=True, save_ttl=True):

    df_path = os.path.join(curr_dir, '..', 'data', 'Practice1_Fillings.xlsx')
    df = pds.ExcelFile(df_path).parse()
    #df = pds.read_csv(df_path)

    patient_df = df[['PBRN_PRACTICE', 'DB_PRACTICE_ID', 'PATIENT_ID', 'TOOTH_DATA', 'BILLED_SURFACE', 'TRAN_DATE', 'ADA_CODE', 'PROVIDER_ID', 'TABLE_NAME']]

    surface_map = {'m': 'Mesial surface enamel of tooth',
                   'o': 'Occlusal surface enamel of tooth',
                   'b': 'Buccal surface enamel of tooth',
                   'd': 'Distal surface enamel of tooth',
                   'i': 'Incisal surface enamel of tooth',
                   'f': 'Labial surface enamel of tooth',
                   'l': 'Lingual surface enamel of tooth'}

    with open(filename, 'w') as f:
        with open('filling_err.txt', 'w') as f_err:
            # local function for printing and saving turtle output
            def output(value_str, print_ttl=print_ttl, save_ttl=save_ttl):
                if print_ttl == True: print value_str
                if save_ttl == True: f.write(value_str)

            def output_err(value_str):
                f_err.write(value_str)
                f_err.write('\n')

            # output prefixes for ttl file
            prefix_str = ohd_ttl['prefix'].format(practice_id=practice_id)
            output(prefix_str)

            # practice
            practice_uri = ohd_ttl['practice uri'].format(practice_id=practice_id)
            # define types
            practice_type = label2uri['dental health care organization']
            practice_label = "practice_" + str(practice_id)
            # delcare individuals
            output(ohd_ttl['declare practice'].format(uri=practice_uri, type=practice_type, label=practice_label))

            # print ttl for each patient
            for (idx, practiceId, locationId, pid, tooth_data, surface, p_date, ada_code, prov_id, tableName) in patient_df.itertuples():
                if tableName.lower() == 'transactions':
                    ada_code = str(ada_code)
                    #sometimes it has 'D' in front of numbers, sometimes there's no D
                    if not ada_code.startswith('D'):
                        ada_code = str('D') + ada_code

                    tooth_char = list(tooth_data)

                    tooth_idx = 0;
                    for (tooth_yn) in tooth_char:
                        if tooth_yn.lower() == 'y':
                            tooth_num = tooth_idx + 1
                            tooth_id = str(practiceId) + "_" + str(locationId) + "_" + str(pid) + "_" + str(tooth_num)
                            try:
                                procedure_date_str = p_date.strftime('%Y-%m-%d')

                                cdt_code_id = tooth_id + "_" + str(ada_code) + "_" + procedure_date_str
                                patient_id = str(practiceId) + "_" + str(locationId) + "_" + str(pid)
                                patient_uri = ohd_ttl['patient uri by prefix'].format(patient_id=patient_id)
                                provider_id = str(practiceId) + "_" + str(locationId) + "_" + str(prov_id)
                                filling_role_id = str(cdt_code_id) + "_" + str(procedure_date_str)

                                tooth_label = "tooth " + str(tooth_num) + " of patient " + str(pid) # "tooth 13 of patient 1"
                                tooth_str = ohd_ttl['declare tooth by prefix'].format(tooth_id=tooth_id,
                                                                                      specific_tooth=label2uri['tooth ' + str(tooth_num)],
                                                                                      restored_tooth=label2uri['restored tooth'],
                                                                                      label=tooth_label)
                                output(tooth_str)

                                if pds.notnull(surface):
                                    surface_char = list(surface)

                                    #filling role
                                    filling_role_label = "tooth to be restored role for " + tooth_label  # "tooth to be restored role for tooth 13 of patient 1"
                                    filling_role = ohd_ttl['declare filling role'].format(filling_role_id=filling_role_id,
                                                                                          tooth_to_be_filled_role=label2uri['tooth to be filled role'].rsplit('/', 1)[-1],
                                                                                          label=filling_role_label)
                                    output(filling_role)

                                    #restoration procedure
                                    restoration_procedure_label = "restoration procedure on " + tooth_label + " on " + procedure_date_str  #  "restoration procedure on tooth 13 of patient 1 on 2003-05-16"
                                    specific_procedure = label2uri[load_ada_procedure_map[ada_code]].rsplit('/', 1)[-1]
                                    restoration_procedure = ohd_ttl['declare restoration procedure'].format(cdt_code_id=cdt_code_id,
                                                                                                            tooth_restoration_procedure=specific_procedure,
                                                                                                            label=restoration_procedure_label)
                                    output(restoration_procedure)

                                    #restoration material
                                    restoration_material_label = "restoration material placed in " + tooth_label  # "restoration material placed in tooth 13 of patient 1"
                                    specific_material = label2uri[load_ada_material_map[ada_code]].rsplit('/', 1)[-1]
                                    restoration_material = ohd_ttl['declare restoration material'].format(cdt_code_id=cdt_code_id,
                                                                                                          tooth_restoration_material=specific_material,
                                                                                                          label=restoration_material_label)
                                    output(restoration_material)

                                    #restoration material role
                                    restoration_material_role_label = "restoration material role for " + restoration_material_label  # "restoration material role for restoration material placed in tooth 13 of patient 1"
                                    restoration_material_role = ohd_ttl['declare restoration material role'].format(cdt_code_id=cdt_code_id,
                                                                                                                    dental_restoration_material_role=label2uri['dental restoration material role'].rsplit('/', 1)[-1],
                                                                                                                    label=restoration_material_role_label)
                                    output(restoration_material_role)

                                    #billing code
                                    billing_code_label = "billing code " + str(ada_code) + " for procedure on " + procedure_date_str  # "billing code D2160 for procedure on 2003-05-16"
                                    billing_code = ohd_ttl['declare billing code'].format(cdt_code_id=cdt_code_id,
                                                                                          billing_code_for_restorative=label2uri[ada_code.lower()].rsplit('/', 1)[-1],
                                                                                          label=billing_code_label)
                                    output(billing_code)

                                    #relation: tooth part of patient  'uri1 is part of uri2':
                                    tooth_uri = "tooth:" + str(tooth_id)
                                    tooth_patient_relation_str = ohd_ttl['uri1 is part of uri2'].format(uri1=tooth_uri, uri2=patient_uri)
                                    output(tooth_patient_relation_str)

                                    restoration_procedure_uri = "restoration_procedure:" + str(cdt_code_id)

                                    material_uri = "restoration_material:" + str(cdt_code_id)

                                    for (single_surface) in surface_char:
                                        try:
                                            surface_id = tooth_id + "_" + single_surface
                                            specific_surface_str =  surface_map[single_surface.lower()]

                                            surface_filling_role_id = str(surface_id) + "_" + str(cdt_code_id) + "_" + str(procedure_date_str)

                                            surface_label = "surface " + single_surface.upper() + " for " + tooth_label  # "surface M for tooth 13 of patient 1"
                                            surface_str = ohd_ttl['declare surface by prefix'].format(surface_id=surface_id,
                                                                                                      surface_of_tooth=label2uri[specific_surface_str.lower()],
                                                                                                      restored_tooth_surface=label2uri['restored tooth surface'],
                                                                                                      label=surface_label)
                                            output(surface_str)

                                            # surface role
                                            surface_role_label = "surface to be restored role for " + surface_label  # "surface to be restored role for surface M for tooth 13 of patient 1"
                                            surface_role = ohd_ttl['declare surface role'].format(surface_filling_role_id=surface_filling_role_id,
                                                                                                      tooth_surface_to_be_restored_role=label2uri['tooth surface to be restored role'].rsplit('/', 1)[-1],
                                                                                                      label=surface_role_label)
                                            output(surface_role)

                                            #relation: surface part of tooth
                                            surface_uri = "surface:" + str(surface_id)
                                            surface_tooth_relation_str = ohd_ttl['uri1 is part of uri2'].format(uri1=surface_uri, uri2=tooth_uri)
                                            output(surface_tooth_relation_str)
                                            output("\n")

                                            #relation: surface role inheres in tooth
                                            surface_role_uri = "surface_role:" + str(surface_filling_role_id)
                                            surface_role_tooth_relation_str = ohd_ttl['uri1 inheres in uri2'].format(uri1=surface_role_uri, uri2=tooth_uri)
                                            output(surface_role_tooth_relation_str)
                                            output("\n")

                                            #relation: restoration procedure realizes surface role
                                            procedure_filling_role_relation_str = ohd_ttl['uri1 realizes uri2'].format(uri1=restoration_procedure_uri, uri2=surface_role_uri)
                                            output(procedure_filling_role_relation_str)
                                            output("\n")

                                            #relation: restoration procedure has specified output surface
                                            procedure_surface_relation_str = ohd_ttl['uri1 has specified output uri2'].format(uri1=restoration_procedure_uri, uri2=surface_uri)
                                            output(procedure_surface_relation_str)
                                            output("\n")

                                            #relaton: material is dental restoration of surface
                                            material_tooth_relation_str = ohd_ttl['ur1 is dental restoration of uri2'].format(uri1=material_uri, uri2=surface_uri)
                                            output(material_tooth_relation_str)
                                            output("\n")
                                        except Exception as ex1:
                                            output_err("Problem surface: " + surface_id)
                                            print("Problem surface: " + surface_id)
                                            logging.exception("message")

                                    #relation: material located in tooth
                                    material_tooth_relation_str = ohd_ttl['uri1 is located in uri2'].format(uri1=material_uri, uri2=tooth_uri)
                                    output(material_tooth_relation_str)
                                    output("\n")

                                    #relation: filling role inderes tooth
                                    filling_role_uri = "filling_role:" + str(filling_role_id)
                                    filling_role_tooth_relation_str = ohd_ttl['uri1 inheres in uri2'].format(uri1=filling_role_uri, uri2=tooth_uri)
                                    output(filling_role_tooth_relation_str)
                                    output("\n")

                                    #relation: restoration procedure realizes patient role
                                    patient_role_uri = ohd_ttl['patient role uri by prefix'].format(patient_id=patient_id)
                                    procedure_patient_role_relation_str = ohd_ttl['uri1 realizes uri2'].format(uri1=restoration_procedure_uri, uri2=patient_role_uri)
                                    output(procedure_patient_role_relation_str)
                                    output("\n")

                                    #relation: restoration procedure realizes provider role
                                    provider_role_uri = "provider_role:" + str(provider_id)
                                    procedure_provider_role_relation_str = ohd_ttl['uri1 realizes uri2'].format(uri1=restoration_procedure_uri, uri2=provider_role_uri)
                                    output(procedure_provider_role_relation_str)
                                    output("\n")

                                    #relation: restoration procedure realizes filling role
                                    filling_role_uri = "filling_role:" + str(cdt_code_id)
                                    procedure_filling_role_relation_str = ohd_ttl['uri1 realizes uri2'].format(uri1=restoration_procedure_uri, uri2=filling_role_uri)
                                    output(procedure_filling_role_relation_str)
                                    output("\n")

                                    #relation: restoration procedur realizes restoration material role
                                    restoration_material_role_uri = "restoration_material_role:" + str(cdt_code_id)
                                    procedure_material_role_relation_str = ohd_ttl['uri1 realizes uri2'].format(uri1=restoration_procedure_uri, uri2=restoration_material_role_uri)
                                    output(procedure_material_role_relation_str)
                                    output("\n")

                                    #relation: restoration procedure has specified output tooth
                                    procedure_tooth_relation_str = ohd_ttl['uri1 has specified output uri2'].format(uri1=restoration_procedure_uri, uri2=tooth_uri)
                                    output(procedure_tooth_relation_str)
                                    output("\n")

                                    #relation: procedure has specified input tooth
                                    procedure_input_tooth_relation_str = ohd_ttl['uri1 has specified input uri2'].format(uri1=restoration_procedure_uri, uri2=tooth_uri)
                                    output(procedure_input_tooth_relation_str)
                                    output("\n")

                                    #relation: procedure has specified input material
                                    procedure_input_material_relation_str = ohd_ttl['uri1 has specified input uri2'].format(uri1=restoration_procedure_uri, uri2=material_uri)
                                    output(procedure_input_material_relation_str)
                                    output("\n")

                                    #relation: cdt code is about restoration procedure
                                    cdt_code_uri = "cdt_code:" + str(cdt_code_id)
                                    cdt_code_procedure_relation_str = ohd_ttl['uri1 is about uri2'].format(uri1=cdt_code_uri, uri2=restoration_procedure_uri)
                                    output(cdt_code_procedure_relation_str)
                                    output("\n")
                            except Exception as ex:
                                output_err("Problem tooth_id: " + tooth_id)
                                print("Problem tooth_id: " + tooth_id )
                                logging.exception("message")

                        tooth_idx = tooth_idx + 1

print_filling_ttl(practice_id='1')