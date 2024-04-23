import os
import csv


# Define the directory path
directory = r'C:\Users\Jan Jiri Bauer\OneDrive - Vysoké učení technické v Brně\Bakalářská práce\Mereni1'

# Walk through the directory structure
for root, dirs, files in os.walk(directory):
    for file in files:
        # Check if the file is a CSV file
        if file.endswith('.csv'):
            # Get the full path of the CSV file
            file_path = os.path.join(root, file)
            print(file)
            
            # Open the CSV file
            with open(file_path, 'r') as csv_file:
                # Create a CSV reader
                csv_reader = csv.reader(csv_file)
                data = list(csv_reader)
                # Iterate over each row in the CSV file
                for row in data:
                    if row[0].isnumeric():
                        if row[1] == "POLL":
                            message_num = row[0]
                            POLL[message_num]: list = [row[2], row[3]]
                            

                        elif row[0] == message_num and row[1] == "POLL_ACK" :
                            POLL_ACK: list = [row[2], row[3]]

                        elif row[0] == message_num and row[1] == "RANGE" :
                            RANGE: list = [row[2], row[3]]
                            if 
