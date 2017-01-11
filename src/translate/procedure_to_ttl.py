import pandas as pds
import logging
import os
from load_resources import curr_dir, ohd_ttl, label2uri, load_ada_filling_material_map, load_ada_endodontic_material_map, load_ada_procedure_map

def print_procedure_ttl(practice_id='3', filename='filling.ttl', print_ttl=True, save_ttl=True, procedure_type=1):

#    df_path = os.path.join(curr_dir, '..', 'data', 'Practice1_Fillings.xlsx')
    #df_path = os.path.join(curr_dir, '..', 'data', 'Practice1_Patient_History.xlsx')
    df_path = os.path.join(curr_dir, '..', 'data', 'Practice' + str(practice_id) + '_Patient_History.xlsx')
    df = pds.ExcelFile(df_path).parse()
    #df = pds.read_csv(df_path)

    patient_df = df[['PBRN_PRACTICE', 'DB_PRACTICE_ID', 'PATIENT_ID', 'TOOTH', 'SURFACE', 'TRAN_DATE', 'ADA_CODE', 'PROVIDER_ID', 'TABLE_NAME']]

    procedure_type_map = {'1': 'filling',
                   '2': 'endodontic',
                   '3': 'inlays',
                   '4': 'onlays'}

    surface_map = {'m': 'Mesial surface enamel of tooth',
                   'o': 'Occlusal surface enamel of tooth',
                   'b': 'Buccal surface enamel of tooth',
                   'd': 'Distal surface enamel of tooth',
                   'i': 'Incisal surface enamel of tooth',
                   'f': 'Labial surface enamel of tooth',
                   'l': 'Lingual surface enamel of tooth'}

    restored_tooth_surface_label_map = {'b': 'restored buccal surface',
                                        'd': 'restored distal surface',
                                        'i': 'restored incisal surface',
                                        'f': 'restored labial surface',
                                        'l': 'restored lingual surface',
                                        'm': 'restored mesial surface',
                                        'o': 'restored occlusal surface'
    }


    # filters on procedure_type by procedure_type_map and create filenames for ttl and err text file
    try:
        filename = procedure_type_map[str(procedure_type)] + '.ttl'
        err_filename = procedure_type_map[str(procedure_type)] + '_err.txt'
    except Exception as ex:  # invalid procedure_type: stop processing here
        print("Invalid procedure type: " + str(procedure_type))
        logging.exception("message")
        return

    with open(filename, 'w') as f:
        with open(err_filename, 'w') as f_err:
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
            for (idx, practiceId, locationId, pid, tooth_num, surface, p_date, ada_code, prov_id, tableName) in patient_df.itertuples():
                if tableName.lower() == 'transactions':
                    ada_code = str(ada_code)
                    #sometimes it has 'D' in front of numbers, sometimes there's no D
                    if not ada_code.startswith('D'):
                        ada_code = str('D') + ada_code

                    #refactor to use tooth column with one integer number (tooth_num) instead of calculating
                    #tooth_char = list(tooth_data)

                    #tooth_idx = 0;
                    #for (tooth_yn) in tooth_char:
                        #if tooth_yn.lower() == 'y':
                            #tooth_num = tooth_idx + 1
                    if pds.notnull(surface):
                        surface = surface.strip()

                    try:
                        date_str = p_date.strftime('%Y-%m-%d')

                        visit_id = str(practiceId) + "_" + str(locationId) + "_" + str(pid) + "_" + date_str
                        #uri
                        visit_uri = ohd_ttl['visit uri'].format(visit_id=visit_id)

                        # try/catch here for filter in filling procedures
                        try:
                            # filters on material for certain types of procedures that we are interested in
                            if str(procedure_type) == '1':  ## for filling
                                load_ada_filling_material_map[ada_code]
                            elif str(procedure_type) == '2':  ## for endodontic
                                load_ada_endodontic_material_map[ada_code]
                            else: #invalid procedure_type: stop processing here
                                print("Invalid procedure type: " + str(procedure_type) + " for patient: " + str(pid) + " for practice: " + str(practiceId))
                                output_err("Invalid procedure type: " + str(procedure_type) + " for patient: " + str(pid) + " for practice: " + str(practiceId))
                                logging.exception("message")
                                return

                            if pds.notnull(tooth_num):
                                tooth_id = str(practiceId) + "_" + str(locationId) + "_" + str(pid) + "_" + str(tooth_num)

                                cdt_code_id = tooth_id + "_" + str(ada_code) + "_" + date_str
                                patient_id = str(practiceId) + "_" + str(locationId) + "_" + str(pid)
                                patient_uri = ohd_ttl['patient uri by prefix'].format(patient_id=patient_id)
                                provider_id = str(practiceId) + "_" + str(locationId) + "_" + str(prov_id)

                                tooth_label = "tooth " + str(tooth_num) + " of patient " + str(pid) # "tooth 13 of patient 1"
                                tooth_str = ohd_ttl['declare tooth by prefix'].format(tooth_id=tooth_id,
                                                                                      specific_tooth=label2uri['tooth ' + str(tooth_num)],
                                                                                      restored_tooth=label2uri['restored tooth'],
                                                                                      label=tooth_label)

                                # restoration procedure
                                restoration_procedure_label = "restoration procedure on " + tooth_label + " on " + date_str  # "restoration procedure on tooth 13 of patient 1 on 2003-05-16"
                                specific_procedure = label2uri[load_ada_procedure_map[ada_code]].rsplit('/', 1)[-1]
                                restoration_procedure = ohd_ttl['declare restoration procedure'].format(cdt_code_id=cdt_code_id,
                                                                                                        tooth_restoration_procedure=specific_procedure,
                                                                                                        label=restoration_procedure_label)

                                # restoration material
                                restoration_material_label = "restoration material placed in " + tooth_label  # "restoration material placed in tooth 13 of patient 1"
                                # material fork here: different procedure calls different map for specific material
                                if str(procedure_type) == '1':  ## for filling (filling has surface info)
                                    specific_material = label2uri[load_ada_filling_material_map[ada_code]].rsplit('/', 1)[-1]
                                elif str(procedure_type) == '2':  ## for endodontic
                                    specific_material = label2uri[load_ada_endodontic_material_map[ada_code]].rsplit('/', 1)[-1]
                                restoration_material = ohd_ttl['declare restoration material'].format(cdt_code_id=cdt_code_id,
                                                                                                    tooth_restoration_material=specific_material,
                                                                                                    label=restoration_material_label)

                                # billing code
                                billing_code_label = "billing code " + str(
                                    ada_code) + " for procedure on " + date_str  # "billing code D2160 for procedure on 2003-05-16"
                                billing_code = ohd_ttl['declare billing code'].format(cdt_code_id=cdt_code_id,
                                                                                      billing_code_for_restorative=
                                                                                      label2uri[ada_code.lower()].rsplit('/',1)[-1],
                                                                                      label=billing_code_label)

                                # relation: tooth part of patient  'uri1 is part of uri2':
                                tooth_uri = "tooth:" + str(tooth_id)
                                tooth_patient_relation_str = ohd_ttl['uri1 is part of uri2'].format(uri1=tooth_uri,
                                                                                                    uri2=patient_uri)

                                restoration_procedure_uri = "restoration_procedure:" + str(cdt_code_id)

                                # relation: procedure part of visit
                                procedure_visit_relation_str = ohd_ttl['uri1 is part of uri2'].format(uri1=restoration_procedure_uri,
                                                                                                      uri2=visit_uri)

                                material_uri = "restoration_material:" + str(cdt_code_id)

                                # relation: restoration procedure has specified input provider
                                provider_uri = ohd_ttl['provider uri by prefix'].format(provider_id=str(practiceId) + "_" + str(locationId) + "_" + str(prov_id))
                                procedure_provider_relation_str = ohd_ttl['uri1 has specified input uri2'].format(uri1=restoration_procedure_uri,
                                                                                                                  uri2=provider_uri)

                                # relation: restoration procedure has specified input tooth
                                procedure_tooth_input_relation_str = ohd_ttl['uri1 has specified input uri2'].format(uri1=restoration_procedure_uri,
                                                                                                                     uri2=tooth_uri)

                                # relation: procedure has specified input material
                                procedure_input_material_relation_str = ohd_ttl['uri1 has specified input uri2'].format(uri1=restoration_procedure_uri,
                                                                                                                        uri2=material_uri)

                                # relation: restoration procedure has specified output tooth
                                procedure_tooth_output_relation_str = ohd_ttl['uri1 has specified output uri2'].format(uri1=restoration_procedure_uri,
                                                                                                                       uri2=tooth_uri)

                                # relation: cdt code is about restoration procedure
                                cdt_code_uri = "cdt_code:" + str(cdt_code_id)
                                cdt_code_procedure_relation_str = ohd_ttl['uri1 is about uri2'].format(uri1=cdt_code_uri,
                                                                                                       uri2=restoration_procedure_uri)

                                #TODO: add other procedure_types for surfaces
                                if str(procedure_type) == '1':  ## for filling (filling has surface info)
                                    if pds.notnull(surface) and surface:
                                        output(tooth_str)
                                        output("\n")

                                        surface_char = list(surface)

                                        output(restoration_procedure)
                                        output("\n")

                                        output(restoration_material)
                                        output("\n")

                                        output(billing_code)
                                        output("\n")

                                        output(tooth_patient_relation_str)
                                        output("\n")

                                        output(procedure_visit_relation_str)
                                        output("\n")

                                        # procedure "occurence date" property
                                        output(
                                            ohd_ttl['declare date property uri'].
                                                format(uri=restoration_procedure_uri,
                                                       type=label2uri['occurrence date'].rsplit('/', 1)[-1],
                                                       date=date_str))

                                        for (single_surface) in surface_char:
                                            try:
                                                surface_id = tooth_id + "_" + single_surface

                                                restored_surface_label = "restored surface " + single_surface.upper() + " for " + tooth_label  # "restored surface M for tooth 13 of patient 1"
                                                restrored_surface_str = ohd_ttl['declare restored tooth surface by prefix'].\
                                                    format(surface_id=surface_id,
                                                           specific_restored_tooth_surface=label2uri[restored_tooth_surface_label_map[single_surface.lower()]],
                                                           label=restored_surface_label)
                                                output(restrored_surface_str)

                                                #relation: restored surface part of tooth
                                                restored_surface_uri = "restored_tooth_surface:" + str(surface_id)
                                                restored_surface_tooth_relation_str = ohd_ttl['uri1 is part of uri2'].format(uri1=restored_surface_uri, uri2=tooth_uri)
                                                output(restored_surface_tooth_relation_str)
                                                output("\n")

                                                #relation: material part of restored surface
                                                material_restored_surface_relation_str = ohd_ttl['uri1 is part of uri2'].format(uri1=material_uri, uri2=restored_surface_uri)
                                                output(material_restored_surface_relation_str)
                                                output("\n")

                                                #relation: restoration procedure has specified output restored surface
                                                procedure_restored_surface_relation_str = ohd_ttl['uri1 has specified output uri2'].\
                                                    format(uri1=restoration_procedure_uri, uri2=restored_surface_uri)
                                                output(procedure_restored_surface_relation_str)
                                                output("\n")

                                            except Exception as ex1:
                                                output_err("Problem surface: " + surface_id)
                                                print("Problem surface: " + surface_id)
                                                logging.exception("message")

                                        output(procedure_provider_relation_str)
                                        output("\n")

                                        output(procedure_tooth_input_relation_str)
                                        output("\n")

                                        output(procedure_input_material_relation_str)
                                        output("\n")

                                        output(procedure_tooth_output_relation_str)
                                        output("\n")

                                        output(cdt_code_procedure_relation_str)
                                        output("\n")
                                elif str(procedure_type) == '2':  ## for endodontic
                                    output(tooth_str)
                                    output("\n")

                                    output(restoration_procedure)
                                    output("\n")

                                    output(restoration_material)
                                    output("\n")

                                    output(billing_code)
                                    output("\n")

                                    output(tooth_patient_relation_str)
                                    output("\n")

                                    # relation: material part of tooth
                                    material_tooth_relation_str = ohd_ttl['uri1 is part of uri2'].format(
                                        uri1=material_uri, uri2=tooth_uri)
                                    output(material_tooth_relation_str)
                                    output("\n")

                                    output(procedure_visit_relation_str)
                                    output("\n")

                                    # procedure "occurence date" property
                                    output(
                                        ohd_ttl['declare date property uri'].
                                            format(uri=restoration_procedure_uri,
                                                   type=label2uri['occurrence date'].rsplit('/', 1)[-1],
                                                   date=date_str))

                                    output(procedure_provider_relation_str)
                                    output("\n")

                                    output(procedure_tooth_input_relation_str)
                                    output("\n")

                                    output(procedure_input_material_relation_str)
                                    output("\n")

                                    output(procedure_tooth_output_relation_str)
                                    output("\n")

                                    output(cdt_code_procedure_relation_str)
                                    output("\n")

                        except Exception as ex1:
                            print("Info -- pid: " + str(pid) + " procedure not a valid type of procedure: " + str(ada_code))
                            output_err("Info -- pid: " + str(pid) + " procedure not a valid type of procedure: " + str(ada_code))
                            logging.exception("message")
                    except Exception as ex:
                        print("Problem procedure date for patient: " + str(pid) + " for practice: " + str(practiceId))
                        output_err("Problem procedure date for patient: " + str(pid) + " for practice: " + str(practiceId))
                        logging.exception("message")

print_procedure_ttl(practice_id='1', procedure_type=2)