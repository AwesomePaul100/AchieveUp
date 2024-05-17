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

# Iterate through the rows and create individual plots for each skill
for index, row in df.iterrows():
    if (row['Skills'] != ''):
        skills = (row['Skills'])
        print (skills)
        x_values = []
        y_values = []
        # Check if there are any percentage values in the row
        if row.iloc[2:].str.contains('%').any():
            for col in row.index[1:]:
                if '%' in str(row[col]):
                    x_values.append(str(col))
            #x_values = [str(col) for col in row.index[1:] if '%' in str(row[col])]
            print ('axis: ', x_values)
            for col in x_values:
                y_values.append(float(row[col].rstrip('%')))
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

