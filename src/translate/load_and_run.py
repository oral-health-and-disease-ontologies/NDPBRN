import os

from patient_to_ttl import translate_patient_to_ttl
from provider_to_ttl import translate_provider_to_ttl_1
from visit_to_ttl import translate_visit_to_ttl
from visit_dates import next_visit_ttl, first_last_visit_date_ttl
from procedure_to_ttl import print_procedure_ttl

#test with practice 1 with ES
def testAllTranslationWithPRAC_1():
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
               output_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/next_visit_dates.ttl',
               output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/')
    first_last_visit_date_ttl(practice_id='1', vendor='ES',
                          input_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/PRAC_1/Patient_History.txt',
                          output_f='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/visit_dates.ttl',
                          output_p='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/PRAC_1/')
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

def runAllPractice(data_p_root='./', output_p_root='./translated/', vendor='ES', prac_lower_num=1, prac_upper_num=1):

    providerTableFile = 'Provider_Table.txt'
    patientTableFile = 'Patient_Table.txt'
    patietnHistoryTFile = 'Patient_History.txt'

    provderOutputFile = 'provider.ttl'
    patientOutputFile = 'patient.ttl'
    visitOutputFile = 'visit.ttl'
    visitFirstLastOutputFile = 'visit_dates.ttl'
    nextVisitOutputFile = 'next_visit_dates.ttl'

    for i in range(prac_lower_num, prac_upper_num+1):
        input_p = data_p_root + 'PRAC_' + str(i) + '/'
        output_p = output_p_root + 'PRAC_' + str(i) + '/'

        if not os.path.exists(output_p):
            os.makedirs(output_p)

        if vendor.lower() == 'dentrix':
            providerTableFile = 'Dentrix_Pract' + str(i) + '_Provider_Table.txt'
            patientTableFile = 'Dentrix_Pract' + str(i) + '_Patient_Table.txt'
            patietnHistoryTFile = 'Dentrix_Pract' + str(i) + '_Patient_History.txt'

        translate_provider_to_ttl_1(practice_id=str(i), vendor=vendor,
                                    input_f=input_p + providerTableFile,
                                    output_f=output_p + provderOutputFile)
        translate_patient_to_ttl(practice_id=str(i), vendor=vendor,
                                 input_f=input_p + patientTableFile,
                                 output_f=output_p + patientOutputFile)
        translate_visit_to_ttl(practice_id=str(i), vendor=vendor,
                               input_f=input_p + patietnHistoryTFile,
                               output_f=output_p + visitOutputFile)
        next_visit_ttl(practice_id=str(i), vendor=vendor,
                       input_f=input_p + patietnHistoryTFile,
                       output_f=output_p + nextVisitOutputFile,
                       output_p=output_p)
        first_last_visit_date_ttl(practice_id=str(i), vendor=vendor,
                                  input_f=input_p + patietnHistoryTFile,
                                  output_f=output_p + visitFirstLastOutputFile,
                                  output_p=output_p)
        for j in range(1, 11):
            print_procedure_ttl(practice_id=str(i), procedure_type=str(j),
                            input_f=input_p + patietnHistoryTFile,
                            output_p=output_p,
                            vendor=vendor)

## test call all for practice 1 testing
#testAllTranslationWithPRAC_1()
## run all ES for practice number from 1 ~ prac_num
#runAllPractice(data_p_root='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/',
#               output_p_root='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/',
#               vendor='ES',
#               prac_lower_num=1,
#               prac_upper_num=3)
## test with dentrix
runAllPractice(data_p_root='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/Dentrix/',
               output_p_root='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/translated/dentrix/',
               vendor='dentrix',
               prac_lower_num=1,
               prac_upper_num=1)
