import pandas as pds
import os
from load_resources import curr_dir, ohd_ttl, label2uri

def translate_provider_to_ttl(practice_id='3', filename='provider.ttl', print_ttl=True, save_ttl=True):
    # get data from RI-demo-data
    df_path = os.path.join(curr_dir, '..', 'data', 'RI-demo-data.xlsx')
    df = pds.ExcelFile(df_path).parse()

    # write ttl to file
    with open(filename, 'w') as f:
        # local function for printing and saving turtle output
        def output(value_str, print_ttl=print_ttl, save_ttl=save_ttl):
            if print_ttl == True: print value_str
            if save_ttl == True: f.write(value_str)

        # output prefixes for ttl file
        prefix_str = ohd_ttl['prefix'].format(practice_id=practice_id)
        output(prefix_str)

        for row in df.itertuples():
            # set variables need to format ttl string
            id = str(practice_id) + "_" + str(row.provider_id)
            provider_type = label2uri['dental health care provider']
            provider_role_type = label2uri['dental health care provider role']
            has_role = label2uri['has role']

            # declare provider
            label = "provider " + id
            ttl_str = \
                ohd_ttl['declare provider']. \
                    format(provider_id=id,
                           label=label,
                           dental_health_care_provider=provider_type)
            output(ttl_str)

            # declare provider role
            label = "provider " + id + " provider role"
            ttl_str = \
                ohd_ttl['declare provider role']. \
                    format(provider_id=id,
                           label=label,
                           dental_health_care_provider_role=provider_role_type)
            output(ttl_str)

            # relate provider to role
            ttl_str = \
                ohd_ttl['relate provider to role']. \
                    format(provider_id=id,
                           has_role=has_role)
            output(ttl_str)

def translate_provider_to_ttl_1(practice_id='3', filename='provider.ttl', print_ttl=True, save_ttl=True):
    # get data from RI-demo-data
    #df_path = os.path.join(curr_dir, '..', 'data', 'RI-demo-data.xlsx')
    #df_path = os.path.join(curr_dir, '..', 'data', 'Practice1_Provider_Table.csv')
    #df_path = os.path.join(curr_dir, '..', 'data', 'Practice1_Provider_Table.xlsx')
    df_path = os.path.join(curr_dir, '..', 'data', 'Practice' + str(practice_id) + '_Provider_Table.xlsx')
    df = pds.ExcelFile(df_path).parse()
    #df = pds.read_csv(df_path)

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

        for row in df.itertuples():
#            if row.PROVIDER_ID.lower() != 'bs' and row.PROVIDER_ID.lower() != 'ss':
            # set variables need to format ttl string
            id = str(row.PBRN_PRACTICE) + "_" + str(row.DB_PRACTICE_ID) + "_" + str(row.PROVIDER_ID)
            provider_type = label2uri['dental health care provider']
            provider_role_type = label2uri['dental health care provider role']
            office_staff_role_type = label2uri['health care office staff role']
            has_role = label2uri['has role']

            # define uri
            provider_uri = ohd_ttl['provider uri by prefix'].format(provider_id=id)
            role_uri = ohd_ttl['provider role uri by prefix'].format(provider_id=id)
            office_staff_role_uri = ohd_ttl['office staff role uri by prefix'].format(provider_id=id)

            # define labels
            provider_label = "provider " + id
            role_label = "provider " + id + " provider role"
            office_staff_role_label = "office staff " + id + " office staff role"

            # delcare individuals
            output(ohd_ttl['declare individual uri'].
                   format(uri=provider_uri, type=provider_type, label=provider_label))

            output(ohd_ttl['declare individual uri'].
                format(uri=role_uri, type=provider_role_type, label=role_label))

            # if string "office" is in position string, print office staff role and relate it to the provider:
            if "office" in row.POSITION.lower():
                output(ohd_ttl['declare individual uri'].
                    format(uri=office_staff_role_uri, type=office_staff_role_type, label=office_staff_role_label))
                output(ohd_ttl['uri1 has role uri2'].
                    format(uri1=provider_uri, uri2=office_staff_role_uri))

            # relate individuals
            output(ohd_ttl['uri1 has role uri2'].
                format(uri1=provider_uri, uri2=role_uri))

            output(ohd_ttl['ur1 member of uri2'].format(uri1=provider_uri, uri2=practice_uri))

#translate_provider_to_ttl()
translate_provider_to_ttl_1(practice_id='2')