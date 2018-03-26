import os

from patient_to_ttl import translate_patient_to_ttl
from provider_to_ttl import translate_provider_to_ttl_1
from visit_to_ttl import translate_visit_to_ttl
from visit_dates import next_visit_ttl, first_last_visit_date_ttl
from procedure_to_ttl import print_procedure_ttl
from condition_to_ttl import print_condition_ttl
import services_to_ttl as services


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

    providerTableFile = 'Provider.txt'
    patientTableFile = '_study_patients.txt'
    patietnHistoryTFile = '_tooth_history.txt'

    provderOutputFile = 'provider.trig'
    patientOutputFile = 'patient.trig'
    visitOutputFile = 'visit.trig'
    visitFirstLastOutputFile = 'visit_dates.trig'
    nextVisitOutputFile = 'next_visit_dates.trig'

    for i in range(prac_lower_num, prac_upper_num+1):
        input_p = data_p_root + 'PRAC_' + str(i) + '/'
        output_p = output_p_root + 'PRAC_' + str(i) + '/'

        if not os.path.exists(output_p):
            os.makedirs(output_p)

        if vendor.lower() == 'es':
            patientTableFile = 'A_' + str(i) + '_study_patients.txt'
            patietnHistoryTFile = 'A_' + str(i) + '_tooth_history.txt'

        if vendor.lower() == 'dentrix':
            providerTableFile = 'PRAC' + str(i) + '_Dentrix_Provider_Table.txt'
            patientTableFile = 'PRAC' + str(i) + '_Dentrix_Patient_Table.txt'
            patietnHistoryTFile = 'PRAC' + str(i) + '_Dentrix_ToothHistory_Table.txt'

        translate_provider_to_ttl_1(practice_id=str(i), vendor=vendor,
                                    input_f=input_p + providerTableFile,
                                    output_f=output_p + provderOutputFile, print_ttl=False)
        translate_patient_to_ttl(practice_id=str(i), vendor=vendor,
                                 input_f=input_p + patientTableFile,
                                 output_f=output_p + patientOutputFile, print_ttl=False)
        translate_visit_to_ttl(practice_id=str(i), vendor=vendor,
                               input_f=input_p + patietnHistoryTFile,
                               output_f=output_p + visitOutputFile, print_ttl=False)
        next_visit_ttl(practice_id=str(i), vendor=vendor,
                       input_f=input_p + patietnHistoryTFile,
                       output_f=output_p + nextVisitOutputFile,
                       output_p=output_p, print_ttl=False)
        first_last_visit_date_ttl(practice_id=str(i), vendor=vendor,
                                  input_f=input_p + patietnHistoryTFile,
                                  output_f=output_p + visitFirstLastOutputFile,
                                  output_p=output_p, print_ttl=False)
        for j in range(1, 19):
            print_procedure_ttl(practice_id=str(i), procedure_type=str(j),
                            input_f=input_p + patietnHistoryTFile,
                            output_p=output_p,
                            vendor=vendor, print_ttl=False)

        for j in range(1, 3):
            print_condition_ttl(practice_id=str(i), condition_type=str(j),
                            input_f=input_p + patietnHistoryTFile,
                            output_p=output_p,
                            vendor=vendor, print_ttl=False)

        for j in range(1, 19):
            services.print_procedure_ttl(practice_id=str(i), procedure_type=str(j),
                            input_f=input_p + patietnHistoryTFile,
                            output_p=output_p,
                            vendor=vendor, print_ttl=False)

## test call all for practice 1 testing
#testAllTranslationWithPRAC_1()
## run all ES for practice number from 1 ~ prac_num
runAllPractice(data_p_root='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/ES/',
               output_p_root='/Users/cwen/development/pyCharmHome/NDPBRN/src/translate/translate_data/ES/',
               vendor='ES',
               prac_lower_num=1,
               prac_upper_num=1)
## test with dentrix
# runAllPractice(data_p_root='/Users/cwen/development/pyCharmHome/NDPBRN/src/data/Dentrix/',
#               output_p_root='/Users/cwen/development/pyCharmHome/NDPBRN/src/translate/translate_data/Dentrix/',
#               vendor='dentrix',
#               prac_lower_num=39,
#               prac_upper_num=45)
