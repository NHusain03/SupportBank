import logging
import csv
import json
import xml.dom.minidom
from datetime import datetime
from datetime import timedelta


class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.localTransactions = []
        self.localAccounts = {}

    def readFile(self):
        self.localTransactions = []
        self.localAccounts = {}

        # Reading .csv file
        if self.filename[-1] == "v":
            with open(self.filename) as csvfile:
                csvReader = csv.reader(csvfile, delimiter=',')
                for row in csvReader:
                    self.localTransactions.append(row)

            self.localTransactions = self.localTransactions[1:]

        # Reading .json file
        elif self.filename[-1] == "n":
            with open(self.filename, 'r') as fcc_file:
                trans_data = json.load(fcc_file)

                # Formatting date to dd/mm/yyyy
                for trans in trans_data:
                    trans_list = list(trans.values())
                    trans_list[0] = trans_list[0][:10].split("-")
                    trans_list[0].reverse()
                    trans_list[0] = "/".join(trans_list[0])

                    self.localTransactions.append(trans_list)

        # Reading .xml file
        elif self.filename[-1] == "l":
            file = xml.dom.minidom.parse(self.filename)
            models = file.getElementsByTagName('SupportTransaction')

            for model in models:
                trans = [
                    self.dateConverterXML(model.attributes['Date'].value),
                    model.getElementsByTagName('Parties')[0].getElementsByTagName('From')[0].firstChild.data,
                    model.getElementsByTagName('Parties')[0].getElementsByTagName('To')[0].firstChild.data,
                    model.getElementsByTagName('Description')[0].firstChild.data,
                    model.getElementsByTagName('Value')[0].firstChild.data
                ]
                self.localTransactions.append(trans)

        # Updating accounts
        for t in self.localTransactions:
            try:
                if t[1] in self.localAccounts:
                    self.localAccounts[t[1]] -= float(t[4])
                else:
                    self.localAccounts[t[1]] = (float(t[4]) * -1)

                if t[2] in self.localAccounts:
                    self.localAccounts[t[2]] += float(t[4])
                else:
                    self.localAccounts[t[2]] = float(t[4])
            except:
                logging.warning("Line skipped: " + str(t) + ", " + t[4] + " is not a number")

    def getTransactionsAccounts(self):
        self.readFile()
        return self.localTransactions, self.localAccounts

    # Converting XML date to dd/mm/yyyy format
    def dateConverterXML(self, XMLdays):
        new_date = datetime(1900, 1, 1, 0, 0, 0) + timedelta(days = int(XMLdays))
        string_date = new_date.strftime("%d/%m/%Y")
        return string_date
