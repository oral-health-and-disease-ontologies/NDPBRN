import pandas as pds
import logging
import collections
from load_resources import curr_dir, ohd_ttl, label2uri
from src.util.ohd_label2uri import get_date_str, get_visit_id_suffix_with_date_str
import csv

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
                      header=0, quoting=csv.QUOTE_NONE)
    else:
        df = pds.read_csv(df_path, sep='\t',
                          names=["NDPBRN_ID", "procid", "PATIENT_ID", "BIRTH_DATE", "SEX", "TABLE_NAME",
                                 "DATE_COMPLETED",
                                 "DATE_ENTERED", "TRAN_DATE", "TOOTH", "SURFACE", "ACTION_CODE",
                                 "ACTION_CODE_DESCRIPTION",
                                 "SERVICE_CODE", "ADA_CODE", "ADA_CODE_DESCRIPTION", "TOOTH_DATA", "SURFACESTRINGHEX",
                                 "PROVIDER_ID", "DB_PRACTICE_ID", "toothrangestartorig", "toothrangeendorig",
                                 "treatmentarea",
                                 "addtlcodesflag"],
                          header=0, quoting=csv.QUOTE_NONE)

    #patient_df = df[['PBRN_PRACTICE', 'DB_PRACTICE_ID', 'PATIENT_ID', 'TOOTH', 'SURFACE', 'TRAN_DATE', 'ADA_CODE', 'PROVIDER_ID', 'TABLE_NAME']]
    if vendor != 'ES':
        df.columns = df.columns.str.lower()
    #dentrix headers changed again: use "ada_code_description" instead of "description" for dentrix:
    if vendor == 'ES':
        patient_df = df[['db_practice_id', 'patient_id', 'tooth', 'surface', 'date_entered', 'ada_code', 'provider_id', 'table_name', 'tooth_data', 'description']]
    else:
        patient_df = df[['db_practice_id', 'patient_id', 'tooth', 'surface', 'date_entered', 'ada_code', 'provider_id', 'table_name', 'tooth_data', 'ada_code_description']]
        patient_df.columns = ['db_practice_id', 'patient_id', 'tooth', 'surface', 'date_entered', 'ada_code', 'provider_id', 'table_name', 'tooth_data', 'description']

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
                             'Root Caries',
                             'Decay',
                             'Root Decay ',
                             'Recurrent Decay',
                             'Interproximal Decay',
                             'Decay to the nerve',
                             'Severe/Gross Caries/Decay',
                             'Rampant Decay',
                             'Decay arrested',
                             'Decay Incipient',
                             '.DECAY',
                             '.DECAY INCIPIENT',
                             'Decay Recurrent',
                             'Decay Primary',
                             '.DECAY ARRESTED']
# remove decalcification per issue #45: https://github.iu.edu/IUSDRegenstrief/EDR-Study/issues/45
#                             'Decalcification',
#                             'DECALCIFICATION/HYPOCALCIFICATION',
#                             '.Decalcification',
#                             'zDecalcification',
#                             'Dicalsification']

    load_desc_missing_tooth_list = ['Missing Tooth',
                                    'Missing/Extracted tooth',
                                    'zzMissing/Extracted tooth',
                                    'zzzMissing tooth',
                                    'Missing tooth, more than a year',
                                    'zzMissing Tooth',
                                    'Congenitally Missing Tooth',
                                    'Congenitally missing',
                                    'Missing more than one year',
                                    'missing teeth',
                                    'Missing Perm. Tooth, PRIMARY Present',
                                    '.Missing Tooth',
                                    'zCongenitally Missing Tooth',
                                    'missing',
                                    'Missing clinical Crown',
                                    'Missing filling',
                                    'Missing Restoration',
                                    'Filling Missing']

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
                locationId = str(locationId).rsplit('.')[0]
                pid = str(pid).rsplit('.')[0]
                prov_id = str(prov_id).rsplit('.')[0]
                if tableName.lower() == 'patient_conditions':
                    if pds.notnull(surface):
                        surface = surface.strip()

                    try:
                        date_str = get_date_str(p_date)
                        if date_str == 'invalid date':
                            if print_ttl == True:
                                print("Problem procedure date for patient: " + str(pid) + " for practice: " + str(practiceId) + " idex: " + str(idx))
                            output_err("Problem procedure date for patient: " + str(pid) + " for practice: " + str(practiceId) + " idex: " + str(idx))

                        locationId = int(locationId)
                        visit_id = str(practiceId) + "_" + str(locationId) + "_" + str(pid) + "_" + get_visit_id_suffix_with_date_str(date_str, idx)
                        #uri
                        visit_uri = ohd_ttl['visit uri'].format(visit_id=visit_id)

                        # try/catch here for filter in filling procedures
                        try:
                            # filters on material for certain types of procedures that we are interested in
                            continue_flag_filter_with_procedure = False
                            if str(condition_type) == '1':  ## for caries
                                #take care of ignoring case
                                #if description in load_desc_caries_list:
                                if any(s.lower() == description.lower() for s in load_desc_caries_list):
                                    continue_flag_filter_with_procedure = True
                            elif str(condition_type) == '2':  ## for missing_tooth
                                #take care of ignoring case
                                #if description in load_desc_missing_tooth_list:
                                if any(s.lower() == description.lower() for s in load_desc_missing_tooth_list):
                                    continue_flag_filter_with_procedure = True
                            else: #invalid condition_type: stop processing here
                                if print_ttl == True:
                                    print("Invalid condition type: " + str(condition_type) + " for patient: " + str(pid) + " for practice: " + str(practiceId))
                                output_err("Invalid condition type: " + str(condition_type) + " for patient: " + str(pid) + " for practice: " + str(practiceId))
                                logging.exception("message")
                                return

                            if continue_flag_filter_with_procedure:
                                ## with right condition type

                                tooth_num_array = []
                                #use tooth_num, NOT tooth_data string
                                # if str(procedure_type) == '11' or str(procedure_type) == '12' or str(procedure_type) == '13' \
                                #         or str(procedure_type) == '15':
                                #     tooth_num_array = get_tooth_array_idx(tooth_data)
                                # else:
                                #     tooth_num_array.append(tooth_num_in_file)
                                tooth_num_array.append(tooth_num_in_file)

                                for tooth_num in tooth_num_array:
                                    origin_tooth = tooth_num
                                    ####if pds.notnull(tooth_num):
                                    ####    tooth_num = int(tooth_num)
                                    ## after get_tooth_num call, tooth_num is a string either a valid tooth number or "invalid_tooth_num_{idx}"
                                    tooth_num = get_tooth_num(tooth_num, idx)

                                    if tooth_num.startswith('invalid'):
                                        if print_ttl == True:
                                            print("Invalid tooth_num for patient: " + str(pid) + " with ada_code: " + str(ada_code) + " tooth: " + str(origin_tooth) + " tooth_num: " + str(tooth_num) + " idx: " + str(idx))
                                        output_err("Invalid tooth_num for patient: " + str(pid) + " with ada_code: " + str(ada_code) + " tooth: " + str(origin_tooth) + " tooth_num: " + str(tooth_num) + " idx: " + str(idx))

                                    tooth_id = str(practiceId) + "_" + str(locationId) + "_" + str(pid) + "_" + str(tooth_num)
                                    dentition_id = str(practiceId) + "_" + str(locationId) + "_" + str(pid)

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
                                        dentition_uri = "dentition:" + dentition_id
                                        specific_dentition_type = label2uri['secondary dentition missing tooth ' + str(tooth_num)].rsplit('/', 1)[-1]
                                        dentition_str = ohd_ttl['declare obo type'].format(uri=dentition_uri ,
                                                                                            type=specific_dentition_type,
                                                                                            practice_id_str=practiceidstring)
                                    else:
                                        tooth_label = "tooth " + str(tooth_num) + " of patient " + str(pid) # "tooth 13 of patient 1"
                                        tooth_str = ohd_ttl['declare tooth by prefix'].format(tooth_id=tooth_id,
                                                                                          specific_tooth=get_specific_tooth('tooth ', tooth_num, idx),
                                                                                          label=tooth_label,
                                                                                          practice_id_str=practiceidstring)

                                    # relation: tooth part of patient  'uri1 is part of uri2':
                                    tooth_uri = "tooth:" + str(tooth_id)
                                    tooth_patient_relation_str = ohd_ttl['uri1 is part of uri2'].format(uri1=tooth_uri,
                                                                                                        uri2=patient_uri)

                                    ## chnage evaluation uri per Bill: NOT include tooth num
                                    evaluation_uri = "evaluation:" + str(practiceId) + "_" + str(locationId) + "_" + str(pid) + "_" + date_str
                                    evaluation_label = "oral evaluation on patient " + str(pid) + " on " + date_str # 'oral evaluation on patient 68 on 2015-01-12'
                                    # else:
                                    #     evaluation_uri = "evaluation:" + str(cdt_code_id)
                                    #     evaluation_label = "oral evaluation on " + tooth_label + " on " + date_str  # "oral evaluation on tooth 13 of patient 1 on 2003-05-16"

                                    # evaluation
                                    evaluation = ohd_ttl['declare obo type with label'].format(uri=evaluation_uri,
                                                                                      type=label2uri['oral evaluation'].rsplit('/', 1)[-1],  ## 'tooth root caries finding', #oral evaluation
                                                                                      label=evaluation_label,
                                                                                      practice_id_str=practiceidstring)

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

                                    if str(condition_type) == '1' :  ## for caries: sub-class follows
                                        output(tooth_str)
                                        output("\n")

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

                                        output(evaluation_provider_relation_str)
                                        output("\n")

                                        output(evaluation_patient_relation_str)
                                        output("\n")

                                        output(evaluation_tooth_input_relation_str)
                                        output("\n")


                                        if 'root ' in description.lower(): ## description contains string 'root ' - falls into 'tooth root caries finding'
                                            root_uri = "root:" + tooth_id
                                            root_str = ohd_ttl['declare obo type'].format(
                                                uri=root_uri,
                                                type=label2uri['root of tooth'].rsplit('/', 1)[-1],
                                                practice_id_str=practiceidstring)
                                            output(root_str)

                                            finding_label = "caries finding for " + tooth_label + " on " + date_str
                                            finding_id = str(tooth_id) + "_" + date_str
                                            finding_uri = "caries_finding:" + finding_id
                                            finding_str = ohd_ttl['declare obo type with label']. \
                                                format(uri=finding_uri,
                                                       type=label2uri['tooth root caries finding'].rsplit('/', 1)[-1],  ## 'tooth root caries finding'
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

                                            lesion_label = "carious lesion of tooth for " + tooth_label + " on " + date_str
                                            lesion_id = str(tooth_id) + "_" + date_str
                                            lesion_uri = "carious_lesion_tooth:" + lesion_id
                                            lesion_str = ohd_ttl['declare lesion']. \
                                                format(lesion_uri=lesion_uri,
                                                       label=lesion_label,
                                                       practice_id_str=practiceidstring)
                                            output(lesion_str)

                                            # relation: lesion part of root  'uri1 is part of uri2':
                                            lesion_root_relation_str = ohd_ttl['uri1 is part of uri2'].format(
                                                uri1=lesion_uri,
                                                uri2=root_uri)
                                            output(lesion_root_relation_str)

                                            # relation: root part of tooth  'uri1 is part of uri2':
                                            root_tooth_relation_str = ohd_ttl['uri1 is part of uri2'].format(
                                                uri1=root_uri,
                                                uri2=tooth_uri)
                                            output(root_tooth_relation_str)

                                            # relation: finding is about lesion
                                            finding_lesion_relation_str = ohd_ttl['uri1 is about uri2'].format(
                                                uri1=finding_uri,
                                                uri2=lesion_uri)
                                            output(finding_lesion_relation_str)
                                            output("\n")

                                            # relation evaluation has output of finding
                                            evaluation_finding_output_relation_str = ohd_ttl[
                                                'uri1 has specified output uri2'].format(
                                                uri1=evaluation_uri,
                                                uri2=finding_uri)
                                            output(evaluation_finding_output_relation_str)
                                            output("\n")

                                        elif pds.notnull(surface) and surface: ## caries with surface string - falls into 'coronal caries finding'
                                            surface_char = list(surface)

                                            for (single_surface) in surface_char:
                                                convert_surface = get_surface(single_surface, idx)

                                                if convert_surface.startswith("invalid"):
                                                    if print_ttl == True:
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
                                                finding_id = str(tooth_id) + "_" + str(surface) + "_" + date_str
                                                finding_uri = "caries_finding:" + finding_id
                                                finding_str = ohd_ttl['declare obo type with label']. \
                                                    format(uri=finding_uri,
                                                           type=label2uri['coronal caries finding'].rsplit('/', 1)[-1],  ## 'coronal caries finding'
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
                                                lesion_id = str(tooth_id) +  "_" + str(surface) + "_" + date_str
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
                                        else:  ## description has no string 'root' and it does not have surface string - falls into 'coronal caries finding' without surface
                                            ## no surface, so change lesion relates to tooth instead of surface: lesion 'part of' tooth
                                            finding_label = "caries finding for " + tooth_label + " on " + date_str
                                            finding_id = str(tooth_id) + "_" + date_str
                                            finding_uri = "caries_finding:" + finding_id
                                            finding_str = ohd_ttl['declare obo type with label']. \
                                                format(uri=finding_uri,
                                                       type=label2uri['coronal caries finding'].rsplit('/', 1)[-1], ## 'coronal caries finding'
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

                                            lesion_label = "carious lesion of tooth for " + tooth_label + " on " + date_str
                                            lesion_id = str(tooth_id) + "_" + date_str
                                            lesion_uri = "carious_lesion_tooth:" + lesion_id
                                            lesion_str = ohd_ttl['declare lesion']. \
                                                format(lesion_uri=lesion_uri,
                                                       label=lesion_label,
                                                       practice_id_str=practiceidstring)
                                            output(lesion_str)

                                            # relation: lesion part of tooth
                                            lesion_tooth_relation_str = ohd_ttl['uri1 is part of uri2'].format(
                                                uri1=lesion_uri, uri2=tooth_uri)
                                            output(lesion_tooth_relation_str)
                                            output("\n")

                                            # relation: finding is about lesion
                                            finding_lesion_relation_str = ohd_ttl['uri1 is about uri2'].format(
                                                uri1=finding_uri,
                                                uri2=lesion_uri)
                                            output(finding_lesion_relation_str)
                                            output("\n")

                                            # relation evaluation has output of finding
                                            evaluation_finding_output_relation_str = ohd_ttl[
                                                'uri1 has specified output uri2'].format(
                                                uri1=evaluation_uri,
                                                uri2=finding_uri)
                                            output(evaluation_finding_output_relation_str)
                                            output("\n")

                                    elif str(condition_type) == '2':
                                        ## no surface: for missing tooth
                                        ## confirmed with Bill - no "tooth" instance for missing tooth finding
                                        # output(tooth_str)
                                        # output("\n")

                                        output(evaluation)
                                        output("\n")

                                        output(dentition_str)
                                        output("\n")

                                        #TODO - comment out for now per Bill, we need another way to do this
                                        #tooth is not part of dentition relation
                                        # tooth_not_part_dentition_relation_str = ohd_ttl['uri1 is NOT in relationship with uri2'].format(
                                        #     uri1=tooth_uri,
                                        #     relation=label2uri['is part of'],
                                        #     uri2=dentition_uri)
                                        # output(tooth_not_part_dentition_relation_str)
                                        # output("\n")

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

                                        finding_label = "missing tooth finding for " + tooth_label + " on " + date_str
                                        finding_id = str(tooth_id) + "_" + date_str
                                        finding_uri = "missing_tooth_finding:" + finding_id
                                        specific_missing_tooth_finding = label2uri['missing tooth ' + str(tooth_num) + ' finding']
                                        finding_str = ohd_ttl['declare missing tooth finding']. \
                                            format(missing_tooth_finding_uri=finding_uri,
                                                   specific_missing_tooth_finding=specific_missing_tooth_finding,
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

                                        # relation: finding is about dentition
                                        finding_dentition_relation_str = ohd_ttl['uri1 is about uri2'].format(
                                            uri1=finding_uri,
                                            uri2=dentition_uri)
                                        output(finding_dentition_relation_str)
                                        output("\n")

                                        # relation evaluation has output of finding
                                        evaluation_finding_output_relation_str = ohd_ttl[
                                            'uri1 has specified output uri2'].format(
                                            uri1=evaluation_uri,
                                            uri2=finding_uri)
                                        output(evaluation_finding_output_relation_str)
                                        output("\n")

                                        ##no relation of: evaluation has output of tooth
                                        # output(evaluation_tooth_output_relation_str)
                                        # output("\n")
                        except Exception as ex1:
                            if print_ttl == True:
                                print("Info -- pid: " + str(pid) + " procedure with problem: tooth_num: " + str(tooth_num) + " idx: " + str(idx))
                                logging.exception("message")
                            output_err("Info -- pid: " + str(pid) + " procedure with problem: tooth_num: " + str(tooth_num) + " idx: " + str(idx))
                    except Exception as ex:
                        if print_ttl == True:
                            print("Problem procedure date for patient: " + str(pid) + " for practice: " + str(practiceId) + " idx: " + str(idx))
                            logging.exception("message")
                        output_err("Problem procedure date for patient: " + str(pid) + " for practice: " + str(practiceId) + " idx: " + str(idx))
            output('}')

def get_tooth_num(tooth_num, idx):
    if pds.notnull(tooth_num):
        try:
            label2uri["tooth " + str(tooth_num).rsplit('.')[0]]
        except Exception as ex:
            return "invalid_tooth_num_" + str(idx)
        return str(tooth_num).rsplit('.')[0]
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

# print_condition_ttl(practice_id='1', condition_type=1,
#                    input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/es_sample/A_1_tooth_history_ted.txt',
#                    output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/es_sample/',
#                    vendor='ES')
# print_condition_ttl(practice_id='1', condition_type=1,
#                    input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/ES/PRAC_1/A_1_tooth_history.txt',
#                    output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/translate/translate_data/ES/PRAC_1/',
#                    vendor='ES',
#                    print_ttl=False)
## try dentrix data
# print_condition_ttl(practice_id='1', condition_type=1,
#                   input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/dentrix_sample/tooth history.txt',
#                   output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/dentrix_sample/',
#                   vendor='dentrix')
