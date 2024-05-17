# Paul Amoruso
# Instructor: Dr. DeMara
# The following script creates a skils matrix so that an instructure
# is able to assosiate certain skills with certian questions.
#authorisation test
import requests
import json
import pdb
import pandas as pd
import csv
import re
import os

from pprint import pprint   # pretty-print


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

# Now dynamically add the skills via JSON file.

# Opening JSON file
f = open('data.json')

# returns JSON object as a dictionary
data = json.load(f)

# Iterating through the json list
for i in data['options']:
    print(i)
    skills. append(i)

# Send API request to retrive the data from Canvas
headers ={'Authorization':'Bearer '+data['token'][0]}

########### Url to extract Quiz questions details
url = 'https://webcourses.ucf.edu/api/v1/courses/1158000000'+ data['url'][0] +'/quizzes/1158000000'+ data['url'][1]

# Closing file
f.close()


# Let us get the title of the assignment first.
url_quiz_name = url
r_quiz_name = requests.get(url_quiz_name,headers = headers)
print(r_quiz_name.status_code)
if r_quiz_name.status_code != 200:
    print("\nPlease check the token\n")
json_quiz_name_data = json.loads(r_quiz_name.text)

# The title.
title = json_quiz_name_data['title']
print(json_quiz_name_data['title'])

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
spreadsheet.to_csv(title + '_'+'questions.csv')

i = 0

questions = []

while i < len(question_spreadsheet):
    cells = pd.read_csv(title + '_' + "questions.csv")
    string = cells.loc[i, 'Question']
    #print("-----------------\n",string)
    newstring = re.sub('<[^>]+>', '', string)
    newstring = newstring.replace('&nbsp;', '')
    questions.append(newstring)
    newstring.strip('^\r\n')
    cells.loc[i, 'Question'] = newstring
    #print("hey")
    cells.to_csv(title + '_' + "questions.csv", index=False)
    i+=1
# writing into the file
cells.to_csv(title + '_' + "questions.csv", index=False)

print(cells)

print("The title: ", title)

##########################################################
# Paul Amoruso
# EIN6258 Project

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

print("Question size: ", len(q))
if len(q) > 100:
    label = Label(master, text=q, wraplength = wrapLen, font=("ariel",12," bold"), bg='#000011', fg = '#FFFFFF')
else:
    label = Label(master, text=q, wraplength = wrapLen, font=("ariel",15," bold"), bg='#000011', fg = '#FFFFFF')
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

if len(skills) >= 1:
    Checkbutton(master, text=skills[0], variable=var1, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='yellow',selectcolor="black").grid(row=3, column = 2,sticky=W)
if len(skills) >=2:
    Checkbutton(master, text=skills[1], variable=var2, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='yellow',selectcolor="black").grid(row=4, column = 2, sticky=W)
if len(skills) >= 3:
    Checkbutton(master, text=skills[2], variable=var3, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black").grid(row=5, column = 2,sticky=W)
if len(skills) >= 4:
    Checkbutton(master, text=skills[3], variable=var4, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black").grid(row=6, column = 2, sticky=W)
if len(skills) >= 5:
    Checkbutton(master, text=skills[4], variable=var5, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black").grid(row=7, column = 2,sticky=W)
if len(skills) >= 6:
    Checkbutton(master, text=skills[5], variable=var6, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black").grid(row=8, column = 2, sticky=W)

if len(skills) >= 7:
    Checkbutton(master, text=skills[6], variable=var7, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black").grid(row=3, column = 3,sticky=W)
if len(skills) >= 8:
    Checkbutton(master, text=skills[7], variable=var8, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black").grid(row=4, column = 3, sticky=W)
if len(skills) >= 9:
    Checkbutton(master, text=skills[8], variable=var9, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black").grid(row=5, column = 3,sticky=W)
if len(skills) >= 10:
    Checkbutton(master, text=skills[9], variable=var10, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black").grid(row=6, column = 3, sticky=W)
if len(skills) >= 11:
    Checkbutton(master, text=skills[10], variable=var11, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black").grid(row=7, column = 3,sticky=W)
if len(skills) >= 12:
    Checkbutton(master, text=skills[11], variable=var12, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black").grid(row=8, column = 3, sticky=W)

if len(skills) >= 13:
    Checkbutton(master, text=skills[12], variable=var13, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black").grid(row=3, column = 4,sticky=W)
if len(skills) >= 14:
    Checkbutton(master, text=skills[13], variable=var14, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black").grid(row=4, column = 4, sticky=W)
if len(skills) >= 15:
    Checkbutton(master, text=skills[14], variable=var15, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black").grid(row=5, column = 4,sticky=W)
if len(skills) >= 16:
    Checkbutton(master, text=skills[15], variable=var16, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black").grid(row=6, column = 4, sticky=W)
if len(skills) >= 17:
    Checkbutton(master, text=skills[16], variable=var17, bg='#000011', fg = '#FFFFFF', activebackground='black', activeforeground='white',selectcolor="black").grid(row=7, column = 4, sticky=W)


Button(master, highlightbackground='#000011', text='Quit', command=master.quit).grid(row=15,column = 3, sticky="", pady=5)

thecsv = titlecsv + '_' + "questions.csv"
cells = pd.read_csv(thecsv)
print(cells)

def var_states():
    global questioncounter
    global label
    global questionNumber
    print("male: %d,\nfemale: %d" % (var1.get(), var2.get()))
    #var1.set(0)
    #var2.set(0)
    print(questioncounter)
    label.config(text="" , bg='#000011')
    questionNumber.config(text="", bg='#000011')
    
    skillcounter = 1
    i = 0
    print("###############The title: ", thecsv)
    
    
    if len(questions) > questioncounter:
        q = questions[questioncounter].strip()
        q = os.linesep.join([s for s in q.splitlines() if s])
        print ("\nQuestion size: ", len(q))
        if len(q) > 100:
            label = Label(master, text=q, wraplength = wrapLen, font=("ariel",12," bold"), bg='#000011', fg = '#FFFFFF')
        else:
            label = Label(master, text=q, wraplength = wrapLen, font=("ariel",15," bold"), bg='#000011', fg = '#FFFFFF')
        label.grid(row = 2, columnspan=6)
        questionNumber =Label(master, text=str(questioncounter+1)+" out of "+ str(len(questions))+ " questions", wraplength = wrapLen, font=("time new roman",13), bg='#000011', fg = '#FFFFFF')
        questionNumber.grid(row = 18, columnspan=6)
        
        if var1.get() == 1 and skillcounter <=5 :
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[0]
            skillcounter = skillcounter + 1
            var1.set(0)
            cells.to_csv(thecsv, index=False)
        if var2.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[1]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 2")
            var2.set(0)
            cells.to_csv(thecsv, index=False)
        if var3.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[2]
            skillcounter = skillcounter + 1
            var3.set(0)
            cells.to_csv(thecsv, index=False)
        if var4.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[3]
            skillcounter = skillcounter + 1
            var4.set(0)
            cells.to_csv(thecsv, index=False)
        if var5.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[4]
            skillcounter = skillcounter + 1
            var5.set(0)
            cells.to_csv(thecsv, index=False)
        if var6.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[5]
            skillcounter = skillcounter + 1
            var6.set(0)
        if var7.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[6]
            skillcounter = skillcounter + 1
            var7.set(0)
        if var8.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[7]
            skillcounter = skillcounter + 1
            var8.set(0)
        if var9.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[8]
            skillcounter = skillcounter + 1
            var9.set(0)
        if var10.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[9]
            skillcounter = skillcounter + 1
            var10.set(0)
        if var11.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[10]
            skillcounter = skillcounter + 1
            var11.set(0)
        if var12.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[11]
            skillcounter = skillcounter + 1
            var12.set(0)
        if var13.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[12]
            skillcounter = skillcounter + 1
            var13.set(0)
        if var14.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[13]
            skillcounter = skillcounter + 1
            var14.set(0)
        if var15.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[14]
            skillcounter = skillcounter + 1
            var15.set(0)
        if var16.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[15]
            skillcounter = skillcounter + 1
            var16.set(0)
        if var17.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[16]
            skillcounter = skillcounter + 1
            var17.set(0)
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
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[0]
            skillcounter = skillcounter + 1
            var1.set(0)
            cells.to_csv(thecsv, index=False)
        if var2.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[1]
            skillcounter = skillcounter + 1
            print("question counter: ", questioncounter, "got skill 2")
            var2.set(0)
            cells.to_csv(thecsv, index=False)
        if var3.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[2]
            skillcounter = skillcounter + 1
            var3.set(0)
            cells.to_csv(thecsv, index=False)
        if var4.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[3]
            skillcounter = skillcounter + 1
            var4.set(0)
            cells.to_csv(thecsv, index=False)
        if var5.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[4]
            skillcounter = skillcounter + 1
            var5.set(0)
            cells.to_csv(thecsv, index=False)
        if var6.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[5]
            skillcounter = skillcounter + 1
            var6.set(0)
        if var7.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[6]
            skillcounter = skillcounter + 1
            var7.set(0)
        if var8.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[7]
            skillcounter = skillcounter + 1
            var8.set(0)
        if var9.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[8]
            skillcounter = skillcounter + 1
            var9.set(0)
        if var10.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[9]
            skillcounter = skillcounter + 1
            var10.set(0)
        if var11.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[10]
            skillcounter = skillcounter + 1
            var11.set(0)
        if var12.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[11]
            skillcounter = skillcounter + 1
            var12.set(0)
        if var13.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[12]
            skillcounter = skillcounter + 1
            var13.set(0)
        if var14.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[13]
            skillcounter = skillcounter + 1
            var14.set(0)
        if var15.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[14]
            skillcounter = skillcounter + 1
            var15.set(0)
        if var16.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[15]
            skillcounter = skillcounter + 1
            var16.set(0)
        if var17.get() == 1 and skillcounter <=5:
            cells.loc[questioncounter-1, 'Skill '+str(skillcounter)] = skills[16]
            skillcounter = skillcounter + 1
            var17.set(0)
        if skillcounter > 6:
            print("skills selcted are: ",skillcounter)
            mb.showinfo("Result", "Maximum # of skills is 5!")

Button(master, text='Next', command=var_states, highlightbackground='#000011').grid(row=15, column = 2, sticky="", pady=5)

mainloop()

if questioncounter > 2:
    print("Writing to the file")
    print(cells)
    cells.to_csv(thecsv, index=False)
# writing into the file
#cells.to_csv(question_spreadsheet, index=False)
