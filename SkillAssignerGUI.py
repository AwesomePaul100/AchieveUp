# Paul Amoruso
# Instructor: Dr. DeMara
# The following script looks at the data from the statistics api call and then compares with
# the skills that corelate to it.
#authorisation test
import requests
import json
import pdb
import pandas as pd
import csv
import matplotlib.pyplot as plt

from pprint import pprint   # pretty-print

## To Flatten the JSON
from flatten_json import flatten

import os
import numpy as np
import the_binary
import math
import ast

# List of the skills
skillsGUI = []

# Now dynamically add the skills via JSON file.

# Opening JSON file
f = open('data.json')

# returns JSON object as a dictionary
data = json.load(f)

# Iterating through the json list
for i in data['options']:
    print(i)
    skillsGUI.append(i)

# Send API request to retrive the data from Canvas
headers ={'Authorization':'Bearer '+data['token'][0]}

########### Url to extract Quiz questions details
# We put the url here so the code can just call this value whenever it needs it.
url = 'https://webcourses.ucf.edu/api/v1/courses/1158000000'+ data['url'][0] +'/quizzes/1158000000'+ data['url'][1]

# Closing file
f.close()

# List of times each is obtained via student.
# Must be the same length in pie chart.
percentskills = [0] * len(skillsGUI)

########### Url to extract Quiz questions details
url_quiz_ques = url+'/questions'
r_quiz_ques = requests.get(url_quiz_ques,headers = headers)
print(r_quiz_ques.status_code)
if r_quiz_ques.status_code != 200:
    print("\nPlease check the token\n")
json_data = json.loads(r_quiz_ques.text)

# Python dictionary to house the points of the students.
ids = {}
students = {}
# To keep track of all the possible skills they could get.
total_points = {}

df1 = []
df2 = []

question_counter = 0
question_spreadsheet = []

# This function reads cells from the questions.csv file (questions_tagged_with_skills).
def read_cell(x, y):
    with open(title + '_' + 'questions.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        y_count = 0
        for n in reader:
            if y_count == y:
                cell = n[x]
                return cell
            y_count += 1


url_quiz_name = url
r_quiz_name = requests.get(url_quiz_name,headers = headers)
print(r_quiz_name.status_code)
json_quiz_name_data = json.loads(r_quiz_name.text)

title = json_quiz_name_data['title']
print(json_quiz_name_data['title'])

url_quiz_stats = url + '/statistics/?per_page=150'
r_quiz_stats = requests.get(url_quiz_stats,headers = headers)
print(r_quiz_stats.status_code)
json_quiz_stat_data = json.loads(r_quiz_stats.text)

number_of_questions = 0
question_number = 1

# Read the data from the JSON data
for qdata in json_quiz_stat_data['quiz_statistics']:
    for q1data in qdata['question_statistics']:
        #print(q1data,'\n')
        
        # We have to make sure that we have the right question
        # 132732739
        print("looking for ", q1data['id'])
        if q1data['id'] == read_cell(1, question_number) or q1data['id'] == 132732739:
            print("it is the correct id value")
        else:
            for r in range(100):
                print("range is at", r)
                if q1data['id'] == read_cell(1, 1 + r) or str(q1data['id'])+"a" == read_cell(1, 1 + r):
                    print(str(q1data['id']) + " is in " + str(read_cell(1, 1 + r)))
                    question_number = r + 1
                    break
        
        if "answer_sets" in q1data:
            #pdb.set_trace()
            for q1data_multiple in q1data['answer_sets']:
                question_stat = q1data_multiple['answers']
                number_of_questions += 1
                # Create a dataframe and put the parsed data into it
                df3 = pd.DataFrame(question_stat)
               
                zip_object = zip(df3['correct'], df3['user_names'], df3['user_ids'])
                for element1, element2, element3 in zip_object:
                    if element1 == True:
                        for id in element3:
                            if id in students:
                                for val in range(5):
                                    print(id, "is getting points")
                                    print(read_cell(3+val, question_number))
                                    if (read_cell(3+val, question_number) in students[id]) and (read_cell(3+val, question_number) != None):
                                        students[id][read_cell(3+val, question_number)] += 1
                                        total_points[id][read_cell(3+val, question_number)] += 1
                                    elif read_cell(3+val, question_number) != None:
                                        new = {read_cell(3+val, question_number): 1}
                                        students[id].update(new)
                                        total_points[id].update(new)
                            else:
                                print("In statment 1")
                                students[id] = {}
                                if id not in total_points:
                                    total_points[id] = {}
                                for val in range(5):
                                    print(id, "is getting points for the first time")
                                    print(read_cell(3+val, question_number))
                                    if read_cell(3+val, question_number) != None:
                                        students[id][read_cell(3+val, question_number)] = 1
                                    if (id not in total_points) and (read_cell(3+val, question_number) != None):
                                        total_points[id][read_cell(3+val, question_number)] = 1
                                    else:
                                        if (read_cell(3+val, question_number) in total_points[id]) and (read_cell(3+val, question_number) != None):
                                            total_points[id][read_cell(3+val, question_number)] += 1
                                        elif read_cell(3+val, question_number) != None:
                                            new = {read_cell(3+val, question_number): 1}
                                            total_points[id].update(new)
                    else:
                        for id in element3:
                            if id in total_points:
                                for val in range(5):
                                    print(id, " skill not gotten")
                                    print(read_cell(3+val, question_number))
                                    if (read_cell(3+val, question_number) in total_points[id]) and (read_cell(3+val, question_number) != None):
                                        #students[id][read_cell(3+val, question_number)] += 1
                                        total_points[id][read_cell(3+val, question_number)] += 1
                                        #print(total_points[33251618])
                                    elif read_cell(3+val, question_number) != None:
                                        new = {read_cell(3+val, question_number): 1}
                                        #students[id].update(new)
                                        total_points[id].update(new)
                            else:
                                print("In else statment 1")
                                #students[id] = {}
                                total_points[id] = {}
                                for val in range(5):
                                    print(id, " skill not gotten for the first time")
                                    print(read_cell(3+val, question_number))
                                    #students[id][read_cell(3+val, question_number)] = 1
                                    if read_cell(3+val, question_number) != None:
                                        total_points[id][read_cell(3+val, question_number)] = 1
                    
                                    #question_number += 1
                
                question_number += 1

        else:
                question_stat = q1data['answers']
                print('in else')
                number_of_questions += 1
                # Create a dataframe and put the parsed data into it
                df3 = pd.DataFrame(question_stat)
                
                # Need to look if it is a calculated question with no answer.
                if q1data['question_type'] == "calculated_question":
                    zip_object = zip(df3['user_names'], df3['user_ids'])
                    for element1, element2 in zip_object:
                        for id in element2:
                            if id in students:
                                print("In statment")
                                for val in range(5):
                                    print(id, "is getting points")
                                    print(read_cell(3+val, question_number))
                                    if (read_cell(3+val, question_number) in students[id]) and (read_cell(3+val, question_number) != None):
                                        students[id][read_cell(3+val, question_number)] += 1
                                        total_points[id][read_cell(3+val, question_number)] += 1
                                    elif read_cell(3+val, question_number) != None:
                                        new = {read_cell(3+val, question_number): 1}
                                        students[id].update(new)
                                        total_points[id].update(new)
                                    #question_number += 1
                            else:
                                print("In statment 2")
                                students[id] = {}
                                if id not in total_points:
                                    total_points[id] = {}
                                for val in range(5):
                                    print(id, "is getting points for the first time")
                                    print(read_cell(3+val, question_number))
                                    if read_cell(3+val, question_number) != None:
                                        students[id][read_cell(3+val, question_number)] = 1
                                    if (id not in total_points) and (read_cell(3+val, question_number) != None):
                                        total_points[id][read_cell(3+val, question_number)] = 1
                                    else:
                                        if (read_cell(3+val, question_number) in total_points[id]) and (read_cell(3+val, question_number) != None):
                                            total_points[id][read_cell(3+val, question_number)] += 1
                                        elif read_cell(3+val, question_number) != None:
                                            new = {read_cell(3+val, question_number): 1}
                                            total_points[id].update(new)
                    continue
                zip_object = zip(df3['correct'], df3['user_names'], df3['user_ids'])
                for element1, element2, element3 in zip_object:
                    if element1 == True:
                        for id in element3:
                            if id in students:
                                print("In statment")
                                for val in range(5):
                                    print(id, "is getting points")
                                    print(read_cell(3+val, question_number))
                                    if (read_cell(3+val, question_number) in students[id]) and (read_cell(3+val, question_number) != None):
                                        students[id][read_cell(3+val, question_number)] += 1
                                        total_points[id][read_cell(3+val, question_number)] += 1
                                    elif read_cell(3+val, question_number) != None:
                                        new = {read_cell(3+val, question_number): 1}
                                        students[id].update(new)
                                        total_points[id].update(new)
                                    #question_number += 1
                            else:
                                print("In statment 2")
                                students[id] = {}
                                if id not in total_points:
                                    total_points[id] = {}
                                for val in range(5):
                                    print(id, "is getting points for the first time")
                                    print(read_cell(3+val, question_number))
                                    if read_cell(3+val, question_number) != None:
                                        students[id][read_cell(3+val, question_number)] = 1
                                    if (id not in total_points) and (read_cell(3+val, question_number) != None):
                                        total_points[id][read_cell(3+val, question_number)] = 1
                                    else:
                                        if (read_cell(3+val, question_number) in total_points[id]) and (read_cell(3+val, question_number) != None):
                                            total_points[id][read_cell(3+val, question_number)] += 1
                                        elif read_cell(3+val, question_number) != None:
                                            new = {read_cell(3+val, question_number): 1}
                                            total_points[id].update(new)
                    else:
                        for id in element3:
                            if id in total_points:
                                for val in range(5):
                                    #print(id, "is getting points")
                                    #print(read_cell(3+val, question_number))
                                    if (read_cell(3+val, question_number) in total_points[id]) and (read_cell(3+val, question_number) != None):
                                        #students[id][read_cell(3+val, question_number)] += 1
                                        total_points[id][read_cell(3+val, question_number)] += 1
                                    elif read_cell(3+val, question_number) != None:
                                        new = {read_cell(3+val, question_number): 1}
                                        #students[id].update(new)
                                        total_points[id].update(new)
                            else:
                                print("In else statment 2")
                                #students[id] = {}
                                total_points[id] = {}
                                for val in range(5):
                                    #print(id, "is getting points for the first time")
                                    #print(read_cell(3+val, question_number))
                                    #students[id][read_cell(3+val, question_number)] = 1
                                    if read_cell(3+val, question_number) != None:
                                        total_points[id][read_cell(3+val, question_number)] = 1
                                    #question_number += 1
                    #print(element1, element2)
                question_number += 1
                

# Merge the all the questions data in the quiz in one dataframe
#df5 = pd.concat(df4, ignore_index=True)
#quiz_stat = pd.concat([quiz_questions,df5],axis = 1, sort = False)
#pprint(quiz_stat)
# The following print statements print our the python dictionaries used for this Python script.
print("The dictionary with all the students and how many times they got the particular skill:\n",students)
print("The dictionary with all the students and all the possible skills they could have gotten:\n",total_points)
#print ('-----------------------------\n' + url[0:60] + '/users/?per_page=150')
url_users = url[0:60] + '/users/?per_page=150'
r_users = requests.get(url_users,headers = headers)
print(r_users.status_code)
json_users_data = json.loads(r_users.text)

url_users = url[0:60] + '/users/?page=2&per_page=150'
r_users = requests.get(url_users,headers = headers)
print(r_users.status_code)
json_users_data = json_users_data + json.loads(r_users.text)

print("json_users_data:",json_users_data)

#print (read_cell(3, 1))
percent = 100

# Traverse the students in the api call to make a list of students with their skills.
student_skills = []

# ASEE-SE statistics to measure achiever over the oprotunity.
oprotunity = [0] * len(skillsGUI)
acheived_skills = [0] * len(skillsGUI)

# If it is on webcourses.
webcourses = False
for users in json_users_data:
    skills_list = []
    if users["id"] in students:
        print("There is " + str(number_of_questions)+ " questions, and " + str(users['id']) + " got " + str(students[users["id"]]) + " correct")
        # Traverse the skills the student got and how many times our of all the possible times they could have gotten it correct.
        for skills in students[users["id"]]:
            percent = (students[users["id"]][skills]/total_points[users["id"]][skills]) * 100
            if skills != '':
                oprotunity[skillsGUI.index(str(skills))] = oprotunity[skillsGUI.index(str(skills))] + (total_points[users["id"]][skills])
                acheived_skills[skillsGUI.index(str(skills))] = acheived_skills[skillsGUI.index(str(skills))] + (students[users["id"]][skills])
                
            print("Student " + str(users["id"]) + " got "  + str(percent) + "% for skill " + str(skills) )
            # We check how well they did on the skill, if it is 90 percent or greater then they can claim the skill.
            if percent >= 95:
                # We append that skill to the lists of all the skills they got.
                skills_list.append(skills)
                # Add to the percentskills array so that it can be used in pie chart.
                if skills != '':
                    percentskills[skillsGUI.index(str(skills))] = percentskills[skillsGUI.index(str(skills))] + 1
        print(skills_list)
        # Prepare a list for the rows in the csv file.
        # In wbcourses we still have to append the "sis_user_id" to it.
        if users["sis_user_id"]:
            student_skills.append([users["id"], users["sis_user_id"], users["name"], skills_list, users["email"]])
            webcourses = True
        else:
            student_skills.append([users["id"], users["name"], skills_list],users["email"])
    #print(users["id"], '\n')
#print(student_skills)
# So we know if we need another column.
if webcourses:
    spreadsheet = pd.DataFrame(student_skills, columns = ['Ids', 'NIDs', 'Names', 'Skills', 'Emails'])
else:
    spreadsheet = pd.DataFrame(student_skills, columns = ['Ids', 'Names', 'Skills','Emails'])
    
#print(read_cell(100, 100))

# This outputs the csv file so that it is ready for an instructure to see the skills the student got on the assignment.
spreadsheet.to_csv('Student_skills_'+json_quiz_name_data['title']+'.csv')
print("The GUI values: ", skillsGUI, percentskills)

# Prior to the spreadsheet.
# Specify path
path = "Student_Skill_Status.csv"
   
# Now check whether the specified path exists or not.
isExist = os.path.exists(path)
print("the file: ", isExist)

# Now calculate the percentages.
Sum = sum(percentskills)
skill_list = []
if not isExist:
    # Making spreadsheet.
      
    # Make a list of 100 cells.
    empty_percentage_list = [0 for x in range(100)]
    empty_skill_list = ['' for x in range(100)]
    
    print(spreadsheet, Sum)
    list_for_thecsv = percentskills + empty_percentage_list
    for i in range(len(list_for_thecsv)):
        print(str(round(((list_for_thecsv[i]/Sum) * 100), 2)))
        list_for_thecsv[i] = str(round(((list_for_thecsv[i]/Sum) * 100), 2)) + "%"
        #percentskills[i] = (percentskills[i]/Sum) * 100

    # Assign data of lists.
    data = {'Skills': skillsGUI + empty_skill_list, json_quiz_name_data['title']: list_for_thecsv}
      
    # Create DataFrame
    spreadsheet = pd.DataFrame(data)
      
    # Print the output.
    spreadsheet.to_csv("Student_Skill_Status.csv")

else:
    # creating a data frame
    #skillsGUI.append("yo")
    df = pd.read_csv("Student_Skill_Status.csv")
    print(df.head())
    skill_list = df["Skills"].values.tolist()
    print(skill_list)
    newpercents = len(skill_list) * ['']
    print("new percents ", newpercents)
    thecounter = 0
    for i in skillsGUI:
        newpercents[skill_list.index(i)] = str(round(((percentskills[thecounter]/Sum) * 100), 2)) + "%"
        thecounter +=1
    df[json_quiz_name_data['title']+"new"] = newpercents
    for skills in skillsGUI:
        if skills not in skill_list:
            #skill_list[skill_list.index('')] = skills
            i = 0
            for j in skill_list:
                if(pd.isnull(j)):
                   print(str(j)+" index is ",i)
                   skill_list[i] = skills
                   break
                # Increment counter.
                i+=1
            print(skills)
    print(skill_list)
    df["Skills"] = skill_list
    #n = (df.columns[1])
    #df.drop(n, axis = 1, inplace = True)
    df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
    print("Printing after the unnamed part ", df.head())
    # Print the output.
    df.to_csv("Student_Skill_Status.csv")
    
############ASEE-SE###########

# Prior to the spreadsheet.
# Specify path
path = "Student_Skill_Status_ASEE-SE.csv"
   
# Now check whether the specified path exists or not.
isExist = os.path.exists(path)
print("the file: ", isExist)

if not isExist:
    # Making spreadsheet.
      
    # Make a list of 100 cells.
    empty_percentage_list = [0 for x in range(100)]
    empty_skill_list = ['' for x in range(100)]
    
    list_for_thecsv = acheived_skills + empty_percentage_list
    list_for_thecsv_two = oprotunity + empty_percentage_list
    for i in range(len(list_for_thecsv)):
        print(list_for_thecsv[i], list_for_thecsv[i])
        if list_for_thecsv_two[i] > 0:
            list_for_thecsv[i] = str(round(((list_for_thecsv[i]/list_for_thecsv_two[i]) * 100), 2)) + "%"
        else:
            print("the else statement: ", list_for_thecsv[i], list_for_thecsv_two[i])
            list_for_thecsv[i] = ""
        #percentskills[i] = (percentskills[i]/Sum) * 100

    # Assign data of lists.
    data = {'Skills': skillsGUI + empty_skill_list, json_quiz_name_data['title']: list_for_thecsv}
      
    # Create DataFrame
    spreadsheet = pd.DataFrame(data)
      
    # Print the output.
    spreadsheet.to_csv("Student_Skill_Status_ASEE-SE.csv")

else:
    # creating a data frame
    #skillsGUI.append("yo")
    df = pd.read_csv("Student_Skill_Status_ASEE-SE.csv")
    print(df.head())
    skill_list = df["Skills"].values.tolist()
    print(skill_list)
    newpercents = len(skill_list) * ['']
    print("new percents ", newpercents)
    thecounter = 0
    for i in skillsGUI:
        if oprotunity[thecounter] > 0:
            newpercents[skill_list.index(i)] = str(round(((acheived_skills[thecounter]/oprotunity[thecounter]) * 100), 2)) + "%"
        else:
            newpercents[skill_list.index(i)] = ""
        thecounter +=1
    df[json_quiz_name_data['title']+"new"] = newpercents
    for skills in skillsGUI:
        if skills not in skill_list:
            #skill_list[skill_list.index('')] = skills
            i = 0
            for j in skill_list:
                if(pd.isnull(j)):
                   print(str(j)+" index is ",i)
                   skill_list[i] = skills
                   break
                # Increment counter.
                i+=1
            print(skills)
    print(skill_list)
    df["Skills"] = skill_list
    #n = (df.columns[1])
    #df.drop(n, axis = 1, inplace = True)
    df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
    print("Printing after the unnamed part ", df.head())
    # Print the output.
    df.to_csv("Student_Skill_Status_ASEE-SE.csv")

skill_binary = []
sum_binary = []
for skill in skill_list:
    ids = []
    values = []
    if str(skill) != 'nan':
        for student in student_skills:
            ids.append(student[0])
            input_string = str(student[3]).replace("'", "")
            for student_skill in input_string[1:-1].split(', '):
                print("skill: ", skill, student[0],  student_skill)
                if skill == student_skill:
                    values.append(1)
                    break
            if len(ids) > len(values):
                values.append(0)
        print(skill)
        print("ids: ", ids)
        print("values: ",values)
        the_sum = the_binary.main(str(skill),str(json_quiz_name_data['title'])[:13], ids, ids, values)
        print("the_binary", the_sum)
        skill_binary.append(skill)
        sum_binary.append(the_sum)
        #print(student_skills)
#the_sum = the_binary.main("test_skill",str(json_quiz_name_data['title'])[:13], [1,2,3,4,5,7,8,10], [1,2,3,5,7,8,10], [1,1,1,0,1,0,1])
#print("the_binary", the_sum)

# Prior to the spreadsheet.
# Specify path
path = "Student_Skill_Status_ASEE-SE_binary.csv"
   
# Now check whether the specified path exists or not.
isExist = os.path.exists(path)
print("the file: ", isExist)

if not isExist:
    # Making spreadsheet.
      
    # Make a list of 100 cells.
    empty_percentage_list = [0 for x in range(100)]
    empty_skill_list = ['' for x in range(100)]
    
    # Assign data of lists.
    data = {'Skills': skill_binary + empty_skill_list, json_quiz_name_data['title']: sum_binary + empty_percentage_list}
      
    # Create DataFrame
    spreadsheet = pd.DataFrame(data)
      
    # Print the output.
    spreadsheet.to_csv("Student_Skill_Status_ASEE-SE_binary.csv")

else:
    # creating a data frame
    #skillsGUI.append("yo")
    df = pd.read_csv("Student_Skill_Status_ASEE-SE_binary.csv")
    print(df.head())
    skill_list = df["Skills"].values.tolist()
    print(skill_list)
    newpercents = len(skill_list) * ['']
    print("new percents ", newpercents)
    thecounter = 0
    for i in skillsGUI:
        newpercents[skill_list.index(i)] = str(sum_binary[thecounter])
        thecounter +=1
    df[json_quiz_name_data['title']+"new"] = newpercents
    for skills in skill_binary:
        if skills not in skill_list:
            #skill_list[skill_list.index('')] = skills
            i = 0
            for j in skill_list:
                if(pd.isnull(j)):
                   print(str(j)+" index is ",i)
                   skill_list[i] = skills
                   break
                # Increment counter.
                i+=1
            print(skills)
    print(skill_list)
    df["Skills"] = skill_list
    #n = (df.columns[1])
    #df.drop(n, axis = 1, inplace = True)
    df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
    print("Printing after the unnamed part ", df.head())
    # Print the output.
    df.to_csv("Student_Skill_Status_ASEE-SE_binary.csv")
'''import easygui

easygui.msgbox("The Overall Class Performance is in the file:\nStudent_Skill_Status.csv", title="SkillAssigner", width_ = 480, height_ = 320)
import pymsgbox
pymsgbox.alert("The Overall Class Performance is in the file:\nStudent_Skill_Status.csv", "SkillAssigner Message")
#response = pymsgbox.prompt('What is your name?')
'''

# Making a pie chart.

while True:
    try:
        thecell = percentskills.index(0)
        percentskills.pop(thecell)
        skillsGUI.pop(thecell)
    except ValueError:
        break

fig, ax = plt.subplots(figsize=(8, 3), subplot_kw=dict(aspect="equal"))

# List of the notable.
topskill = [skillsGUI[percentskills.index(max(percentskills))]]
leastskill = [skillsGUI[percentskills.index(min(percentskills))]]

print("The new GUI values: ", skillsGUI, percentskills)
# Make the Pie chart.
#plt.text(-.05, 1.3, 'The most obtained skill is:\n'+notableSkills[0], fontsize = 13, horizontalalignment = 'center',bbox = dict(facecolor = 'gold', alpha = 0.5))
#plt.text(-.05, 1, 'The least obtained skill is:\n'+notableSkills[1], fontsize = 13, horizontalalignment = 'center',bbox = dict(facecolor = 'gold', alpha = 0.5))
wedges, texts, autotexts = plt.pie(percentskills, labels = skillsGUI, autopct='%1.1f%%')

topcolor = [wedges[percentskills.index(max(percentskills))]]
leastcolor = [wedges[percentskills.index(min(percentskills))]]

legend1 = ax.legend(topcolor,topskill,
          title="The highest skill gotten",
          loc="best",
          bbox_to_anchor=(1.3,1))
legend2 =ax.legend(leastcolor,leastskill,
          title="The lowest skill gotten",
          loc="best",
          bbox_to_anchor=(1.3,0.8))
ax.add_artist(legend1)
ax.add_artist(legend2)
          
plt.savefig(json_quiz_name_data['title']+'.png')
plt.title(json_quiz_name_data['title'])
plt.show()

## Generate a quiz_stat.csv file with the dataframe created
#quiz_stat.to_csv('quiz_stat_new.csv')


'''
###############Printing a the csv to view initially###########
from tkinter import *
from tkmagicgrid import *
import io
import csv

# Create a root window
root = Tk()

# Create a MagicGrid widget
grid = MagicGrid(root)
grid.pack(side="top", expand=1, fill="both")

# Display the contents of some CSV file
# (note this is not a particularly efficient viewer)
with io.open("test.csv", "r", newline="") as csv_file:
    reader = csv.reader(csv_file)
    parsed_rows = 0
    for row in reader:
        if parsed_rows == 0:
            # Display the first row as a header
            grid.add_header(*row)
        else:
            grid.add_row(*row)
        parsed_rows += 1

# Start Tk's event loop
root.mainloop()
pdb.set_trace()
'''
# API paggination: https://community.canvaslms.com/t5/Canvas-Developers-Group/Canvas-cURL-pagination-doesn-t-include-quot-last-quot-page-link/m-p/234685
