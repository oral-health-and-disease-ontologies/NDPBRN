import pandas as pds
import os
from load_resources import curr_dir, ohd_ttl, label2uri

def translate_provider_to_ttl_1(practice_id='1', output_f='provider.ttl', input_f= 'Provider_Table.txt', print_ttl=True, save_ttl=True, vendor='ES'):
    # get data from RI-demo-data
    #df_path = os.path.join(curr_dir, '..', 'data', 'RI-demo-data.xlsx')
    #df_path = os.path.join(curr_dir, '..', 'data', 'Practice1_Provider_Table.csv')
    #df_path = os.path.join(curr_dir, '..', 'data', 'Practice1_Provider_Table.xlsx')
    #df_path = os.path.join(curr_dir, '..', 'data', 'Practice' + str(practice_id) + '_Provider_Table.xlsx')
    #df_path = os.path.join(curr_dir, '..', 'data', 'Practice' + str(practice_id) + '_Provider_Table.txt')
    df_path = input_f
    #df = pds.ExcelFile(df_path).parse()
    if vendor == 'ES':
        df = pds.read_csv(df_path, sep='\t', names=["db_practice_id", "provider_id", "status", "position_id", "description"], header=0)
    else:
        df = pds.read_csv(df_path, sep='\t',
                           names=["db_practice_id", "provider_id", "status", "position_id", "title"], header=0)

    with open(output_f, 'w') as f:
        # local function for printing and saving turtle output
        def output(value_str, print_ttl=print_ttl, save_ttl=save_ttl):
            if print_ttl == True: print value_str
            if save_ttl == True: f.write(value_str)

        # output prefixes for ttl file
        if(vendor == 'ES'):
            practice_id = 'A_' + str(practice_id)
        else:
            practice_id = 'B_' + str(practice_id)
        prefix_str = ohd_ttl['prefix'].format(practice_id=practice_id)
        output(prefix_str)

        output(':G_' + practice_id + ' {')

        # practice
        practice_uri = ohd_ttl['practice uri'].format(practice_id=practice_id)
        # define types
        practice_type = label2uri['dental health care organization']
        practice_label = "practice_" + str(practice_id)
        # delcare individuals
        #practiceidstring = 'NDPBRN ' + vendor + ' practice ' + str(practice_id)
        #if(vendor == 'ES'):
        #    vendorChar = 'A '
        #else:
        #    vendorChar = 'B '
        #practiceidstring = 'NDPBRN practice ' + vendorChar + str(practice_id)
        practiceidstring = 'NDPBRN practice ' + str(practice_id)
        output(ohd_ttl['declare practice'].format(uri=practice_uri, type=practice_type, label=practice_label,
                                                  practice_id_str=practiceidstring))

        for row in df.itertuples():
#            if row.PROVIDER_ID.lower() != 'bs' and row.PROVIDER_ID.lower() != 'ss':
            # set variables need to format ttl string
            # new headers from exported provider txt file: db_practice_id	provider_id	status	position_id	description
            #id = str(row.PBRN_PRACTICE) + "_" + str(row.DB_PRACTICE_ID) + "_" + str(row.PROVIDER_ID)
            id = str(practice_id) + "_" + str(row.db_practice_id) + "_" + str(row.provider_id)
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
                   format(uri=provider_uri, type=provider_type, label=provider_label, practice_id_str=practiceidstring))

            output(ohd_ttl['declare individual uri'].
                format(uri=role_uri, type=provider_role_type, label=role_label, practice_id_str=practiceidstring))

            # if string "office" is in position string, print office staff role and relate it to the provider:
            #if "office" in row.POSITION.lower():
            if vendor == 'ES':
                description = row.description
            else:
                description = row.title
            if pds.notnull(description):
                roleDesc = str(description).lower()
                if "office" in roleDesc:
                    output(ohd_ttl['declare individual uri'].
                            format(uri=office_staff_role_uri, type=office_staff_role_type, label=office_staff_role_label,
                                    practice_id_str=practiceidstring))
                    output(ohd_ttl['uri1 has role uri2'].
                            format(uri1=provider_uri, uri2=office_staff_role_uri))
            # else:
            #     roleDesc = row.rsctype
            #     if 2 == roleDesc:
            #         output(ohd_ttl['declare individual uri'].
            #                format(uri=office_staff_role_uri, type=office_staff_role_type, label=office_staff_role_label,
            #                       practice_id_str=practiceidstring))
            #         output(ohd_ttl['uri1 has role uri2'].
            #                format(uri1=provider_uri, uri2=office_staff_role_uri))

            # relate individuals
            output(ohd_ttl['uri1 has role uri2'].
                format(uri1=provider_uri, uri2=role_uri))

            output(ohd_ttl['ur1 member of uri2'].format(uri1=provider_uri, uri2=practice_uri))

        output('}')

#translate_provider_to_ttl()
#translate_provider_to_ttl_1(practice_id='1', vendor='ES',
#                             input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Provider_Table.txt',
#                             output_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/provider.ttl')
#translate_provider_to_ttl_1(practice_id='2', vendor='ES',
#                             input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_2/Provider_Table.txt',
#                             output_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_2/provider.trig')
#translate_provider_to_ttl_1(practice_id='1', vendor='dentrix',
#                             input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/Dentrix/PRAC_1/Dentrix_Pract1_Provider_Table.txt',
#                             output_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/dentrix/PRAC_1/provider.ttl')
# translate_provider_to_ttl_1(practice_id='1', vendor='dentrix',
#                             input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/dentrix_sample/provider table.txt',
#                             output_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/dentrix_sample/provider.ttl')
