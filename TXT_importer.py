import csv

def import_txt(File_to_import):                                         # Function to import any TXT file and return it in the form of a n dimensional list
    with open(File_to_import) as csv_file:                              # Recommended to use with when opening files to prevent corruption in case of sudden close. Open File_to_import as a csv file
        csv_reader = csv.reader(csv_file, delimiter='\t')               # Import the file into a set
        line_count = 0                                                  # Initialize the line_count
        First_sub_item = True
        for row in csv_reader:                                          # For each row in the set :
            if line_count == 0:                                         # We first discard the headers. If needed they can be extracted and returned as well
                #print(f'Column names are: {", ".join(row)}')           # Print For debugging purposes
                line_count += 1                                         # We increase the line count to jump to the next step on the next iteration
            elif line_count == 1:                                       # When we are in the first data row
                for index,item in enumerate(row):
                    if First_sub_item:
                        items = [float(repr(row[index]).replace("'",""))]
                        First_sub_item = False
                    else:
                        items.append(float(repr(row[index]).replace("'","")))
                Variable_for_data = list([items])                       # We initialize a item dimensional list with the first items
                line_count += 1                                         # We increase the line count to jump to the next step on the next iteration

            else :                                                      # When we are in the second or later data rows
                First_sub_item = True
                items = []
                for index, item in enumerate(row):
                    if First_sub_item:
                        items = [float(repr(row[index]).replace("'", ""))]
                        First_sub_item = False
                    else:
                        items.append(float(repr(row[index]).replace("'", "")))
                Variable_for_data.append(items)                         # We append the current items to the already existing item dimensional list to add the values as rows within the list
                ##print(temp_array)                                     # Print For debugging purposes
                line_count += 1                                         # We increase the line count even though it is not really necessary
                #print(*Variable_for_data, sep='\n')
        #print(f'Processed {line_count} lines.')                        # Print For debugging purposes
        #print(temp_array)                                              # Print For debugging purposes
        #print(temp_array.shape)                                        # Print For debugging purposes
        #print(*Variable_for_data, sep='\n')                            # Print For debugging purposes
        return Variable_for_data                                        # When the for loop finishes we return the created lis

def import_txt_to_string_list(File_to_import):                                         # Function to import any TXT file and return it in the form of a n dimensional list
    with open(File_to_import) as csv_file:                              # Recommended to use with when opening files to prevent corruption in case of sudden close. Open File_to_import as a csv file
        csv_reader = csv.reader(csv_file, delimiter=',')               # Import the file into a set
        Variable_for_data = []
        for row in csv_reader:                                          # For each row in the set :
            for i,item in enumerate(row):
                row[i] = row[i].replace('[','')
                row[i] = row[i].replace("]", "")
                row[i] = row[i].replace("(", "")
                row[i] = row[i].replace(")", "")
                row[i] = row[i].replace("'","")
            #     print(row[i])
            #     input('Press enter')
            # print(row)
            Variable_for_data.append(row)                         # We append the current items to the already existing item dimensional list to add the values as rows within the list
            #print(*Variable_for_data, sep='\n')
        #print(f'Processed {line_count} lines.')                        # Print For debugging purposes
        #print(temp_array)                                              # Print For debugging purposes
        #print(temp_array.shape)                                        # Print For debugging purposes
        #print(*Variable_for_data, sep='\n')                            # Print For debugging purposes
        return Variable_for_data                                        # When the for loop finishes we return the created lis

def import_txt_to_string_list_one_col_only(File_to_import,col = 0):                                         # Function to import any TXT file and return it in the form of a n dimensional list
    with open(File_to_import) as csv_file:                              # Recommended to use with when opening files to prevent corruption in case of sudden close. Open File_to_import as a csv file
        csv_reader = csv.reader(csv_file, delimiter=',')               # Import the file into a set
        Variable_for_data = []
        for row in csv_reader:                                          # For each row in the set :
            row[col] = row[col].replace('[','')
            row[col] = row[col].replace("]", "")
            row[col] = row[col].replace("(", "")
            row[col] = row[col].replace(")", "")
            row[col] = row[col].replace("'","")
            #     print(row[i])
            #     input('Press enter')
            # print(row)
            Variable_for_data.append(row[col])                         # We append the current items to the already existing item dimensional list to add the values as rows within the list
            #print(*Variable_for_data, sep='\n')
        #print(f'Processed {line_count} lines.')                        # Print For debugging purposes
        #print(temp_array)                                              # Print For debugging purposes
        #print(temp_array.shape)                                        # Print For debugging purposes
        #print(*Variable_for_data, sep='\n')                            # Print For debugging purposes
        return Variable_for_data                                        # When the for loop finishes we return the created lis