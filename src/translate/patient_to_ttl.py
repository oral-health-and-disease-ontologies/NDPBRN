import pandas as pds
import logging
import os
from load_resources import curr_dir, ohd_ttl, label2uri

def translate_patient_to_ttl(practice_id='3', filename='patient.ttl', print_ttl=True, save_ttl=True):
    # get data from RI-demo-data
    df_path = os.path.join(curr_dir, '..', 'data', 'RI-demo-data.xlsx')
    df = pds.ExcelFile(df_path).parse()

    # extract just the patient and gender columns for convience
    patient_df = df[['patient_id', 'gender']]

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

        # print ttl for each patient
        for (idx, pid, gender) in patient_df.itertuples():
            id = str(practice_id) + "_" + str(pid)
            patient_role_type = label2uri['dental patient role']
            is_bearer_of = label2uri['is bearer of']
            has_role = label2uri['has role']

            if gender == 'M':
                patient_type = label2uri['male dental patient']
                gender_role_type = label2uri['male gender role']
            else:
                patient_type = label2uri['female dental patient']
                gender_role_type = label2uri['female gender role']

            # declare patient
            label = "patient " + id
            ttl_str = ohd_ttl['declare patient']. \
                format(patient_id=id,
                       dental_patient=patient_type,
                       label=label)
            output(ttl_str)

            # declare patient role
            label = "patient " + id + " patient role"
            ttl_str = ohd_ttl['declare patient role']. \
                format(patient_id=id,
                       patient_role=patient_role_type,
                       label=label)
            output(ttl_str)

            # declare patient gender role
            label = "patient " + id + " gender role " + gender
            ttl_str = ohd_ttl['declare gender role']. \
                format(patient_id=id,
                       gender_role=gender_role_type,
                       gender_code=gender,
                       label=label)
            output(ttl_str)

            # relate patient to patient role
            ttl_str = ohd_ttl['relate patient to role']. \
                format(patient_id=id,
                       has_role=has_role)
            output(ttl_str)

            # relate patient to gender role
            ttl_str = ohd_ttl['relate patient to gender']. \
                format(patient_id=id,
                       gender_code=gender,
                       is_bearer_of=is_bearer_of)
            output(ttl_str)


def translate_patient_to_ttl_1(practice_id='3', filename='patient.ttl', print_ttl=True, save_ttl=True):
    # get data from RI-demo-data
    #df_path = os.path.join(curr_dir, '..', 'data', 'RI-demo-data.xlsx')
    df_path = os.path.join(curr_dir, '..', 'data', 'Practice1_Patient_Table.xlsx')
    df = pds.ExcelFile(df_path).parse()
    #df = pds.read_csv(df_path)

    # extract just the patient and gender columns for convience
    #patient_df = df[['patient_id', 'gender', 'birth_date']]
    patient_df = df[['PATIENT_ID', 'SEX', 'BIRTH_DATE', 'PATIENT_STATUS', 'PBRN_PRACTICE', 'DB_PRACTICE_ID']]

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
        for (idx, pid, gender, birth_date, pstatus, practiceId, locationId) in patient_df.itertuples():
            if pstatus.lower() == 'y':
                try:
                    birth_date_str = birth_date.strftime('%Y-%m-%d')
                    id = str(practiceId) + "_" + str(locationId) + "_" + str(pid)
                    patient_role_type = label2uri['dental patient role']

                    if gender == 'M':
                        patient_type = label2uri['male dental patient']
                        gender_role_type = label2uri['male gender role']
                    else:
                        patient_type = label2uri['female dental patient']
                        gender_role_type = label2uri['female gender role']

                    birth_date_type = label2uri['birth_date'].rsplit('/', 1)[-1]

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

                    # relate individuals
                    output(ohd_ttl['uri1 is bearer of uri2'].format(uri1=patient_uri, uri2=gender_uri))
                    output(ohd_ttl['uri1 has role uri2'].format(uri1=patient_uri, uri2=role_uri))
                    output(ohd_ttl['ur1 member of uri2'].format(uri1=patient_uri, uri2=practice_uri))
                except Exception as ex:
                    print("patient " + str(pid) + " has problems!!!")
                    logging.exception("message")

# translate_patient_to_ttl()
translate_patient_to_ttl_1(practice_id='1')