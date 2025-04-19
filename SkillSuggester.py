import tkinter as tk
from tkinter import messagebox
import python_client_skills
import csv
import os
import socket
import tkinter as tk
from tkinter import messagebox
import json
import requests

# Opening JSON file
f = open('data.json')

# returns JSON object as a dictionary
data = json.load(f)

server_ip = data['ip'][0]
print("server IP is: ", server_ip)

# Send API request to retrive the data from Canvas
headers ={'Authorization':'Bearer '+data['token'][0]}

########### Url to extract course questions details
url = 'https://webcourses.ucf.edu/api/v1/courses/1158000000'+ data['url'][0]

# Closing file
f.close()


# Let us get the title of the assignment first.
url_course_name = url
r_course_name = requests.get(url_course_name,headers = headers)
print(r_course_name.status_code)
if r_course_name.status_code != 200:
    print("\nPlease check the token\n")
json_course_name_data = json.loads(r_course_name.text)

# The title.
title = json_course_name_data['name']
print(json_course_name_data['name'])
title = title.replace(' ', '_')

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

# Check if the file exists
if os.path.exists(title+ "_generated_skills.csv"):
  print("skills.csv exists in the directory.")
  # Open the CSV file for reading
  with open(title+'_generated_skills.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    # Initialize an empty list to store the results
    result_list = []

    # Iterate over each row in the CSV file
    for row in reader:
        original_value = row['Generative_AI_suggested_skill_list']
        replaced_value = row['Instructor_refined_skill_list']

        # Check if the "replaced_values" column is not empty
        if replaced_value.strip() != "":
            # If it's not empty, add the value from that column to the result list
            result_list.append(replaced_value)
        else:
            # If it's empty, add the original value to the result list
            result_list.append(original_value)

    # Print the resulting list
    print(result_list)
else:
  print("skills.csv does not exist in the directory.")
  # Get the server IP address from the user (or hardcode it)
  #server_ip = '192.168.168.103'

  # Check the server status
  if check_server_status(server_ip):
   print(f"{server_ip} is online.")
  else:
   show_offline_message(server_ip)
  def get_string():
    root = tk.Tk()
    root.title("SkillSuggester")
    root.geometry("300x100")  # Set width to 300 pixels, height to 100 pixels.
    root.resizable(True, True)  # Allow resizing in both directions
    label = tk.Label(root, text="Please enter the course name:", font=("Helvetica", 13))
    label.pack()

    entry = tk.Entry(root)
    entry.pack()

    def save_string():
        global user_input
        user_input = entry.get().replace(' ', '_')
        print(user_input)
        if user_input:
            messagebox.showinfo("Success", f"Your input is: {user_input}")
            root.destroy()
        else:
            messagebox.showerror("Error", "Please enter a string")

    button = tk.Button(root, text="Save", command=save_string)
    button.pack()

    root.mainloop()
    return user_input

  user_input = get_string()
  print(user_input)
  #exit()
  auto_skills = (str(python_client_skills.main(user_input.replace(' ','_'))))
  auto_skills = auto_skills.replace('</start_of_turn>','')
  skills_list = [item.strip() for item in auto_skills.split(', ')]
  print(skills_list)


  skills_list += [""] * (17 - len(skills_list))  # add empty strings to fill up to 17

  skills_list = skills_list[:17]  # trim the list to 17 indexes, or less if it's already shorter

  print(skills_list)

  import pandas as pd


  # Convert the list to a pandas Series (a one-dimensional labeled array)
  series = pd.Series(skills_list, index=range(len(skills_list)))

  # Create a DataFrame with two columns: original values and replaced values
  df = pd.DataFrame({'Generative_AI_suggested_skill_list': series, 'Instructor_refined_skill_list': ''})

  # Write the DataFrame to a CSV file
  df.to_csv(title+'_generated_skills.csv', header=True, index=False)
