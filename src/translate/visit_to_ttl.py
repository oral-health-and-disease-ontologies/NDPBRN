import pandas as pds
import logging
import os
from datetime import datetime
from load_resources import curr_dir, ohd_ttl, label2uri

def translate_visit_to_ttl(practice_id='1', output_f='visit.ttl', input_f= 'Patient_History.txt', print_ttl=True, save_ttl=True, vendor='ES'):
    # get data from RI-demo-data
    #df_path = os.path.join(curr_dir, '..', 'data', 'Practice1_Patient_History.xlsx')
    #df_path = os.path.join(curr_dir, '..', 'data', 'Practice' + str(practice_id) + '_Patient_History.xlsx')
    #df_path = os.path.join(curr_dir, '..', 'data', 'Practice' + str(practice_id) + '_Patient_History.txt')
    df_path = input_f
    #df = pds.ExcelFile(df_path).parse()
    #patient_id	birth_date	sex	table_name	date_completed	date_entered	tran_date	description	tooth	surface	action_code	action_code_description	service_code	ada_code	ada_code_description	tooth_data	surface_detail	provider_id	db_practice_id
    if vendor == 'ES':
        df = pds.read_csv(df_path, sep='\t', names=["patient_id", "birth_date", "sex", "table_name", "date_completed", "date_entered", "tran_date", "description", "tooth", "surface", "action_code", "action_code_description", "service_code", "ada_code", "ada_code_description", "tooth_data", "surface_detail", "provider_id", "db_practice_id"],
                      header=0)
    else:
        df = pds.read_csv(df_path, sep='\t',
                      names=["PBRN_PRACTICE", "LOG_ID", "PATIENT_ID", "BIRTH_DATE", "SEX", "TABLE_NAME", "DATE_COMPLETED",
                             "DATE_ENTERED", "TRAN_DATE", "DESCRIPTION", "TOOTH", "SURFACE", "ACTION_CODE", "ACTION_CODE_DESCRIPTION",
                             "SERVICE_CODE", "ADA_CODE", "ADA_CODE_DESCRIPTION", "PROVIDER_ID", "DB_PRACTICE_ID"],
                              header=0)
    if vendor != 'ES':
        df.columns = df.columns.str.lower()

    #visit_df = df[['PBRN_PRACTICE', 'PATIENT_ID', 'TRAN_DATE', 'PROVIDER_ID', 'TABLE_NAME', 'DB_PRACTICE_ID']]
    visit_df = df[['patient_id', 'tran_date', 'provider_id', 'table_name', 'db_practice_id']]

    with open(output_f, 'w') as f:
        # local function for printing and saving turtle output
        def output(value_str, print_ttl=print_ttl, save_ttl=save_ttl):
            if print_ttl == True: print value_str
            if save_ttl == True: f.write(value_str)

        # output prefixes for ttl file
        prefix_str = ohd_ttl['prefix'].format(practice_id=practice_id)
        output(prefix_str)

        # define uri
        practice_uri = ohd_ttl['practice uri'].format(practice_id=practice_id)
        # define types
        practice_type = label2uri['dental health care organization']
        practice_label = 'practice_' + str(practice_id)
        #practiceidstring = 'NDPBRN ' + vendor + ' practice ' + str(practice_id)
        practiceidstring = 'NDPBRN practice ' + str(practice_id)
        # delcare individuals
        output(ohd_ttl['declare practice'].format(uri=practice_uri, type=practice_type, label=practice_label,
                                                  practice_id_str=practiceidstring))

        # print ttl for each patient
        for (idx, pid, visitDate, providerId, tableName, locationId) in visit_df.itertuples():
            practiceId = practice_id
            if tableName.lower() == 'transactions':
                try:
                    date_str = str(datetime.strptime(visitDate, '%Y-%m-%d').date())

                    locationId = int(locationId)
                    visit_id = str(practiceId) + "_" + str(locationId) + "_" + str(pid) + "_" + date_str
                    #uri
                    visit_uri = ohd_ttl['visit uri'].format(visit_id=visit_id)

                    #declare visit
                    output(ohd_ttl['declare obo type with label'].format(uri=visit_uri, type=label2uri['dental visit'].rsplit('/', 1)[-1],
                                                                         label="dental visit " + str(visit_id),
                                                                         practice_id_str=practiceidstring))

                    # relate individuals
                    output(ohd_ttl['uri1 realizes uri2'].format(uri1=visit_uri, uri2= str('obo:') + label2uri['dental health care provider role'].rsplit('/', 1)[-1]))
                    output('\n')
                    output(ohd_ttl['uri1 realizes uri2'].format(uri1=visit_uri, uri2=str('obo:') + label2uri['dental patient role'].rsplit('/', 1)[-1]))
                    output(ohd_ttl['declare date property uri'].format(uri=visit_uri, type=label2uri['occurrence date'].rsplit('/', 1)[-1], date=date_str))

                    # patient role: visit realize patient role
                    patientId = str(practiceId) + "_" + str(locationId) + "_" + str(pid)
                    patient_role_uri = ohd_ttl['patient role uri by prefix'].format(patient_id=patientId)
                    patient_patient_role_relation_str = ohd_ttl['uri1 realizes uri2'].format(uri1=visit_uri, uri2=patient_role_uri)
                    output(patient_patient_role_relation_str)
                    output("\n")

                    # provider role: visit realize probider role
                    provider_id = str(practiceId) + "_" + str(locationId) + "_" + str(providerId)
                    provider_role_uri = ohd_ttl['provider role uri by prefix'].format(provider_id=provider_id)
                    patient_provider_role_relation_str = ohd_ttl['uri1 realizes uri2'].format(uri1=visit_uri, uri2=provider_role_uri)
                    output(patient_provider_role_relation_str)
                    output("\n")

                except Exception as ex:
                    print("Problem visit for patient: " + str(pid) + " for practice: " + str(practiceId))
                    logging.exception("message")

#translate_visit_to_ttl(practice_id='3', vendor='ES')
translate_visit_to_ttl(practice_id='1', vendor='ES',
                       input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Patient_History.txt',
                       output_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/visit.ttl')