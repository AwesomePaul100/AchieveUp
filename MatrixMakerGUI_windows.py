# Paul Amoruso
# Instructor: Dr. DeMara
# The following script creates a skils matrix so that an instructure
# is able to assosiate certain skills with certian questions.
#authorisation test
# Generative approach.
import requests
import json
import pdb
import pandas as pd
import csv
import re
import os
#import python_client_tagging
import time
import python_client_tagging

#print("python_client", python_client.main("hey"))

from pprint import pprint   # pretty-print

print("\nmatrixmaker")

# A boolean value to identify if the title is too long for Windows.
title_length = False

# Server status
server_status = True

# This function reads cells from the questions.csv file (questions_tagged_with_skills).
def read_cell(x, y):
    with open('questions.csv', 'r') as f:
        reader = csv.reader(f)
        y_count = 0
        for n in reader:
            if y_count == y:
                cell = n[x]
                return cell
            y_count += 1

## To Flatten the JSON
from flatten_json import flatten

skills = []
server_ip = ''
# Now dynamically add the skills via JSON file.

# Opening JSON file
f = open('data.json')

# returns JSON object as a dictionary
data = json.load(f)

# Iterating through the json list
#for i in data['options']:
#    print(i)
#    skills. append(i)

# Send API request to retrive the data from Canvas
headers ={'Authorization':'Bearer '+data['token'][0]}

server_ip = data['ip'][0]
print("server IP is: ", server_ip)

########### Url to extract Quiz questions details
url = 'https://webcourses.ucf.edu/api/v1/courses/1158000000'+ data['url'][0] +'/quizzes/1158000000'+ data['url'][1]
########### Url to extract course questions details
url_name = 'https://webcourses.ucf.edu/api/v1/courses/1158000000'+ data['url'][0]

# Closing file
f.close()


# Let us get the title of the assignment first.
url_quiz_name = url
r_quiz_name = requests.get(url_quiz_name,headers = headers)
print(r_quiz_name.status_code)
if r_quiz_name.status_code != 200:
    print("\nPlease check the token\n")
json_quiz_name_data = json.loads(r_quiz_name.text)

# Let us get the title of course.
r_course_name = requests.get(url_name,headers = headers)
print(r_course_name.status_code)
if r_course_name.status_code != 200:
    print("\nPlease check the token\n")
json_course_name_data = json.loads(r_course_name.text)

# The title.
title_course = json_course_name_data['name']
print("\nThe course name: ",json_course_name_data['name'])
title_course = title_course.replace(' ', '_')

# The title.
title = json_quiz_name_data['title']
print(json_quiz_name_data['title'])
if len(title) > 50:
    title_length = True

url_quiz_ques = url + '/questions/?per_page=150'
r_quiz_ques_1 = requests.get(url_quiz_ques,headers = headers)
print(r_quiz_ques_1.status_code)
json_data = json.loads(r_quiz_ques_1.text)

# Get second page of the data.
url_quiz_ques = url + '/questions/?page=2&per_page=150'
r_quiz_ques_2 = requests.get(url_quiz_ques,headers = headers)
print("Is the pages the same??: ",r_quiz_ques_1 == r_quiz_ques_2)
print(r_quiz_ques_2.status_code)
json_data = json_data + json.loads(r_quiz_ques_2.text)

#print(json_data)
# Python dictionary to house the points of the students.
ids = {}

df1 = []
df2 = []

question_counter = 0
question_spreadsheet = []

# Read the data from the JSON data
for data in json_data:
    ans_data = data['answers']
    # Create a dataframe and put the parsed data into it
    df = pd.DataFrame(ans_data)

    # Renaming the features so that they are easily readable
    df = df.rename({'weight':'answers_weight'},axis = 1)
    
    # Get rid of the html, comments and comments_html features from the dataframe
    #df = df.drop(['id','text'],axis = 1)
    question_counter += 1
    open_bracket = False
    letter_T= False
    last_bracket = False
    letter = ''
    # Make a sting for all the partial credits.
    string = ""
    
    # Just to see if there was a partial credit question.
    partial_question = False
    
    # If there is a reference sheet, just skip over it.
    if str(data['question_name']) == "Reference Sheet":
        continue
    if str(data['question_type']) == "matching_question":
        continue
    # This is string that is gotten with all partial credits.
    the_full_question = str(data['question_text'])
    print("\nQuestion " + str(question_counter)+ " is: " + str(data['question_text']) + "\n")
    for element in the_full_question:
        string = string + element
        if element == '[':
            open_bracket = True
            print("The first statment")
            #print(string)
            continue
        if element == 'a' and open_bracket == True or element == 'b' and open_bracket == True or element == 'c' and open_bracket == True:
            letter_T = True
            letter = element
            print("The letter")
            #print(string)
            continue
        elif element == ']' and letter_T and open_bracket:
            last_bracket = True
            if data['id'] == 132732719:
                print(string)
            question_spreadsheet.append([str(data['id']) + letter, string, '', '', '', '', ''])
            question_counter += 1
            # Set the string back to capture the following partial credit questions.
            string = ""
            #print("####################")
            open_bracket = False
            letter_T= False
            last_bracket = False
            # Set the letter back to check for more.
            letter = ''
            # Make note that there was a parital credit question.
            partial_question = True
        else:
            open_bracket = False
            letter_T = False
            
    # If it gets to this statement and partial_question is still set to false, then it is not a partian credit question.
    if partial_question == False:
        question_spreadsheet.append([str(data['id']) + letter, the_full_question, '', '', '', '', ''])
    else:
        partial_question = False

    
#print("question counter = ", question_counter)
## Add the questions and then the asnwers in one dataframe
#quiz_questions = pd.concat([df_ques,df], axis = 1, sort = False)

# The following line makes a dataframe with the columns for skills.
spreadsheet = pd.DataFrame(question_spreadsheet, columns = ['Ids', 'Question', 'Skill 1', 'Skill 2', 'Skill 3', 'Skill 4', 'Skill 5'])

# This outputs the csv file so that it is ready for an instructure to tag skills to the questions.

if title_length:
    spreadsheet.to_csv(title[:50] + '_'+'questions.csv')
else:
    spreadsheet.to_csv(title + '_'+'questions.csv')

i = 0

questions = []

while i < len(question_spreadsheet):
    if title_length:
        cells = pd.read_csv(title[:50] + '_' + "questions.csv")
    else:
        cells = pd.read_csv(title + '_' + "questions.csv")
    string = cells.loc[i, 'Question']
    #print("-----------------\n",string)
    newstring = re.sub('<[^>]+>', '', string)
    newstring = newstring.replace('&nbsp;', '')
    questions.append(newstring)
    newstring.strip('^\r\n')
    cells.loc[i, 'Question'] = newstring
    #print("hey")
    if title_length:
        cells.to_csv(title[:50] + '_' + "questions.csv", index=False)
    else:
        cells.to_csv(title + '_' + "questions.csv", index=False)
    i+=1
# writing into the file
if title_length:
    cells.to_csv(title[:50] + '_' + "questions.csv", index=False)
else:
    cells.to_csv(title + '_' + "questions.csv", index=False)
 
#time.sleep(3)
# API call to make the suggested skills list.
import concurrent.futures
# Set the number of workers (threads or processes)
num_workers = 8

import csv

skills_list = []

# Open the CSV file for reading
with open(title_course+'_generated_skills.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    # Initialize an empty list to store the results
    #result_list = []

    # Iterate over each row in the CSV file
    for row in reader:
        original_value = row['Generative_AI_suggested_skill_list']
        replaced_value = row['Instructor_refined_skill_list']

        # Check if the "replaced_values" column is not empty
        if replaced_value.strip() != "":
            # If it's not empty, add the value from that column to the result list
            skills_list.append(replaced_value)
        else:
            # If it's empty, add the original value to the result list
            skills_list.append(original_value)

    # Print the resulting list
    print(skills_list)
'''
skills_list += [""] * (17 - len(skills_list))  # add empty strings to fill up to 17

skills_list = skills_list[:17]  # trim the list to 17 indexes, or less if it's already shorter

print(skills_list)
'''
import socket
import tkinter as tk
from tkinter import messagebox

def check_server_status(server_ip):
  """Checks if a server is online."""
  try:
    # Attempt to connect to the server on port 8000
    socket.create_connection((server_ip, 8000), 2)
    return True
  except socket.error:
    return False

def show_offline_message(server_ip):
  """Displays a popup message if the server is offline."""
  messagebox.showerror("Server Status", f"{server_ip} is offline. Please contact support. \n\n paul.amoruso@ucf.edu")

# Get the server IP address from the user (or hardcode it)
#server_ip = '192.168.168.103'
#server_ip = '10.173.214.164'
    
suggested_skills = []
# Check the server status
if check_server_status(server_ip):
  print(f"{server_ip} is online.")
  from tkinter import ttk
  root = tk.Tk()
  root.title("Processing...")
  root.geometry("300x100")  # Set width to 500 pixels, height to 300 pixels.
  root.resizable(True, True)  # Allow resizing in both directions.
  progress_bar = ttk.Progressbar(root, orient="horizontal", length=300,mode="determinate")
  progress_bar.pack(pady=20)
  
  # Add a label to display the status message
  status_label = ttk.Label(root, text="Retrieving data from AI database...", font=("Helvetica", 13))
  status_label.pack()
  root.update()
  
  time.sleep(1)
  start_time = time.time()
  from concurrent.futures import ThreadPoolExecutor
  loop_counter = 0
  with ThreadPoolExecutor(max_workers=10) as executor:
    for q in questions:
        sublist = []
        loop_counter = loop_counter + 1
        print("asking the questions:...")
        #executor.submit(qskills = (python_client_tagging.main(q.replace(' ','_'), str(title_course), result_list)).split(","))
        qskills = (python_client_tagging.main(q.replace(' ','_'), str(title_course), skills_list)).split(",")
        sublist = [qskill.strip() for qskill in qskills]  # Create a sublist, removing extra spaces.
        suggested_skills.append(sublist)
        #print(python_client_tagging.main(q.replace(' ','_'), str(title_course), result_list))
        if (loop_counter % 2) == 0:
            status_label.config(text=f"Processing question {loop_counter} of {len(questions)}")
            progress_bar['value'] = (loop_counter / len(questions)) * 100
            print(loop_counter)
            root.update() # Update the GUI to reflect the progress bar
  end_time = time.time()
  elapsed_time = end_time - start_time
  print(f"The for loop took {elapsed_time:.4f} seconds to execute.")
  root.destroy()
  print(suggested_skills)
  # Make the list with the suggesteded and questions.
  suggested_df = pd.DataFrame({'Column1': questions, 'Column2': suggested_skills})
  print("the list: ",suggested_df)
  suggested_df.to_csv(str(title_course)+'suggested_values.csv', index=False)
else:
  show_offline_message(server_ip)
  server_status = False
  
print("server_status: ",server_status)
#exit()
 
target_size = 17

suggested_skills = suggested_skills + [[""] * 3 for _ in range(target_size - len(suggested_skills))]

print(suggested_skills)

'''try:
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        suggested_skills = list(executor.map(lambda q: python_client_tagging.main(q.replace(' ','_'), str(title_course), result_list), questions[:5]))
except Exception as e:
    # handle exception here
    print(f"Error occurred: {e}")
'''

#suggested_skills = [python_client_tagging.main(q.replace(' ','_'), str(title_course), result_list) for q in questions]

#time.sleep(15)

print(cells)

print("The title: ", title)
#exit()

##########################################################
# Paul Amoruso
# EIN6258 Project
# Suggestion process also trying to implement.

# Imports
from tkinter import *

# import messagebox as mb from tkinter
from tkinter import messagebox as mb

print("This is prior to GUI")


#questions = ["A processor on an airplane receives data from 16 different modules. Every module has 2 sensors each of which generate 16 KB/sec. The airplane’s flight duration is 16 hours.Partial Credit 1: What is the aggregate data rate per second from all sensors? a) 16 KB/s b) 32 KB/s c) 64 KB/s d) 0.5 MB/s e) 1 MB/s f) 16 MB/s g) none of the choices listedAnswer 1: [a]", "(Note: Indicate ONLY the LETTER corresponding to your choice)Partial Credit 2: What is the leaststorage capacity listed below that is sufficientto recordthe duration of a single flight?  a) 16GB b) 32GB c) 64GB d) 128GB e) 132 GB f) 144 GB g) 164 GB h) 184 GBAnswer 2: [b]","A mobile phoneprocessor  accesses 4 Bytes from memory during a single Write operation.Partial Credit 1: How many wires comprise the data bus? a) 2 b) 4 c) 8 d) 16 e) 32 f) 64 g) insufficient information to determine h) none of the choices listedAnswer 1: [a]"]

print("The skills array length: ", len(skills))


questioncounter = 0

print("The title prior to GUI: ", title)

master = Tk()

titlecsv = title

# Setting colors.
master.configure(bg='#000011')

print(questioncounter)

# set the title of the Window
master.title("Matrix Maker")

# The title to be shown
title = Label(master, text="Matrix Maker", width=50, bg="#b7a369",fg="white", font=("ariel", 20, "bold"))

# place of the title
title.grid(row = 1, columnspan=6)

window_width = master.winfo_width() #get current screen width
wrapLen = 2000/3

q = questions[questioncounter].strip()
q = os.linesep.join([s for s in q.splitlines() if s])
print(q.replace(' ','_'), '\n')
#print(python_client.main(q.replace(' ','_')))

print("Question size: ", len(q))
if len(q) > 200:
    print("large")
    label = Label(master, text=q.strip(), wraplength = wrapLen, font=("ariel",12, "bold"), bg='#000011', fg = '#FFFFFF')
else:
    label = Label(master, text=q.strip(), wraplength = wrapLen, font=("ariel",15," bold"), bg='#000011', fg = '#FFFFFF')
label.grid(row = 2, columnspan=6)
questioncounter = 1 + questioncounter
questionNumber = Label(master, text=str(questioncounter)+" out of "+ str(len(questions))+ " questions", wraplength = wrapLen, font=("time new roman",13), bg='#000011', fg = '#FFFFFF')
questionNumber.grid(row = 18, columnspan=6)
        
var1 = IntVar()
var2 = IntVar()
var3 = IntVar()
var4 = IntVar()
var5 = IntVar()
var6 = IntVar()
var7 = IntVar()
var8 = IntVar()
var9 = IntVar()
var10 = IntVar()
var11 = IntVar()
var12 = IntVar()
var13 = IntVar()
var14 = IntVar()
var15 = IntVar()
var16 = IntVar()
var17 = IntVar()


checkbutton = None
checkbutton2 = None
checkbutton3 = None
checkbutton4 = None
checkbutton5 = None
checkbutton6 = None
checkbutton7 = None
checkbutton8 = None
checkbutton9 = None
checkbutton10 = None
checkbutton11 = None
checkbutton12 = None
checkbutton13 = None
checkbutton14 = None
checkbutton15 = None
checkbutton16 = None
checkbutton17 = None


if len(skills_list) >= 1:
    checkbutton = Checkbutton(master, text=skills_list[0], variable=var1, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='yellow',selectcolor="black")
    checkbutton.grid(row=3, column = 2, sticky=W)
if len(skills_list) >=2:
    checkbutton2 = Checkbutton(master, text=skills_list[1], variable=var2, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='yellow',selectcolor="black")
    checkbutton2.grid(row=4, column = 2, sticky=W)
    
if len(skills_list) >= 3:
    checkbutton3 = Checkbutton(master, text=skills_list[2], variable=var3, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black")
    checkbutton3.grid(row=5, column = 2,sticky=W)
    
if len(skills_list) >= 4:
    checkbutton4 = Checkbutton(master, text=skills_list[3], variable=var4, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black")
    checkbutton4.grid(row=6, column = 2, sticky=W)
    
if len(skills_list) >= 5:
    checkbutton5 = Checkbutton(master, text=skills_list[4], variable=var5, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black")
    checkbutton5.grid(row=7, column = 2,sticky=W)
    
if len(skills_list) >= 6:
    checkbutton6 = Checkbutton(master, text=skills_list[5], variable=var6, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black")
    checkbutton6.grid(row=8, column = 2, sticky=W)
    
if len(skills_list) >= 7:
    checkbutton7 = Checkbutton(master, text=skills_list[6], variable=var7, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black")
    checkbutton7.grid(row=3, column = 3,sticky=W)
    
if len(skills_list) >= 8:
    checkbutton8 = Checkbutton(master, text=skills_list[7], variable=var8, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black")
    checkbutton8.grid(row=4, column = 3, sticky=W)
    
if len(skills_list) >= 9:
    checkbutton9 = Checkbutton(master, text=skills_list[8], variable=var9, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black")
    checkbutton9.grid(row=5, column = 3,sticky=W)
    
if len(skills_list) >= 10:
    checkbutton10 = Checkbutton(master, text=skills_list[9], variable=var10, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black")
    checkbutton10.grid(row=6, column = 3, sticky=W)
    
if len(skills_list) >= 11:
    checkbutton11 = Checkbutton(master, text=skills_list[10], variable=var11, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black")
    checkbutton11.grid(row=7, column = 3,sticky=W)
    
if len(skills_list) >= 12:
    checkbutton12 = Checkbutton(master, text=skills_list[11], variable=var12, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black")
    checkbutton12.grid(row=8, column = 3, sticky=W)
    
if len(skills_list) >= 13:
    checkbutton13 = Checkbutton(master, text=skills_list[12], variable=var13, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black")
    checkbutton13.grid(row=3, column = 4,sticky=W)
    
if len(skills_list) >= 14:
    checkbutton14 = Checkbutton(master, text=skills_list[13], variable=var14, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black")
    checkbutton14.grid(row=4, column = 4, sticky=W)
    
if len(skills_list) >= 15:
    checkbutton15 = Checkbutton(master, text=skills_list[14], variable=var15, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black")
    checkbutton15.grid(row=5, column = 4,sticky=W)
    
if len(skills_list) >= 16:
    checkbutton16 = Checkbutton(master, text=skills_list[15], variable=var16, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black")
    checkbutton16.grid(row=6, column = 4, sticky=W)
    
if len(skills_list) >= 17:
    checkbutton17 = Checkbutton(master, text=skills_list[16], variable=var17, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black")
    checkbutton17.grid(row=7, column = 4, sticky=W)

if server_status:
    # The first question
    if checkbutton and (skills_list[0] in suggested_skills[questioncounter - 1]):  # Check if the checkbutton was created successfully
        print("the checkbutton")
        master.after(0, lambda: checkbutton.select())  # Schedule the selection
        # Automatically select the checkbutton.
    if checkbutton2 and (skills_list[1] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
        print(skills_list[1]," a match!")
        master.after(0, lambda: checkbutton2.select())  # Schedule the selection
    if checkbutton3 and (skills_list[2] in suggested_skills[questioncounter-1]):  # Check if the checkbutton was created successfully
        print(skills_list[2]," a match!")
        master.after(0, lambda: checkbutton3.select())  # Schedule the selection
    if checkbutton4 and (skills_list[3] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
        master.after(0, lambda: checkbutton4.select())  # Schedule the selection
    if checkbutton5 and (skills_list[4] in suggested_skills[questioncounter - 1]):  # Check if the checkbutton was created successfully
        master.after(0, lambda: checkbutton5.select())  # Schedule the selection
    if checkbutton6 and (skills_list[5] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
        master.after(0, lambda: checkbutton6.select())  # Schedule the selection
    if checkbutton7 and (skills_list[6] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
        master.after(0, lambda: checkbutton7.select())  # Schedule the selection
    if checkbutton8 and (skills_list[7] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
        master.after(0, lambda: checkbutton8.select())  # Schedule the selection
    if checkbutton9 and (skills_list[8] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
        master.after(0, lambda: checkbutton9.select())  # Schedule the selection
    if checkbutton10 and (skills_list[9] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
        master.after(0, lambda: checkbutton10.select())  # Schedule the selection
    if checkbutton11 and (skills_list[10] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
        master.after(0, lambda: checkbutton11.select())  # Schedule the selection
    if checkbutton12 and (skills_list[11] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
        master.after(0, lambda: checkbutton12.select())  # Schedule the selection
    if checkbutton13 and (skills_list[12] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
        master.after(0, lambda: checkbutton13.select())  # Schedule the selection
    if checkbutton14 and (skills_list[13] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
        master.after(0, lambda: checkbutton14.select())  # Schedule the selection
    if checkbutton15 and (skills_list[14] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
        master.after(0, lambda: checkbutton15.select())  # Schedule the selection
    if checkbutton16 and (skills_list[15] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
        master.after(0, lambda: checkbutton16.select())  # Schedule the selection
    if checkbutton17 and (skills_list[16] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
        master.after(0, lambda: checkbutton17.select())  # Schedule the selection

Button(master, highlightbackground='#000011', text='Quit', command=master.quit).grid(row=15,column = 2, sticky="", pady=5)

if title_length:
    thecsv = titlecsv[:50] + '_' + "questions.csv"
else:
    thecsv = titlecsv + '_' + "questions.csv"
cells = pd.read_csv(thecsv)
print(cells)

def toggle_var(var):
    if var.get() == 1:
        var.set(0)
    else:
        var.set(1)

def var_states():
    global questioncounter
    global label
    global questionNumber
    #print("male: %d,\nfemale: %d" % (var1.get(), var2.get()))
    #var1.set(0)
    #var2.set(0)
    print("\nQuestioncounter value: ",questioncounter)
    label.config(text="" , bg='#000011')
    questionNumber.config(text="", bg='#000011')
    
    skillcounter = 1
    i = 0
    print("###############The title: ", thecsv)
    
    
    if len(questions) > questioncounter:
        q = questions[questioncounter].strip()
        q = os.linesep.join([s for s in q.splitlines() if s])
        print ("\nQuestion size: ", len(q))
        #print('\nquestion:',questioncounter+1, python_client.main(q.replace(' ','_')))
        if len(q) > 700:
            #repr(q)
            q = q.replace('\n', ' ').replace('\r', ' ')
            #print("\nafter strip command lol: ",q)
            label = Label(master, text=q, wraplength = wrapLen, font=("ariel",10, "bold"), bg='#000011', fg = '#FFFFFF')
        if len(q) > 300:
            repr(q)
            q = q.replace('\n', '   ').replace('\r', '\n')
            #print("\nafter strip command lol: ",q)
            label = Label(master, text=q, wraplength = wrapLen, font=("ariel",12, "bold"), bg='#000011', fg = '#FFFFFF')
        else:
            label = Label(master, text=q, wraplength = wrapLen, font=("ariel",15,"bold"), bg='#000011', fg = '#FFFFFF')
        label.grid(row = 2, columnspan=6)
        questionNumber =Label(master, text=str(questioncounter+1)+" out of "+ str(len(questions))+ " questions", wraplength = wrapLen, font=("time new roman",13), bg='#000011', fg = '#FFFFFF')
        questionNumber.grid(row = 18, columnspan=6)
        #for num in range(0,16):
           # print("\nNum value: ", num)
        #print("skill 0: ", skills_list[0], "suggested_skills:", suggested_skills[questioncounter - 1])
        #print("skill 1: ", skills_list[1], "suggested_skills:", suggested_skills[questioncounter -1])
        #print("skill 2: ", skills_list[2], "suggested_skills:", suggested_skills[questioncounter -1])
        if server_status:
            if checkbutton and (skills_list[0] in suggested_skills[questioncounter - 1]):  # Check if the checkbutton was created successfully
                print("the checkbutton")
                master.after(0, lambda: checkbutton.select())  # Schedule the selection.
                # Automatically select the checkbutton.
            if checkbutton2 and (skills_list[1] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
                print(skills_list[1]," a match!")
                master.after(0, lambda: checkbutton2.select())  # Schedule the selection
            if checkbutton3 and (skills_list[2] in suggested_skills[questioncounter-1]):  # Check if the checkbutton was created successfully
                print(skills_list[2]," a match!")
                master.after(0, lambda: checkbutton3.select())  # Schedule the selection
            if checkbutton4 and (skills_list[3] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
                master.after(0, lambda: checkbutton4.select())
            if checkbutton5 and (skills_list[4] in suggested_skills[questioncounter - 1]):  # Check if the checkbutton was created successfully
                master.after(0, lambda: checkbutton5.select())  # Schedule the selection
            if checkbutton6 and (skills_list[5] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
                master.after(0, lambda: checkbutton6.select())  # Schedule the selection
            if checkbutton7 and (skills_list[6] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
                master.after(0, lambda: checkbutton7.select())  # Schedule the selection
            if checkbutton8 and (skills_list[7] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
                master.after(0, lambda: checkbutton8.select())  # Schedule the selection
            if checkbutton9 and (skills_list[8] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
                master.after(0, lambda: checkbutton9.select())  # Schedule the selection
            if checkbutton10 and (skills_list[9] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
                master.after(0, lambda: checkbutton10.select())  # Schedule the selection
            if checkbutton11 and (skills_list[10] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
                master.after(0, lambda: checkbutton11.select())  # Schedule the selection
            if checkbutton12 and (skills_list[11] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
                master.after(0, lambda: checkbutton12.select())  # Schedule the selection
            if checkbutton13 and (skills_list[12] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
                master.after(0, lambda: checkbutton13.select())  # Schedule the selection
            if checkbutton14 and (skills_list[13] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
                master.after(0, lambda: checkbutton14.select())  # Schedule the selection
            if checkbutton15 and (skills_list[14] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
                master.after(0, lambda: checkbutton15.select())  # Schedule the selection
            if checkbutton16 and (skills_list[15] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
                master.after(0, lambda: checkbutton16.select())  # Schedule the selection
            if checkbutton17 and (skills_list[16] in suggested_skills[questioncounter -1]):  # Check if the checkbutton was created successfully
                master.after(0, lambda: checkbutton17.select())  # Schedule the selection
        
        print("checking var1 status: ", var1.get())
        
        if checkbutton.cget("state") == "selected":
            print("Checkbutton is selected!")
        else:
            print("Checkbutton is not selected.")
        if var1.get() == 1 and skillcounter <=5 :
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[0]
            skillcounter = skillcounter + 1
            var1.set(0)
            checkbutton.deselect()  # Uncheck the button.
            cells.to_csv(thecsv, index=False)
            print("question counter: ", questioncounter, "got skill 1")
        if var2.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[1]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 2")
            var2.set(0)
            checkbutton2.deselect()  # Uncheck the button
            cells.to_csv(thecsv, index=False)
        if var3.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[2]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 3")
            var3.set(0)
            checkbutton3.deselect()  # Uncheck the button
            cells.to_csv(thecsv, index=False)
        if var4.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[3]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 4")
            var4.set(0)
            checkbutton4.deselect()  # Uncheck the button
            cells.to_csv(thecsv, index=False)
        if var5.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[4]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 5")
            var5.set(0)
            checkbutton5.deselect()  # Uncheck the button
            cells.to_csv(thecsv, index=False)
        if var6.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[5]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 6")
            var6.set(0)
            checkbutton6.deselect()  # Uncheck the button
        if var7.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[6]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 7")
            var7.set(0)
            checkbutton7.deselect()  # Uncheck the button
        if var8.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[7]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 8")
            var8.set(0)
            checkbutton8.deselect()  # Uncheck the button
        if var9.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[8]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 9")
            var9.set(0)
            checkbutton9.deselect()  # Uncheck the button
        if var10.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[9]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 10")
            var10.set(0)
            checkbutton10.deselect()  # Uncheck the button
        if var11.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[10]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 11")
            var11.set(0)
            checkbutton11.deselect()  # Uncheck the button
        if var12.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[11]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 12")
            var12.set(0)
            checkbutton12.deselect()  # Uncheck the button
        if var13.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[12]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 13")
            var13.set(0)
            checkbutton13.deselect()  # Uncheck the button
        if var14.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[13]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 13")
            var14.set(0)
            checkbutton14.deselect()  # Uncheck the button
        if var15.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[14]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 14")
            var15.set(0)
            checkbutton15.deselect()  # Uncheck the button
        if var16.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[15]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 15")
            var16.set(0)
            checkbutton16.deselect()  # Uncheck the button
        if var17.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[16]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 16")
            var17.set(0)
            checkbutton17.deselect()  # Uncheck the button
        if skillcounter > 6:
            print("skills selcted are: ",skillcounter)
            mb.showinfo("Result", "Maximum # of skills is 5!")
        
        questioncounter = 1 + questioncounter
        
    else:
        print(cells)
        # Shows a message box to display the result
        mb.showinfo("Result", "End of questions!")
        #print("Writing to the file")
        if var1.get() == 1 and skillcounter <=5 :
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[0]
            skillcounter = skillcounter + 1
            var1.set(0)
            checkbutton.deselect()  # Uncheck the button.
            cells.to_csv(thecsv, index=False)
        if var2.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[1]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 2")
            var2.set(0)
            checkbutton2.deselect()  # Uncheck the button.
            cells.to_csv(thecsv, index=False)
        if var3.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[2]
            skillcounter = skillcounter + 1
            var3.set(0)
            checkbutton3.deselect()  # Uncheck the button.
            cells.to_csv(thecsv, index=False)
        if var4.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[3]
            skillcounter = skillcounter + 1
            var4.set(0)
            checkbutton4.deselect()  # Uncheck the button.
            cells.to_csv(thecsv, index=False)
        if var5.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[4]
            skillcounter = skillcounter + 1
            var5.set(0)
            checkbutton5.deselect()  # Uncheck the button.
            cells.to_csv(thecsv, index=False)
        if var6.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[5]
            skillcounter = skillcounter + 1
            var6.set(0)
            checkbutton6.deselect()  # Uncheck the button.
        if var7.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[6]
            skillcounter = skillcounter + 1
            var7.set(0)
            checkbutton7.deselect()  # Uncheck the button.
        if var8.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[7]
            skillcounter = skillcounter + 1
            var8.set(0)
            checkbutton8.deselect()  # Uncheck the button.
        if var9.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[8]
            skillcounter = skillcounter + 1
            var9.set(0)
            checkbutton9.deselect()  # Uncheck the button.
        if var10.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[9]
            skillcounter = skillcounter + 1
            var10.set(0)
            checkbutton10.deselect()  # Uncheck the button.
        if var11.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[10]
            skillcounter = skillcounter + 1
            var11.set(0)
            checkbutton11.deselect()  # Uncheck the button.
        if var12.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[11]
            skillcounter = skillcounter + 1
            var12.set(0)
            checkbutton12.deselect()  # Uncheck the button.
        if var13.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[12]
            skillcounter = skillcounter + 1
            var13.set(0)
            checkbutton13.deselect()  # Uncheck the button.
        if var14.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[13]
            skillcounter = skillcounter + 1
            var14.set(0)
            checkbutton14.deselect()  # Uncheck the button.
        if var15.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[14]
            skillcounter = skillcounter + 1
            var15.set(0)
            checkbutton15.deselect()  # Uncheck the button.
        if var16.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[15]
            skillcounter = skillcounter + 1
            var16.set(0)
            checkbutton16.deselect()  # Uncheck the button.
        if var17.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills_list[16]
            skillcounter = skillcounter + 1
            var17.set(0)
            checkbutton17.deselect()  # Uncheck the button.
        if skillcounter > 6:
            print("skills selcted are: ",skillcounter)
            mb.showinfo("Result", "Maximum # of skills is 5!")
        #exit()

Button(master, text='Next', command=var_states, highlightbackground='#000011').grid(row=15, column = 4, sticky="", pady=5)

master.mainloop()

if questioncounter > 2:
    print("Writing to the file")
    print(cells)
    cells.to_csv(thecsv, index=False)
# writing into the file
#cells.to_csv(question_spreadsheet, index=False)
