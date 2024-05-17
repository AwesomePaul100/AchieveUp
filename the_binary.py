import csv
import random
import os

def generate_random_ids():
  ids = [2,5,7,8,10]
  return ids

def create_csv_file(file_path, ids, initial_values):
  with open(file_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["student_id", "initial"])
    for i in range(len(ids)):
      writer.writerow([ids[i], initial_values[i]])
    writer.writerow(["sum", 0])

def perform_logical_or_operation(file_path, assignment,ids, binary_scores):
  with open(file_path, "r", newline="") as csvfile:
    reader = csv.reader(csvfile)
    data = []
    for row in reader:
      data.append(row)

  # Get the index of the last column
  last_column_index = len(data[0]) - 1

  # Create a new column called run1 (or run2, etc., depending on the number of existing columns)
  data[0].append(assignment)
  for i in range(len(data)-1):
    data[i+1].append(0)
  print(data)
  newlist = []
  # Iterate over the ids and binary_scores arrays
  for i in range(len(data) - 2):
    # Find the corresponding student data row
    print("index value: ", len(data))
    for n in range(len(ids)):
      print(data[i+1][0], ids[n])
      if int(data[i+1][0]) == int(ids[n]):
        print("yo", data[i+1][last_column_index + 1], binary_scores[n])
        # Perform the logical OR operation
        data[i+1][last_column_index + 1] = int(data[i+1][last_column_index]) | int(binary_scores[n])
        print("New value: ", data[i+1][last_column_index + 1])
        break
      else:
        data[i+1][last_column_index + 1] = int(data[i+1][last_column_index])
        
    # Update the sum.
    sum = 0
    for i in range(len(data) - 2):
      sum += data[i+1][last_column_index + 1]
    data[len(data) - 1][last_column_index + 1] = sum
    print("student_data_row")
    #student_data_row = [row for row in data if row[0] == ids[i]][0]
    print("student_data_row[-1]")
    

  # Write the updated data to the CSV file
  with open(file_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)
  
  # Used for the skillAssigner.
  return sum

def main(skill, assignment,ids, second_ids, second_binary_values):
  # Generate random IDs
  #ids = generate_random_ids()

  # Create initial values for the students
  initial_values = [0] * len(ids)
  # Check if the CSV file exists.
  file_exists = os.path.isfile(skill + ".csv")
  # Create the CSV file.
  if not file_exists:
    create_csv_file(skill+".csv", ids, initial_values)

  # Take in a second array of IDs (might be less than 5) and corresponding binary values
  #second_ids = [2, 7, 8, 5, 10]
  #second_binary_values = [1, 1, 1, 1, 1]

  # Perform logical OR operation for the corresponding ID binary values that are stored in the rightmost column and store the new logical operation output in a new column
  sum = perform_logical_or_operation(skill+".csv", assignment, second_ids, second_binary_values)
  return sum

'''if __name__ == "__main__":
  main(skill, ids, second_ids, second_binary_values)
  #main("test_skill", [1,2,3,4,5,7,8,10], [1,2,3,5,7,8,10], [1,0,1,0,1,0,1])
'''
