import pandas as pds
import logging
import os
#import datetime
import numpy as np
#from functools import reduce
#from itertools import groupby
#from operator import itemgetter
from load_resources import curr_dir, ohd_ttl, label2uri, load_ada_material_map, load_ada_procedure_map

def visit_date_test(practice_id='1', filename='visit_dates.ttl', print_ttl=True, save_ttl=True):
    #df_path = os.path.join(curr_dir, '..', 'data', 'Practice1_Patient_History_small.xlsx')
    df_path = os.path.join(curr_dir, '..', 'data', 'Practice1_Patient_History.xlsx')
    df = pds.ExcelFile(df_path).parse()

    visit_df = df[['PBRN_PRACTICE', 'PATIENT_ID', 'TRAN_DATE', 'PROVIDER_ID', 'TABLE_NAME', 'DB_PRACTICE_ID']]

    with open(filename, 'w') as f:
        with open('visit_date_err.txt', 'w') as f_err:

            def output(value_str, print_ttl=print_ttl, save_ttl=save_ttl):
                if print_ttl == True: print value_str
                if save_ttl == True: f.write(value_str)

            def output_err(value_str):
                f_err.write(value_str)
                f_err.write('\n')

            results = []

            for (idx, practiceId, pid, visitDate, providerId, tableName, locationId) in visit_df.itertuples():
                if tableName.lower() == 'transactions':
                    try:
                        id = str(practiceId) + "_" + str(locationId) + "_" + str(pid)

                        date_str = visitDate.strftime('%Y-%m-%d')

                        visit_id = str(practiceId) + "_" + str(locationId) + "_" + str(pid) + "_" + date_str
                        # uri
                        visit_uri = ohd_ttl['visit uri'].format(visit_id=visit_id)
                        patient_uri = ohd_ttl['patient uri by prefix'].format(patient_id=id)

                        results.append([patient_uri] + [date_str])

                    except Exception as ex:
                        print("Problem visit for patient: " + str(pid) + " for practice: " + str(practiceId))
                        logging.exception("message")

            patient_uri_with_visit_dates_df = pds.DataFrame(results, columns=['patient_uri', 'visit_date'])

            #debugging...:
            #patient_uri_first_visit_dates_df = reduce((lambda x, y: x * y), patient_uri_with_visit_dates_df)
            #grouped_df = pds.DataFrame(data=patient_uri_with_visit_dates_df, columns=['patient_uri', 'visit_date']) \
            #    .groupby('patient_uri')
            #print(grouped_df.head(2))
            #test_df = pds.DataFrame(data=patient_uri_with_visit_dates_df, columns=['patient_uri', 'visit_date'])\
            #    .groupby('patient_uri').agg({'visit_date' : lambda x: min(x)})
            #test_df = pds.DataFrame(data=patient_uri_with_visit_dates_df, columns=['patient_uri', 'visit_date']) \
            #    .groupby('patient_uri').agg({'visit_date': lambda x: min(datetime.datetime.strptime(x, '%Y-%m-%d'))})
            #test_df = pds.DataFrame(data=patient_uri_with_visit_dates_df, columns=['patient_uri', 'visit_date']) \
            #    .groupby('patient_uri').agg({'visit_date': [np.min, np.max]})
            #print( len(test_df.index))
            #print(test_df.shape)
            #print(test_df.ix[:,:])

            patient_with_multiindex_date_df = pds.DataFrame(data=patient_uri_with_visit_dates_df, columns=['patient_uri', 'visit_date']) \
                .groupby('patient_uri').agg({'visit_date': [np.min, np.max]})

            patient_with_first_last_date_df = pds.DataFrame(patient_with_multiindex_date_df.to_records())

            first_visit_date_type = label2uri['first dental visit date'].rsplit('/', 1)[-1]
            last_visit_date_type = label2uri['last dental visit date'].rsplit('/', 1)[-1]

            for (idx, patient_uri, first_visit_date, last_visit_date) in patient_with_first_last_date_df.itertuples():
                output(ohd_ttl['declare date property uri'].format(uri=patient_uri, type=first_visit_date_type,
                                                                   date=first_visit_date))
                output(ohd_ttl['declare date property uri'].format(uri=patient_uri, type=last_visit_date_type,
                                                                   date=last_visit_date))

                #print(ohd_ttl['declare date property uri'].format(uri=patient_uri, type=first_visit_date_type,
                #                                                   date=first_visit_date))
                #print(ohd_ttl['declare date property uri'].format(uri=patient_uri, type=last_visit_date_type,
                #                                                   date=last_visit_date))

visit_date_test(practice_id='1')