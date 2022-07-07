import logging
import csv
import json
import xml.dom.minidom
from datetime import datetime
from datetime import timedelta

import Transactions


class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.localTransactions = []
        self.localAccounts = {}

    def readCSV(self, filename):
        csvTrans = []

        with open(filename) as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            first = True
            for row in csvReader:
                if not first:
                    trans = Transactions.Transaction(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4]
                    )
                    csvTrans.append(trans)
                else:
                    first = False

        return csvTrans

    def readJSON(self, filename):
        jsonTrans = []

        with open(filename, 'r') as fcc_file:
            trans_data = json.load(fcc_file)

            # Formatting date to dd/mm/yyyy
            for trans in trans_data:
                trans_list = list(trans.values())
                trans_list[0] = trans_list[0][:10].split("-")
                trans_list[0].reverse()
                trans_list[0] = "/".join(trans_list[0])

                trans = Transactions.Transaction(
                    trans_list[0],
                    trans_list[1],
                    trans_list[2],
                    trans_list[3],
                    trans_list[4]
                )

                jsonTrans.append(trans)

            return jsonTrans

    def readXML(self, filename):
        xmlTrans = []

        file = xml.dom.minidom.parse(self.filename)
        models = file.getElementsByTagName('SupportTransaction')

        for model in models:
            trans = Transactions.Transaction(
                self.dateConverterXML(model.attributes['Date'].value),
                model.getElementsByTagName('Parties')[0].getElementsByTagName('From')[0].firstChild.data,
                model.getElementsByTagName('Parties')[0].getElementsByTagName('To')[0].firstChild.data,
                model.getElementsByTagName('Description')[0].firstChild.data,
                model.getElementsByTagName('Value')[0].firstChild.data
            )
            xmlTrans.append(trans)

        return xmlTrans

    def getTransactionsAccounts(self):
        if self.filename[-4:] == ".csv":
            self.localTransactions = self.readCSV(self.filename)

        elif self.filename[-5:] == ".json":
            self.localTransactions = self.readJSON(self.filename)

        elif self.filename[-4:] == ".xml":
            self.localTransactions = self.readXML(self.filename)

        for t in self.localTransactions:
            try:
                if t.personA in self.localAccounts:
                    self.localAccounts[t.personA] -= float(t.amount)
                else:
                    self.localAccounts[t.personA] = (float(t.amount) * -1)

                if t.personB in self.localAccounts:
                    self.localAccounts[t.personB] += float(t.amount)
                else:
                    self.localAccounts[t.personB] = float(t.amount)
            except:
                logging.warning("Line skipped: " + str(t) + ", " + t.amount + " is not a number")

        return self.localTransactions, self.localAccounts

    # Converting XML date to dd/mm/yyyy format
    def dateConverterXML(self, XMLdays):
        new_date = datetime(1900, 1, 1, 0, 0, 0) + timedelta(days = int(XMLdays))
        string_date = new_date.strftime("%d/%m/%Y")
        return string_date
