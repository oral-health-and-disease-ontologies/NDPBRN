import pandas as pds
import logging
import os
from datetime import datetime
from load_resources import curr_dir, ohd_ttl, label2uri

def translate_patient_to_ttl(practice_id='3', filename='patient.ttl', print_ttl=True, save_ttl=True):
    # get data from RI-demo-data
    #df_path = os.path.join(curr_dir, '..', 'data', 'RI-demo-data.xlsx')
    #df_path = os.path.join(curr_dir, '..', 'data', 'Practice1_Patient_Table.xlsx')
    #df_path = os.path.join(curr_dir, '..', 'data', 'Practice' + str(practice_id) + '_Patient_Table.xlsx')
    df_path = os.path.join(curr_dir, '..', 'data', 'Practice' + str(practice_id) + '_Patient_Table.txt')
    #df = pds.ExcelFile(df_path).parse()
    #df = pds.ExcelFile(df_path).parse()
    df = pds.read_csv(df_path, sep='\t', names=["patient_id", "sex", "birth_date", "status", "patient_db_practice_id"], header=0)
    #df = pds.read_csv(df_path)

    # extract just the patient and gender columns for convience
    #patient_df = df[['patient_id', 'gender', 'birth_date']]
    #patient_df = df[['PATIENT_ID', 'SEX', 'BIRTH_DATE', 'STATUS', 'PBRN_PRACTICE', 'DB_PRACTICE_ID']]
    patient_df = df[['patient_id', 'sex', 'birth_date', 'status', 'patient_db_practice_id']]

    # testing...
    # print patient_df

    with open(filename, 'w') as f:
        # local function for printing and saving turtle output
        def output(value_str, print_ttl=print_ttl, save_ttl=save_ttl):
            if print_ttl == True: print value_str
            if save_ttl == True: f.write(value_str)

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
        for (idx, pid, gender, birth_date, pstatus, locationId) in patient_df.itertuples():
            practiceId = practice_id
#            if pstatus.lower() == 'y':
            try:
                #birth_date_str = birth_date.strftime('%Y-%m-%d')
                birth_date_str = str(datetime.strptime(birth_date, '%Y-%m-%d').date())
                id = str(practiceId) + "_" + str(locationId) + "_" + str(pid)
                patient_role_type = label2uri['dental patient role']

                if gender == 'M':
                    patient_type = label2uri['male dental patient']
                    gender_role_type = label2uri['male gender role']
                else:
                    patient_type = label2uri['female dental patient']
                    gender_role_type = label2uri['female gender role']

                birth_date_type = label2uri['birth_date'].rsplit('/', 1)[-1]

                patient_activity_status_type = label2uri['has patient activity status'].rsplit('/', 1)[-1]

                patient_first_visit_date_type = label2uri['first dental visit date'].rsplit('/', 1)[-1]

                patient_last_visit_date_type = label2uri['last dental visit date'].rsplit('/', 1)[-1]

                # define uri
                patient_uri = ohd_ttl['patient uri by prefix'].format(patient_id=id)
                role_uri = ohd_ttl['patient role uri by prefix'].format(patient_id=id)
                gender_uri = ohd_ttl['gender role uri by prefix'].format(patient_id=id, gender_code=gender)
                # try:
                #    birth_date_str = birth_date.strftime('%Y-%m-%d')
                # except Exception:
                #    birth_date_str = ''
                #    print("patient " + str(pid) + " has not birth date!!!")
                # if pds.isnull(birth_date):
                #    birth_date_str = ''
                # else:
                #    birth_date_str = birth_date.strftime('%Y-%m-%d')

                # define labels
                patient_label = "patient " + id
                role_label = "patient " + id + " patient role"
                gender_label = "patient " + id + " gender role " + gender

                # delcare individuals
                output(ohd_ttl['declare individual uri'].format(uri=patient_uri, type=patient_type,
                                                                label=patient_label))
                output(ohd_ttl['declare individual uri'].format(uri=role_uri, type=patient_role_type,
                                                                label=role_label))
                output(ohd_ttl['declare individual uri'].format(uri=gender_uri, type=gender_role_type,
                                                                label=gender_label))

                output(ohd_ttl['declare date property uri'].format(uri=patient_uri, type=birth_date_type,
                                                                   date=birth_date_str))

                if pstatus == 'A':
                    pstatus_str = 'active'
                else:
                    pstatus_str = 'inactive'

                output(ohd_ttl['declare string property uri'].format(uri=patient_uri, type=patient_activity_status_type,
                                                                   string_value=pstatus_str
                                                                     ))

                # relate individuals
                output(ohd_ttl['uri1 is bearer of uri2'].format(uri1=patient_uri, uri2=gender_uri))
                output(ohd_ttl['uri1 has role uri2'].format(uri1=patient_uri, uri2=role_uri))
                output(ohd_ttl['ur1 member of uri2'].format(uri1=patient_uri, uri2=practice_uri))
            except Exception as ex:
                print("patient " + str(pid) + " has problems!!!")
                logging.exception("message")

translate_patient_to_ttl(practice_id='2')