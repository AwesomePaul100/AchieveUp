import requests
import json
import time
## To Flatten the JSON
from flatten_json import flatten

skills = []
skills_descriptions = []

# Now dynamically add the skills via JSON file.

'''# Opening JSON file
f = open('data.json')

# returns JSON object as a dictionary
data = json.load(f)

# Iterating through the json list
for i in data['options']:
    print(i)
    skills.append(i)
    
# Opening JSON file
f = open('data.json')

# returns JSON object as a dictionary
data = json.load(f)

# Iterating through the json list
for i in data['badges']:
    print(i)
    skills_descriptions.append(i)
skills_length = len(skills)
skills_descriptions_length = len(skills_descriptions)
print(skills_length, skills_descriptions_length)
updated_skills = str(skills).replace(' ','')
updated_descriptions = (str(skills_descriptions).replace(' ','_')).replace(',_',',')
print("skills:", updated_skills)
print("skills_descriptions:", updated_descriptions)
'''
# Opening JSON file
f = open('data.json')

# returns JSON object as a dictionary
data = json.load(f)

server_ip = data['ip'][0]

# Closing file
f.close()

print("imports")

def main(question):
    #time.sleep(1)
    #print( 'http://192.168.168.103:8000/square?number=In_a_STEM_course,_with_'+str(skills_length)+'_skills_listed_here:_'+updated_descriptions+',_and_the_following_acronyms:_'+updated_skills+'_are_used_to_associate_with_those_skillsets_respectfully_in_the_same_order._With_the_following_question:_"'+question+'",_please_select_up_to_5_skills_you_would_use_to_classify_the_question_skillsets._You_do_not_need_to_select_5_skills,_and_please_only_respond_with_the_acronyms.')
    #response = requests.get('http://192.168.168.103:8000/square?number=Please_respond_in_one_word_for:_' + '"' + question + '"')
    # In_a_STEM_course,_with_<#>_skills_listed_here:_<skills_descriptions>,_and_the_following_acronym's:_<skills>_associated_with_the_skillsets._With_the_following_question:_<question>,_please_select_up_to_5_skills_you_would_use_to_classify_the_question_skillsets._You_do_not_need_to_select_5_skills,_and_please_only_respond_with_the_acronym's.
    try:
        #print('http://192.168.168.103:8000/square?number=May_you_please_list_low-level_skills_students_are_expected_to_learn_in_' + str(question) + '_UCF_college_course?_PLEASE_ONLY_RESPOND_WITH_the_skills_using_commas_to_seperate_them_NO_EXPLANATION_before_or_after_NECESSARY_thank_you.')
        
        response = requests.get('http://'+server_ip+':8000/square?number=May_you_please_list_what_technical_low_level_skills_are_expected_to_learn_in_a_' + str(question) + '_course_at_the_Univeristy_of_central_florida?_PLEASE_ONLY_RESPOND_WITH_the_skills_using_commas_to_seperate_them_NO_EXPLANATION_before_or_after_NECESSARY_thank_you.')
        #response = requests.get('http://192.168.168.103:8000/square?number=hey.')
    except ZeroDivisionError:
        try:
            print("Error: cannot divide by zero!")
            response = "error"
        except Exception as e:
            print(f"An error occurred while printing the message: {e}")
            response = "error"
    #response = requests.get('http://192.168.168.103:8000/square?number=Please_respond_in_one_word_for:_' + '"' + question + '"')
    print(str(response))
    if str(response) == "<Response [500]>":
        #print ("yo")
        return "error"
    if str(response) == "<Response [200]>":
        print("got solutions")
        return(response.json()['result'])


'''python_client http://192.168.168.103:8000/square?number=In_a_STEM_course,_with_17_skills_listed_here:_['Memory_capacity,hierarchy,and_storage_devices','Digital_signal_communication,busing_and_Interfacing','Processor_Performance_Metrics,and_Benchmarking_','Instruction_Encoding_and_Datapath_design','Integrated_Circuit_materials_and_Fabrication','Floating-point_and_numeric_intensive_acceleration','In_circuit_emulation_and_debugging','Metrics_of_Performance_and/or_SI_Units','Energy_Analysis_or_Conversion','Computational/Algorithmic_Thinking','Conduct_Directed_Design_Process','Conduct_Open-Ended_Design','Conduct_Tradeoff_Analysis_(A_vs_B)','Logic_/_Operational_Flow_Analysis','Engineering_Life_Cycle_(Reliability,Maintainability,Practicality)','Data/Info_Representation','Tools_for_Simulation_/_Emulator_/_MATLAB'],_and_the_following_acronyms:_['D-ECE-1','D-ECE-2','D-ECE-3','D-ECE-4','D-ECE-5','D-ECE-6','D-ECE-7','T1','T2','T3','T4','T5','T6','T7','T8','A1','A2']_associated_with_the_skillsets._With_the_following_question:_hey,_please_select_up_to_5_skills_you_would_use_to_classify_the_question_skillsets._You_do_not_need_to_select_5_skills,_and_please_only_respond_with_the_acronyms.'''

'''python_client http://192.168.168.103:8000/square?number=In_a_STEM_course,_with_17_skills_listed_here:_['Memory_capacity,hierarchy,and_storage_devices','Digital_signal_communication,busing_and_Interfacing','Processor_Performance_Metrics,and_Benchmarking_','Instruction_Encoding_and_Datapath_design','Integrated_Circuit_materials_and_Fabrication','Floating-point_and_numeric_intensive_acceleration','In_circuit_emulation_and_debugging','Metrics_of_Performance_and/or_SI_Units','Energy_Analysis_or_Conversion','Computational/Algorithmic_Thinking','Conduct_Directed_Design_Process','Conduct_Open-Ended_Design','Conduct_Tradeoff_Analysis_(A_vs_B)','Logic_/_Operational_Flow_Analysis','Engineering_Life_Cycle_(Reliability,Maintainability,Practicality)','Data/Info_Representation','Tools_for_Simulation_/_Emulator_/_MATLAB'],_and_the_following_acronyms:_['D-ECE-1','D-ECE-2','D-ECE-3','D-ECE-4','D-ECE-5','D-ECE-6','D-ECE-7','T1','T2','T3','T4','T5','T6','T7','T8','A1','A2']_are_used_to_associate_with_those_skillsets_respectfully_in_the_same_order._With_the_following_question:_hey,_please_select_up_to_5_skills_you_would_use_to_classify_the_question_skillsets._You_do_not_need_to_select_5_skills,_and_please_only_respond_with_the_acronyms.'''

# IP list: 192.168.168.103,10.173.214.164
#response = requests.get('http://10.173.214.164:8000/square?number=In_a_STEM_course,_with_'+str(skills_length)+'_skill_descriptions_listed_here:_'+updated_descriptions+',_and_the_following_acronyms:_'+updated_skills+'_associated_with_the_skillsets._With_the_following_question:_"'+question+'",_please_select_up_to_5_skills_you_would_use_to_classify_the_question_skillsets._You_do_not_need_to_select_5_skills,_just_the_ones_you_are_super_confident_with,_and_PLEASE_ONLY_RESPOND_WITh_the_ACRONYMS_using_commas_to_seperate_them_NO_EXPLANATION_before_or_after_NECESSARY_thank_you.')
