#!/usr/bin/python

import requests
import time
import json

apiKey = json.load(open('private.json'))["api-key"]
requestUrl = 'https://namescan.io/api/v2/person-scans/standard'

originalCsv = open("input.csv", "r")
processedCsv = open("output.csv", "a+")
rawResponses = open("output_raw.txt", "a+")

processedLines = len(processedCsv.readlines())
sentRequests = 0
maxRequests = 250

# This makes the output line the same as in the original doc
if processedLines == 0:
    processedLines = 1
    processedCsv.write("name,first_name,middle_name,last_name,dob,gender,country,\n")

def splitCsvLine(csvLine):
    splitLine = csvLine.split(",")
    dateOfBirthList = splitLine[4].split("/")
    dateOfBirth = "/".join([
        '{0:02d}'.format(int(dateOfBirthList[1])),
        '{0:02d}'.format(int(dateOfBirthList[0])),
        dateOfBirthList[2]
    ])
    lineDictionary = {
        "dob": dateOfBirth,
        "country": splitLine[6],
    }
    if splitLine[0] != "n/a":
        lineDictionary['name'] = splitLine[0]
    else:
        lineDictionary['first_name'] = splitLine[1]
        if splitLine[2] != "n/a":
            lineDictionary['middle_name'] = splitLine[2]
        lineDictionary['last_name'] = splitLine[3]
    if splitLine[5] and splitLine[5] != "n/a":
        lineDictionary['gender'] = "female" if splitLine[5] == "f" else "male"
    return lineDictionary

def appendCsvLine(lineDictionary):
    processedCsv.write(",".join([
        lineDictionary.get('name', ''),
        lineDictionary.get('first_name', ''),
        lineDictionary.get('middle_name', ''),
        lineDictionary.get('last_name', ''),
        lineDictionary.get('dob', ''),
        lineDictionary.get('gender', ''),
        lineDictionary.get('country', ''),
        lineDictionary.get('matches', '')
    ]))
    processedCsv.write("\n")

def sendRequest(lineDictionary):
    headers = {
        "api-key": apiKey,
        "content-type": "application/json"
    }
    print lineDictionary
    response = requests.post(requestUrl, headers = headers, json = lineDictionary)
    decoded = response.json()
    rawResponses.write(str(lineDictionary) + "\n" + str(decoded) + "\n\n")
    print (decoded)
    print (decoded["number_of_matches"])
    print (decoded["number_of_matches"] == 0)
    lineDictionary["matches"] = str( (decoded["number_of_matches"] == 0) )

for csvLine in originalCsv.readlines()[processedLines:]:
    lineDictionary = splitCsvLine(csvLine)
    sendRequest(lineDictionary)
    appendCsvLine(lineDictionary)
    sentRequests += 1
    if sentRequests == maxRequests:
        print "api requests exhausted"
        exit()

print sentRequests

originalCsv.close()
processedCsv.close()
rawResponses.close()

