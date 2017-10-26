import pandas as pds
import logging
import collections
from load_resources import curr_dir, ohd_ttl, label2uri
from src.util.ohd_label2uri import get_date_str, get_visit_id_suffix_with_date_str

## no need of specific restored surface in conditions (only need specific Surface Enamel of Tooth)
# restored_tooth_surface_label_map = {'b': 'restored buccal surface',
#                                     'd': 'restored distal surface',
#                                     'i': 'restored incisal surface',
#                                     'f': 'restored labial surface',
#                                     'l': 'restored lingual surface',
#                                     'm': 'restored mesial surface',
#                                     'o': 'restored occlusal surface'
#                                     }

tooth_surface_label_map = {'b': 'buccal surface enamel of tooth',
                           'd': 'distal surface enamel of tooth',
                           'i': 'incisal surface enamel of tooth',
                           'f': 'labial surface enamel of tooth',
                           'l': 'lingual surface enamel of tooth',
                           'm': 'mesial surface enamel of tooth',
                           'o': 'occlusal surface enamel of tooth'
                          }

def print_condition_ttl(practice_id='1', input_f='Patient_History.txt',
                        output_p='./',
                        print_ttl=True, save_ttl=True, condition_type=1, vendor='ES'):

#    df_path = os.path.join(curr_dir, '..', 'data', 'Practice1_Fillings.xlsx')
    #df_path = os.path.join(curr_dir, '..', 'data', 'Practice1_Patient_History.xlsx')
    #df_path = os.path.join(curr_dir, '..', 'data', 'Practice' + str(practice_id) + '_Patient_History.xlsx')
    #df_path = os.path.join(curr_dir, '..', 'data', 'Practice' + str(practice_id) + '_Patient_History.txt')
    df_path = input_f
    #df = pds.ExcelFile(df_path).parse()
    #patient_id	birth_date	sex	table_name	date_completed	date_entered	tran_date	description	tooth	surface	action_code	action_code_description	service_code	ada_code	ada_code_description	tooth_data	surface_detail	provider_id	db_practice_id
    if vendor == 'ES':
        df = pds.read_csv(df_path, sep='\t',
                      names=["practice_id", "patient_id", "birth_date", "sex", "table_name", "date_completed", "date_entered", "tran_date", "description", "tooth", "surface", "action_code", "action_code_description",
                             "service_code", "ada_code", "ada_code_description", "tooth_data", "surface_detail", "provider_id", "db_practice_id"],
                      header=0)
    else:
        #df = pds.read_csv(df_path, sep='\t',
        #              names=["PBRN_PRACTICE", "LOG_ID", "PATIENT_ID", "patient_status", "BIRTH_DATE", "SEX", "TABLE_NAME",
        #                     "DATE_COMPLETED", "DATE_ENTERED", "TRAN_DATE", "DESCRIPTION", "TOOTH", "toothrangestart",
        #                     "toothrangeend", "SURFACE", "surfm", "surfo", "surfd", "surfl", "surff", "surf5", "ACTION_CODE",
        #                     "ACTION_CODE_DESCRIPTION", "SERVICE_CODE", "ADA_CODE", "ADA_CODE_DESCRIPTION", "PROVIDER_ID",
        #                     "chartstatus", "DB_PRACTICE_ID"],
        #                      header=0)
         df = pds.read_csv(df_path, sep='\t',
                        names=['NDPBRN_ID', "patient_id", "birth_date", "sex", "table_name", "date_completed", "date_entered", "tran_date", "description", "tooth", "surface", "action_code", "action_code_description",
                             "service_code", "ada_code", "ada_code_description", "tooth_data", "surface_detail", "provider_id", "db_practice_id"],
                           header=0)

#patient_df = df[['PBRN_PRACTICE', 'DB_PRACTICE_ID', 'PATIENT_ID', 'TOOTH', 'SURFACE', 'TRAN_DATE', 'ADA_CODE', 'PROVIDER_ID', 'TABLE_NAME']]
    if vendor != 'ES':
        df.columns = df.columns.str.lower()
    #TODO - check on using of date_entered
    patient_df = df[['db_practice_id', 'patient_id', 'tooth', 'surface', 'date_entered', 'ada_code', 'provider_id', 'table_name', 'tooth_data', 'description']]

    condition_type_map = {'1': 'caries',
                   '2': 'missing_tooth'}

    surface_map = {'m': 'Mesial surface enamel of tooth',
                   'o': 'Occlusal surface enamel of tooth',
                   'b': 'Buccal surface enamel of tooth',
                   'd': 'Distal surface enamel of tooth',
                   'i': 'Incisal surface enamel of tooth',
                   'f': 'Labial surface enamel of tooth',
                   'l': 'Lingual surface enamel of tooth'}

    load_desc_caries_list = ['Incipient Caries',
                    'caries',
                    'Caries/decay',
                    'Deep dentinal/cemental caries',
                    'Recurring caries/surface restor',
                    'Severe/Gross Caries/Decay',
                    'Decay',
                    'Recurrent Decay',
                    'Interproximal Decay',
                    'Decay to the nerve',
                    'Severe/Gross Caries/Decay',
                    'Rampant Decay',
                    'Decay Incipient',
                    '.DECAY',
                    '.DECAY INCIPIENT',
                    'Decay Recurrent',
                    'Decay Primary',
                    'Decalcification',
                    'DECALCIFICATION/HYPOCALCIFICATION',
                    '.Decalcification',
                    'zDecalcification',
                    'Dicalsification']

    #TODO - filling all description for missing tooth later
    load_desc_missing_tooth_list = []

    try:
        filename = output_p + condition_type_map[str(condition_type)] + '.trig'
        err_filename = output_p + condition_type_map[str(condition_type)] + '_err.txt'
    except Exception as ex:  # invalid condition_type: stop processing here
        print("Invalid condition type: " + str(condition_type))
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

            if (vendor == 'ES'):
                practice_id = 'A_' + str(practice_id)
            else:
                practice_id = 'B_' + str(practice_id)

            # output prefixes for ttl file
            prefix_str = ohd_ttl['prefix'].format(practice_id=practice_id)
            output(prefix_str)

            output(':G_' + practice_id + ' {')

            #practiceidstring = 'NDPBRN ' + vendor + ' practice ' + str(practice_id)
            # if (vendor == 'ES'):
            #     vendorChar = 'A '
            # else:
            #     vendorChar = 'B '
            # practiceidstring = 'NDPBRN practice ' + vendorChar + str(practice_id)
            practiceidstring = 'NDPBRN practice ' + str(practice_id)
            # practice
            practice_uri = ohd_ttl['practice uri'].format(practice_id=practice_id)
            # define types
            practice_type = label2uri['dental health care organization']
            practice_label = "practice_" + str(practice_id)
            # delcare individuals
            output(ohd_ttl['declare practice'].format(uri=practice_uri, type=practice_type, label=practice_label,
                                                      practice_id_str=practiceidstring))

            # print ttl for each patient
            #for (idx, practiceId, locationId, pid, tooth_num, surface, p_date, ada_code, prov_id, tableName) in patient_df.itertuples():
            practiceId = practice_id
            for (idx, locationId, pid, tooth_num_in_file, surface, p_date, ada_code, prov_id, tableName, tooth_data, description) in patient_df.itertuples():
                if tableName.lower() == 'patient_conditions':
                    if pds.notnull(surface):
                        surface = surface.strip()

                    try:
                        date_str = get_date_str(p_date)
                        if date_str == 'invalid date':
                            print("Problem procedure date for patient: " + str(pid) + " for practice: " + str(practiceId) + " idex: " + str(idx))
                            output_err("Problem procedure date for patient: " + str(pid) + " for practice: " + str(practiceId) + " idex: " + str(idx))

                        locationId = int(locationId)
                        #TODO - need discuss with Bill about the "visit" which is not a "transactions" (probably change visit translation or define in here for conditions)
                        visit_id = str(practiceId) + "_" + str(locationId) + "_" + str(pid) + "_" + get_visit_id_suffix_with_date_str(date_str, idx)

                        #TODO - wait for double check on visit
                        #uri
                        visit_uri = ohd_ttl['visit uri'].format(visit_id=visit_id)

                        # try/catch here for filter in filling procedures
                        try:
                            # filters on material for certain types of procedures that we are interested in
                            continue_flag_filter_with_procedure = False
                            if str(condition_type) == '1':  ## for caries
                                if description in load_desc_caries_list:
                                    continue_flag_filter_with_procedure = True
                            elif str(condition_type) == '2':  ## for missing_tooth
                                if description in load_desc_missing_tooth_list:
                                    continue_flag_filter_with_procedure = True
                            else: #invalid condition_type: stop processing here
                                print("Invalid condition type: " + str(condition_type) + " for patient: " + str(pid) + " for practice: " + str(practiceId))
                                output_err("Invalid condition type: " + str(condition_type) + " for patient: " + str(pid) + " for practice: " + str(practiceId))
                                logging.exception("message")
                                return

                            if continue_flag_filter_with_procedure:
                                ## with right condition type

                                ##### coped from visit_to_ttl: basically to create visit here... we dont tranlate "patient_conditions" in visit_to_ttl
                                # declare visit
                                output(ohd_ttl['declare obo type with label'].format(uri=visit_uri, type=
                                label2uri['dental visit'].rsplit('/', 1)[-1],
                                                                                     label="dental visit " + str(
                                                                                         visit_id),
                                                                                     practice_id_str=practiceidstring))

                                # relate individuals
                                output(
                                    ohd_ttl['uri1 realizes uri2'].format(uri1=visit_uri, uri2=str('obo:') + label2uri[
                                        'dental health care provider role'].rsplit('/', 1)[-1]))
                                output('\n')
                                output(
                                    ohd_ttl['uri1 realizes uri2'].format(uri1=visit_uri, uri2=str('obo:') + label2uri[
                                        'dental patient role'].rsplit('/', 1)[-1]))
                                if date_str != 'invalid date':
                                    output(ohd_ttl['declare date property uri'].format(uri=visit_uri, type=
                                    label2uri['occurrence date'].rsplit('/', 1)[-1], date=date_str))
                                else:
                                    output('\n')

                                # patient role: visit realize patient role
                                patientId = str(practiceId) + "_" + str(locationId) + "_" + str(pid)
                                patient_role_uri = ohd_ttl['patient role uri by prefix'].format(patient_id=patientId)
                                patient_patient_role_relation_str = ohd_ttl['uri1 realizes uri2'].format(uri1=visit_uri,
                                                                                                         uri2=patient_role_uri)
                                output(patient_patient_role_relation_str)
                                output("\n")

                                # provider role: visit realize probider role
                                provider_id = str(practiceId) + "_" + str(locationId) + "_" + str(prov_id)
                                provider_role_uri = ohd_ttl['provider role uri by prefix'].format(
                                    provider_id=provider_id)
                                patient_provider_role_relation_str = ohd_ttl['uri1 realizes uri2'].format(
                                    uri1=visit_uri,
                                    uri2=provider_role_uri)
                                output(patient_provider_role_relation_str)
                                output("\n")
                                #####END of coped from visit_to_ttl: basically to create visit here... we dont tranlate "patient_conditions" in visit_to_ttl

                                tooth_num_array = []
                                #TODO - check to see if we need tooth_num or tooth_date
                                # if str(procedure_type) == '11' or str(procedure_type) == '12' or str(procedure_type) == '13' \
                                #         or str(procedure_type) == '15':
                                #     tooth_num_array = get_tooth_array_idx(tooth_data)
                                # else:
                                #     tooth_num_array.append(tooth_num_in_file)
                                tooth_num_array.append(tooth_num_in_file)

                                for tooth_num in tooth_num_array:
                                    origin_tooth = tooth_num
                                    if pds.notnull(tooth_num):
                                        tooth_num = int(tooth_num)
                                    ## after get_tooth_num call, tooth_num is a string either a valid tooth number or "invalid_tooth_num_{idx}"
                                    tooth_num = get_tooth_num(tooth_num, idx)

                                    if tooth_num.startswith('invalid'):
                                        print("Invalid tooth_num for patient: " + str(pid) + " with ada_code: " + str(ada_code) + " tooth: " + str(origin_tooth) + " tooth_num: " + str(tooth_num) + " idx: " + str(idx))
                                        output_err("Invalid tooth_num for patient: " + str(pid) + " with ada_code: " + str(ada_code) + " tooth: " + str(origin_tooth) + " tooth_num: " + str(tooth_num) + " idx: " + str(idx))

                                    tooth_id = str(practiceId) + "_" + str(locationId) + "_" + str(pid) + "_" + str(tooth_num)

                                    # TODO - virtual cdt_code_id here, double check with Bill (without ada_code for conditions)
                                    if date_str != 'invalid date':
                                        cdt_code_id = tooth_id + "_" + date_str
                                    else:
                                        cdt_code_id = tooth_id + "_invalid_procedure_date_" + str(idx)
                                    patient_id = str(practiceId) + "_" + str(locationId) + "_" + str(pid)
                                    patient_uri = ohd_ttl['patient uri by prefix'].format(patient_id=patient_id)
                                    provider_id = str(practiceId) + "_" + str(locationId) + "_" + str(prov_id)

                                    if str(condition_type) == '1':
                                        ## for caries
                                        tooth_label = "tooth " + str(tooth_num) + " of patient " + str(pid) # "tooth 13 of patient 1"
                                        tooth_str = ohd_ttl['declare tooth by prefix'].format(tooth_id=tooth_id,
                                                                                          specific_tooth=get_specific_tooth('tooth ', tooth_num, idx),
                                                                                          label=tooth_label,
                                                                                          practice_id_str=practiceidstring)
                                    elif str(condition_type) == '2':
                                        ## for missing tooth
                                        tooth_label = "tooth " + str(tooth_num) + " of patient " + str(pid) # "tooth 13 of patient 1"
                                        tooth_str = ohd_ttl['declare tooth by prefix'].format(tooth_id=tooth_id,
                                                                                          specific_tooth=get_specific_tooth('tooth ', tooth_num, idx),
                                                                                          label=tooth_label,
                                                                                          practice_id_str=practiceidstring)
                                        dentition_uri = "dentition:" + tooth_id
                                        dentition_str = ohd_ttl['declare obo type'].format(uri=dentition_uri ,
                                            type=label2uri['secondary dentition'].rsplit('/', 1)[-1],
                                            practice_id_str=practiceidstring)
                                    else:
                                        tooth_label = "tooth " + str(tooth_num) + " of patient " + str(pid) # "tooth 13 of patient 1"
                                        tooth_str = ohd_ttl['declare tooth by prefix'].format(tooth_id=tooth_id,
                                                                                          specific_tooth=get_specific_tooth('tooth ', tooth_num, idx),
                                                                                          label=tooth_label,
                                                                                          practice_id_str=practiceidstring)

                                    # evaluation
                                    evaluation_label = "oral evaluation on " + tooth_label + " on " + date_str  # "oral evaluation on tooth 13 of patient 1 on 2003-05-16"
                                    #specific_procedure = label2uri[load_ada_procedure_map[ada_code]].rsplit('/', 1)[-1]
                                    evaluation = ohd_ttl['declare evaluation'].format(cdt_code_id=cdt_code_id,
                                                                                      label=evaluation_label,
                                                                                      practice_id_str=practiceidstring)

                                    # relation: tooth part of patient  'uri1 is part of uri2':
                                    tooth_uri = "tooth:" + str(tooth_id)
                                    tooth_patient_relation_str = ohd_ttl['uri1 is part of uri2'].format(uri1=tooth_uri,
                                                                                                        uri2=patient_uri)

                                    evaluation_uri = "evaluation:" + str(cdt_code_id)

                                    # relation: evaluation part of visit
                                    evaluation_visit_relation_str = ohd_ttl['uri1 is part of uri2'].format(uri1=evaluation_uri,
                                                                                                          uri2=visit_uri)

                                    # relation: evaluation has specified input provider
                                    provider_uri = ohd_ttl['provider uri by prefix'].format(provider_id=str(practiceId) + "_" + str(locationId) + "_" + str(prov_id))
                                    evaluation_provider_relation_str = ohd_ttl['uri1 has specified input uri2'].format(uri1=evaluation_uri,
                                                                                                                      uri2=provider_uri)

                                    # relation: evaluation has specified input patient
                                    evaluation_patient_relation_str = ohd_ttl['uri1 has specified input uri2'].format(uri1=evaluation_uri,
                                                                                                                     uri2=patient_uri)

                                    # relation: evaluation has specified input tooth
                                    evaluation_tooth_input_relation_str = ohd_ttl['uri1 has specified input uri2'].format(uri1=evaluation_uri,
                                                                                                                         uri2=tooth_uri)

                                    # relation: evaluation has specified output finding
                                    #TODO - finding output here

                                    if str(condition_type) == '1' :  ## for caries (with surface info)
                                        if pds.notnull(surface) and surface:
                                            output(tooth_str)
                                            output("\n")

                                            surface_char = list(surface)

                                            output(evaluation)
                                            output("\n")

                                            output(tooth_patient_relation_str)
                                            output("\n")

                                            output(evaluation_visit_relation_str)
                                            output("\n")

                                            # evaluation "occurence date" property
                                            if date_str != 'invalid date':
                                                output(
                                                    ohd_ttl['declare date property uri'].
                                                        format(uri=evaluation_uri,
                                                           type=label2uri['occurrence date'].rsplit('/', 1)[-1],
                                                           date=date_str))

                                            for (single_surface) in surface_char:
                                                convert_surface = get_surface(single_surface, idx)

                                                if convert_surface.startswith("invalid"):
                                                    print("Invalid surface for patient: " + str(
                                                        pid) + " tooth: " + str(
                                                        origin_tooth) + " tooth_num: " + str(
                                                        tooth_num) + " surface: " + str(single_surface) + " idx: " + str(
                                                        idx))
                                                    output_err("Invalid surface for patient: " + str(
                                                        pid) + " tooth: " + str(
                                                        origin_tooth) + " tooth_num: " + str(
                                                        tooth_num) + " surface: " + str(single_surface) + " idx: " + str(
                                                        idx))

                                                surface_id = tooth_id + "_" + convert_surface

                                                surface_label = "surface " + single_surface.upper() + " for " + tooth_label  # "surface M for tooth 13 of patient 1"
                                                specific_tooth_surface = get_specific_surface(single_surface, idx)
                                                surface_str = ohd_ttl['declare surface by prefix'].\
                                                    format(surface_id=surface_id,
                                                           specific_tooth_surface=specific_tooth_surface,
                                                           label=surface_label,
                                                           practice_id_str=practiceidstring)
                                                output(surface_str)

                                                finding_label = "caries finding for " + surface_label + " on " + date_str
                                                finding_id = str(surface_id) + "_" + date_str
                                                finding_uri = "caries_finding:" + finding_id
                                                finding_str = ohd_ttl['declare caries finding'].\
                                                    format(caries_finding_uri=finding_uri,
                                                           label=finding_label,
                                                           practice_id_str=practiceidstring)
                                                output(finding_str)

                                                # finding "occurence date" property
                                                if date_str != 'invalid date':
                                                    output(
                                                        ohd_ttl['declare date property uri'].
                                                            format(uri=finding_uri,
                                                                   type=label2uri['occurrence date'].rsplit('/', 1)[-1],
                                                                   date=date_str))

                                                lesion_label = "carious lesion of tooth for " + surface_label + " on " + date_str
                                                lesion_id = str(surface_id) + "_" + date_str
                                                lesion_uri = "carious_lesion_tooth:" + lesion_id
                                                lesion_str = ohd_ttl['declare lesion']. \
                                                    format(lesion_uri=lesion_uri,
                                                           label=lesion_label,
                                                           practice_id_str=practiceidstring)
                                                output(lesion_str)

                                                #relation: surface part of tooth
                                                surface_uri = "surface:" + str(surface_id)
                                                surface_tooth_relation_str = ohd_ttl['uri1 is part of uri2'].format(uri1=surface_uri, uri2=tooth_uri)
                                                output(surface_tooth_relation_str)
                                                output("\n")

                                                # relation: lesion part of surface
                                                lesion_surface_relation_str = ohd_ttl['uri1 is part of uri2'].format(uri1=lesion_uri, uri2=surface_uri)
                                                output(lesion_surface_relation_str)
                                                output("\n")

                                                # relation: finding is about lesion
                                                finding_lesion_relation_str = ohd_ttl['uri1 is about uri2'].format(
                                                    uri1=finding_uri,
                                                    uri2=lesion_uri)
                                                output(finding_lesion_relation_str)
                                                output("\n")

                                                # relation evaluation has output of finding
                                                evaluation_finding_output_relation_str = ohd_ttl['uri1 has specified output uri2'].format(
                                                    uri1=evaluation_uri,
                                                    uri2=finding_uri)
                                                output(evaluation_finding_output_relation_str)
                                                output("\n")

                                            output(evaluation_provider_relation_str)
                                            output("\n")

                                            output(evaluation_patient_relation_str)
                                            output("\n")

                                            output(evaluation_tooth_input_relation_str)
                                            output("\n")

                                        else:
                                            ## null/empty surface when there's supposed to have surface:
                                            print("Null surface for patient: " + str(pid) + " tooth: " + str(origin_tooth) + " tooth_num: " + str(tooth_num) + " surface: "  + str(surface) + " idx: " + str(idx))
                                            output_err("Null surface for patient: " + str(pid) + " tooth: " + str(origin_tooth) + " tooth_num: " + str(tooth_num) + " surface: "  + str(surface) + " idx: " + str(idx))

                                            output(tooth_str)
                                            output("\n")

                                            output(evaluation)
                                            output("\n")

                                            output(tooth_patient_relation_str)
                                            output("\n")

                                            output(evaluation_visit_relation_str)
                                            output("\n")
                                            output(evaluation_provider_relation_str)
                                            output("\n")

                                            output(evaluation_patient_relation_str)
                                            output("\n")

                                            output(evaluation_tooth_input_relation_str)
                                            output("\n")

                                    elif str(condition_type) == '2':
                                        #TODO - test for type 2 for missing tooth!!
                                        ## no surface: for missing tooth
                                        output(tooth_str)
                                        output("\n")

                                        output(evaluation)
                                        output("\n")


                                        output(dentition_str)
                                        output("\n")

                                        #tooth is not part of dentition relation
                                        tooth_not_part_dentition_relation_str = ohd_ttl['uri1 is NOT in relationship with uri2'].format(
                                            uri1=tooth_uri,
                                            relation=label2uri['is part of'],
                                            uri2=dentition_uri)
                                        output(tooth_not_part_dentition_relation_str)
                                        output("\n")

                                        # relation dentition part of patient
                                        dentition_patient_relation_str = ohd_ttl['uri1 is part of uri2'].format(
                                            uri1=dentition_uri, uri2=patient_uri)
                                        output(dentition_patient_relation_str)
                                        output("\n")

                                        #dentition "missing tooth number" property
                                        if not tooth_num.startswith('invalid'):
                                            dentition_miss_tooth_prop = ohd_ttl['declare string property uri'].format(
                                                uri=dentition_uri, type = label2uri['missing tooth number'].rsplit('/', 1)[-1], string_value=str(tooth_num))
                                            output(dentition_miss_tooth_prop)
                                            output("\n")

                                        output(evaluation_visit_relation_str)
                                        output("\n")

                                        # procedure "occurence date" property
                                        if date_str != 'invalid date':
                                            output(
                                                ohd_ttl['declare date property uri'].
                                                    format(uri=evaluation_uri,
                                                       type=label2uri['occurrence date'].rsplit('/', 1)[-1],
                                                       date=date_str))

                                        output(evaluation_provider_relation_str)
                                        output("\n")

                                        output(evaluation_patient_relation_str)
                                        output("\n")

                                        output(evaluation_tooth_input_relation_str)
                                        output("\n")

                                        ##no relation of: evaluation has output of tooth
                                        # output(evaluation_tooth_output_relation_str)
                                        # output("\n")
                        except Exception as ex1:
                            print("Info -- pid: " + str(pid) + " procedure with problem: tooth_num: " + str(tooth_num) + " idx: " + str(idx))
                            output_err("Info -- pid: " + str(pid) + " procedure with problem: tooth_num: " + str(tooth_num) + " idx: " + str(idx))
                            logging.exception("message")
                    except Exception as ex:
                        print("Problem procedure date for patient: " + str(pid) + " for practice: " + str(practiceId) + " idx: " + str(idx))
                        output_err("Problem procedure date for patient: " + str(pid) + " for practice: " + str(practiceId) + " idx: " + str(idx))
                        logging.exception("message")
            output('}')

def get_tooth_num(tooth_num, idx):
    if pds.notnull(tooth_num):
        try:
            label2uri["tooth " + str(tooth_num)]
        except Exception as ex:
            return "invalid_tooth_num_" + str(idx)
        return str(tooth_num)
    else:
        return "invalid_tooth_num_" + str(idx)

## now the tooth_prefix is one of "tooth ", "prosthetic tooth ".
def get_specific_tooth(tooth_prefix, tooth_num, idx):
    try:
        specific_tooth = label2uri[tooth_prefix + str(tooth_num)]
        return specific_tooth
    except Exception as ex:
        if tooth_prefix.startswith('tooth'):
            return label2uri['tooth']
        elif tooth_prefix.startswith('prosthetic'):
            return label2uri['prosthetic tooth']

def get_surface(single_surface, idx):
    try:
        label2uri[tooth_surface_label_map[single_surface.lower()]]
        return single_surface
    except Exception as ex:
        return "invalid_surface_" + str(idx)

def get_specific_surface(single_surface, idx):
    try:
        specific_tooth_surface = label2uri[tooth_surface_label_map[single_surface.lower()]]
        return specific_tooth_surface
    except Exception as ex:
        return label2uri['surface enamel of tooth']

def get_tooth_array_idx(tooth_data):
    tooth_num_array = []
    array_idx = 1
    for tooth_array_char in tooth_data:
        if 'Y' == tooth_array_char and array_idx < 33:
            tooth_num_array.append(array_idx)
        array_idx = array_idx + 1
    #TODO - check on this:
    ## if there is NO tooth data marked with Y for first 32 teeth, append '' into it so we can do invalid info output
    if len(tooth_num_array) < 1:
        tooth_num_array.append('empty_tooth')

    return tooth_num_array

def test_get_tooth_array_idx():
    indx_array = get_tooth_array_idx('NNNNNNNNNNYYYYYNNNNNYYYYYYYYYYYYYYY')
    print indx_array
    indx_array = get_tooth_array_idx('NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN')
    print indx_array
#test_get_tooth_array_idx()

print_condition_ttl(practice_id='1', condition_type=1,
                   input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/es_sample/A_1_tooth_history_ted.txt',
                   output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/es_sample/',
                   vendor='ES')
## try dentrix data
#print_condition_ttl(practice_id='1', condition_type=1,
#                   input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/dentrix_sample/tooth history.txt',
#                   output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/dentrix_sample/',
#                   vendor='dentrix')
