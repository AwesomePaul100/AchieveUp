# Paul Amoruso
# Thesis EEL 6971
# Instructor: Dr. Ronald DeMara

# importing the required modules
import glob
import pandas as pd
import itertools
import collections
from collections import Counter
from collections import OrderedDict
# libraries to be imported to send emails.
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json
import requests
import csv

# Storing badges to links.

# Opening JSON file.
f = open('data.json')

# Returns JSON object as a dictionary.
data = json.load(f)

thebadgenames = {}

# Part of the original version that used acronyms.
# Iterating through the json list.
#for x, y in zip(data['options'], data['badges']):
#    thebadgenames[x] = y
#print("The badge names:",thebadgenames)

thelinks = {}

# Iterating through the json list.
#for x, y in zip(data['options'], data['links']):
#    thelinks[x] = y
#print("The links:",thelinks)

# Send API request to retrive the data from Canvas
headers ={'Authorization':'Bearer '+data['token'][0]}

########### Url to extract course questions details
url_name = 'https://webcourses.ucf.edu/api/v1/courses/1158000000'+ data['url'][0]

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
print(title_course)

# List of the skills
skillsGUI = []

# Open the CSV file for reading.
with open(title_course+'_generated_skills.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    # Initialize an empty list to store the results.
    #result_list = []

    # Iterate over each row in the CSV file.
    loop_counter = 0
    for row in reader:
        original_value = row['Generative_AI_suggested_skill_list']
        replaced_value = row['Instructor_refined_skill_list']

        # Check if the "replaced_values" column is not empty.
        if replaced_value.strip() != "":
            # If it's not empty, add the value from that column to the result list.
            thebadgenames[replaced_value] = (replaced_value)
            skillsGUI.append(replaced_value)
        else:
            # If it's empty, add the original value to the result list.
            thebadgenames[original_value] = (original_value)
            skillsGUI.append(original_value)
            
        loop_counter = loop_counter + 1
    # Print the resulting list.
    print(thebadgenames)

#Iterating through the json list.
for x, y in zip(skillsGUI, data['links']):
    thelinks[x] = y
print("The links:",thelinks)
# Closing file
f.close()

# Python code to illustrate Sending mail with attachments
# from your Gmail account
def send_email(email, badges):
    theBadges = ""
    thelinksinemail = ""
    print("the badges to email", badges)
    for i in badges:
        # Only want the skills not the instances of that skill to send to the student.
        if not isinstance(i,int):
            if i != '':
                theBadges = theBadges + " " + i +","
                print("thebadge: ", theBadges)
                thelinksinemail = thelinksinemail + "\n" + thelinks[i]
                print("thelinksinemail: ", thelinksinemail)
    email = (str(email) + "\nHello, \n\n" + "You have received a badge in"+ str(theBadges)+" from EEL3801.\n\nBadges are evidence of competency in select specific skills.\nIf you wish to add the badge to your LinkedIn profile, please refer to the attached file for instructions.\n\nLink to graphic(s): " + str(thelinksinemail)+"\n\n\n")
    print(email)
    
    #open text file
    text_file = open("email_list.txt", "a")
     
    #write string to file
    n = text_file.write(email)
     
    #close file
    text_file.close()
     
    print(n)

# specifying the path to csv files
path = "skill_status"

# csv files in the path
files = glob.glob(path + "/*.csv")

# defining an empty list to store
# content
data_frame = pd.DataFrame()
content = []

# checking all the csv files in the specified path.
Numberfiles = 0
for filename in files:
    # reading content of csv file
    # content.append(filename)
    df = pd.read_csv(filename, index_col=None)
    content.append(df)
    Numberfiles += 1
#print("the content: ", content)

# converting content to data frame
data_frame = pd.concat(content)
print(data_frame)

# Get rid of the column that automatically gets made.
data_frame.drop('Unnamed: 0', inplace=True, axis=1)

#print("original data fram: ", data_frame)
#data_frame.to_csv("original_data_frame.csv")

dict = {}

theList = []

if "m" in dict:
    print("in dict", dict["m"])
data_frame = data_frame.reset_index()
for ids in data_frame.iterrows():
    print("the ids",ids[1][4])
    theString = ids[1][4].replace("[",'')
    theString = theString.replace("]",'')
    theString = theString.replace("'",'')
    theList = theString.split(",")
    print(theList)
    if str(ids[1][2]) in dict:
        dict[str(ids[1][2])] = list(itertools.chain(dict[str(ids[1][2])], theList))
    else:
        dict[str(ids[1][2])] = theList
        
print("The dictionary:", dict)
print("The dictionary size:", len(dict))

theBadges = {}

for key, value in dict.items():
    #print(key, ': ', value)
    theString = str(value).replace("[",'')
    theString = theString.replace("]",'')
    theString = theString.replace("' ","'")
    theString = theString.replace("'",'')
    #print("\n\n\n\n hey: ", theString)
    theString = theString.replace(", ",",")
    #print("\n\n\n\n hey: ", theString)
    theList = theString.split(",")
    print("The list", theList)
    #print(theList)
    cnt = Counter(theList)
    print("the cnt", cnt)
    #od = OrderedDict(cnt.most_common())
    od = cnt.most_common()
    print("The original list ",od)
    NIDs = key
    #print(type(od))
    number = 0
    tempList = []
    for key, value in od:
        print("looking at ", od[number])
        if value >= 3:
            print(key,"!!!!!!!!!!!!!!!!!!")
            tempList += od[number]
            theBadges[str(NIDs)] = tempList
        else:
            print("removing ", od[number])
            #od.remove(od[number])
            #print(od)
            theBadges[str(NIDs)] = tempList
        number += 1
print("\n The badges = ",theBadges)
print(data_frame)

        
print(data_frame)

# Remove the repeating rows.
data_frame.drop(data_frame.index[len(dict):], inplace=True)
data_frame.to_csv('data_fram.csv')

#data_frame = data_frame.head((-len(dict))*(Numberfiles-1))

# Get rid of the column that automatically gets made.
data_frame.drop('index', inplace=True, axis=1)

data_frame.to_csv('overall.csv')
i = 0
print(dict)
print(len(dict))

# open file.
text_file = open("email_list.txt", "w")
# Now clear it.
n = text_file.write('')
#close file
text_file.close()
 
print(n)

while i < len(dict):
    cells = pd.read_csv("overall.csv")
    #cells.loc[i, 'Skills'] = 'yo'
    string = cells.loc[i, 'Skills']
    print("String ",string)
    #print("Student ",theBadges["5058343"])
    print("+++\n",str(cells.loc[i, 'NIDs']))
    user = str(cells.loc[i, 'NIDs'])
    newList = theBadges[user]
    if len(newList) > 0:
        send_email(cells.loc[i, 'Emails'], newList)
    print("new list",newList)
    cells.loc[i, 'Skills'] = str(newList)
    #print("hey")
    cells.to_csv("overall.csv", index=False)
    i+=1

#https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
#https://appdividend.com/2020/09/25/how-to-convert-python-string-to-array/
#https://note.nkmk.me/en/python-collections-counter/
#https://www.geeksforgeeks.org/remove-last-n-rows-of-a-pandas-dataframe/
#https://www.educative.io/edpresso/how-to-remove-a-key-value-pair-from-a-dictionary-in-python
