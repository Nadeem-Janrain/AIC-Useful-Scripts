# AgentDelete script, written by Nadeem Rasool
# Script will run the apid-cli entity.delete from a csv file of email address
#!/usr/bin/python3
import os
import csv
inputFile = open('Test.csv', 'r') #This is a CSV file which contains the list of email address of agents for the console
with inputFile:
    reader = csv.reader(inputFile, delimiter="|") #Setting the delimiter
    for row in reader:
        for email in row:            
            print("apid-cli ed user --key-attribute email --key-value '\""+email+"\"' -c dashboard-metadata")
            # The following location for apid-cli.rb may be different on your environment,
            os.system("/Users/<your user>/Documents/GitHub/capture_utils/cli/apid-cli.rb ed user --key-attribute email --key-value '\""+email+"\"' -c dashboard-metadata")