from load_resources import curr_dir, ohd_ttl, label2uri

from patient_to_ttl import translate_patient_to_ttl
from provider_to_ttl import translate_provider_to_ttl_1
from visit_to_ttl import translate_visit_to_ttl
from visit_dates import first_last_visit_date_ttl, next_visit_ttl
from procedure_to_ttl import print_procedure_ttl

#test with practice 1 with ES
translate_provider_to_ttl_1(practice_id='1', vendor='ES',
                            input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Provider_Table.txt',
                            output_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/provider.ttl')
translate_patient_to_ttl(practice_id='1', vendor='ES',
                            input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Patient_Table.txt',
                            output_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/patient.ttl')
translate_visit_to_ttl(practice_id='1', vendor='ES',
                       input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Patient_History.txt',
                       output_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/visit.ttl')
next_visit_ttl(practice_id='1', vendor='ES',
               input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Patient_History.txt',
               output_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/next_visit_dates.ttl')
first_last_visit_date_ttl(practice_id='1', vendor='ES',
                          input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Patient_History.txt',
                          output_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/visit_dates.ttl')
print_procedure_ttl(practice_id='1', procedure_type=1,
                    input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Patient_History.txt',
                    output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/',
                    vendor='ES')
print_procedure_ttl(practice_id='1', procedure_type=2,
                    input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Patient_History.txt',
                    output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/',
                    vendor='ES')
print_procedure_ttl(practice_id='1', procedure_type=3,
                    input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Patient_History.txt',
                    output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/',
                    vendor='ES')
print_procedure_ttl(practice_id='1', procedure_type=4,
                    input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Patient_History.txt',
                    output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/',
                    vendor='ES')
print_procedure_ttl(practice_id='1', procedure_type=5,
                    input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Patient_History.txt',
                    output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/',
                    vendor='ES')
print_procedure_ttl(practice_id='1', procedure_type=6,
                    input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Patient_History.txt',
                    output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/',
                    vendor='ES')
print_procedure_ttl(practice_id='1', procedure_type=7,
                    input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Patient_History.txt',
                    output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/',
                    vendor='ES')
print_procedure_ttl(practice_id='1', procedure_type=8,
                    input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Patient_History.txt',
                    output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/',
                    vendor='ES')
print_procedure_ttl(practice_id='1', procedure_type=9,
                    input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Patient_History.txt',
                    output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/',
                    vendor='ES')
print_procedure_ttl(practice_id='1', procedure_type=10,
                    input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Patient_History.txt',
                    output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/',
                    vendor='ES')
