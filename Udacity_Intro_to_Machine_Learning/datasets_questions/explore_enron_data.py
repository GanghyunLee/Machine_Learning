#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle
import numpy as np

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "rb"), fix_imports=True)

print("Number of data points(people) : " + str(len(enron_data)))
print("Number of features each person : " + str(len(enron_data["SKILLING JEFFREY K"])))

# “poi”feature records whether the person is a person of interest,
# according to our definition. How many POIs are there in the E+F dataset?
# In other words, count the number of entries in the dictionary where
# data[person_name]["poi"]==1
resultTheNumberOfPOI = 0

for person_key, _ in enron_data.items():
    resultTheNumberOfPOI += (enron_data[person_key]["poi"]==1)

print("Number of the person is a person of interest(POI) : " + str(resultTheNumberOfPOI) )

# We compiled a list of all POI names (in ../final_project/poi_names.txt) and associated email addresses (in ../final_project/poi_email_addresses.py).
# How many POI’s were there total?
# (Use the names file, not the email addresses, since many folks have more than one address and a few didn’t work for Enron, so we don’t have their emails.)
result = 0
with open("../final_project/poi_names.txt", "r") as f:
    data = f.readlines()

    for line in data:
        result += 1

print("Number of POI in POI names file  : " + str(result - 2) )

print("Total value of the stock belonging to James Prentice : " + str(enron_data["PRENTICE JAMES"]["total_stock_value"]))
print("The number of email messages from Wesley Colwell to persons of interest : " + str(enron_data["COLWELL WESLEY"]["from_this_person_to_poi"]))

# CEO : Jeffrey Skilling
# Chairman : Kenneth Lay
# CFO : Andrew Fastow

FraudPersonArray = ["SKILLING JEFFREY K", "LAY KENNETH L", "FASTOW ANDREW S"]
mostMoney = 0
WhoTookMostMoney = ""

for nameKey in FraudPersonArray:
    money = enron_data[nameKey]["total_payments"]

    if money > mostMoney:
        mostMoney = money
        WhoTookMostMoney = nameKey

print("Who took most money : " + str(WhoTookMostMoney) + " (Money : " + str(mostMoney) + ")")

resultSalary = 0
resultEmail = 0

for person_key, _ in enron_data.items():
    resultSalary += (enron_data[person_key]["salary"]!="NaN")
    resultEmail += (enron_data[person_key]["email_address"]!="NaN")

print("Number of quantified Salary : "  + str(resultSalary))
print("Number of known email-address : "  + str(resultEmail))

resultTotalPaymentNaN = 0
for nameKey, _ in enron_data.items():
    resultTotalPaymentNaN += (enron_data[nameKey]["total_payments"] == "NaN")

print("Percentage of people have \"NaN\" for their total payments : " + str(resultTotalPaymentNaN / len(enron_data)))

resultPIOTotalPaymentNaN = 0
for person_key, _ in enron_data.items():
    resultPIOTotalPaymentNaN += (enron_data[person_key]["poi"]==1 and enron_data[person_key]["total_payments"]=="NaN")

print("Percentage of POI have \"NaN\" for their total payments : " + str(resultPIOTotalPaymentNaN / resultTheNumberOfPOI))

resultTotalPaymentNaN = 0
for person_key, _ in enron_data.items():
    resultTotalPaymentNaN += (enron_data[person_key]["total_payments"]=="NaN")

print("Number of \"NaN\" for their total payments : " + str(resultTotalPaymentNaN))