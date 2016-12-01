import pandas as pds
import os
from load_resources import curr_dir, ohd_ttl, label2uri

def translate_practice_to_ttl(practice_id='3', filename='practice.ttl', print_ttl=True, save_ttl=True):
    # get data from RI-demo-data
    df_path = os.path.join(curr_dir, '..', 'data', 'RI-demo-data-practice.xlsx')
    df = pds.ExcelFile(df_path).parse()

    patient_df = df[['LOCATION_ID']]

    # testing...
    # print patient_df

    with open(filename, 'w') as f:
        # local function for printing and saving turtle output
        def output(value_str, print_ttl=print_ttl, save_ttl=save_ttl):
            if print_ttl == True: print value_str
            if save_ttl == True: f.write(value_str)

        # output prefixes for ttl file
        prefix_str = ohd_ttl['prefix for practice'].format(practice_id=practice_id)
        output(prefix_str)

        # define uri
        practice_uri = ohd_ttl['practice uri'].format(practice_id=practice_id)
        # define types
        practice_type = label2uri['dental health care organization']
        # delcare individuals
        output(ohd_ttl['declare practice'].format(uri=practice_uri, type=practice_type, label="practice " + str(practice_id)))

        #TODO: confirm with Bill - we concludded we don't have location_id from the DB, so the practice_id is the only think we have
        # print ttl for each patient
        for (idx, lid) in patient_df.itertuples():
            location_uri = ohd_ttl['location uri'].format(location_id=lid)

            output(ohd_ttl['declare practice'].format(uri=location_uri, type=practice_type))

            # relate individuals
            output(ohd_ttl['ur1 member of uri2'].format(uri1=location_uri, uri2=practice_uri))


translate_practice_to_ttl()