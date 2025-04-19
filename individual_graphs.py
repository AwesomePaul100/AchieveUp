import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import math

# Read the CSV file into a DataFrame
df = pd.read_csv("Student_Skill_Status_ASEE-SE_binary.csv")
print(df)

# Create a directory to store the individual line graphs
output_directory = "individual_line_graphs"
os.makedirs(output_directory, exist_ok=True)

def modify_string(input_string):
    for i, char in enumerate(input_string):
        if char.isdigit():
            return input_string[:i+1]
    return input_string[:15]
def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
        
def is_int_or_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Iterate through the rows and create individual plots for each skill
for index, row in df.iterrows():
    if (row['Skills'] != '' and row['Skills'] != ' ' and row['Skills'] != 'nan'):
        skills = (row['Skills'])
        print("skills: ", skills)
        x_values = []
        y_values = []
        # Check if there are any percentage values in the row.
        #print("\nvalue: ",row.iloc[2:])
        #if row.iloc[2:].str.contains('%').any():
        for col in row.index[1:]:
            print("column:", col)
            print("str(row[col])", str(row[col]))
            if (is_integer(str(row[col])) or is_int_or_float(str(row[col]))):
                print(str(row[col]), " is an integer")
                x_values.append(str(col))
                y_values.append(float(row[col]))
        print("sum:", sum(y_values))
        if (sum(y_values) < 1) or math.isnan(sum(y_values)):
            continue
        #x_values = [str(col) for col in row.index[1:] if '%' in str(row[col])]
        print ('axis: ', x_values)
        #for col in x_values:
         #   y_values.append(float(row[col].rstrip('%')))
        #y_values = [float(row[col].rstrip('%')) for col in x_values]
        print ('y values: ',y_values)
        
        # Make the x values pretty.
        counter = 0
        for val in x_values:
            print("new value: ", val[:8])
            x_values[counter] = modify_string(val)
            counter = counter + 1
                
            
            # Create a plot
            plt.figure()
            #plt.plot(x_values, y_values, marker='o')
            plt.bar(x_values, y_values, color ='gray', width = 0.5)
            plt.xlabel("Quizzes")
            plt.ylabel("# Of Students")
            plt.title(f"Skill {skills} Performance")
            filename = os.path.join(output_directory, f"skill_{skills}_performance.png")
            plt.savefig(filename)
            plt.close()

# Print a message to indicate the saving is complete
print("Individual line graphs saved to", output_directory)

