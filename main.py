import logging
import csv
import json
import xml.dom.minidom
from datetime import datetime
from datetime import timedelta

accounts = {}
transactions = []

logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)

class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.localTransactions = []
        self.localAccounts = {}

    def readFile(self):
        self.localTransactions = []
        self.localAccounts = {}

        if self.filename[-1] == "v":
            with open(self.filename) as csvfile:
                csvReader = csv.reader(csvfile, delimiter=',')
                for row in csvReader:
                    self.localTransactions.append(row)

            self.localTransactions = self.localTransactions[1:]

        elif self.filename[-1] == "n":
            with open(self.filename, 'r') as fcc_file:
                trans_data = json.load(fcc_file)
                for trans in trans_data:
                    trans_list = list(trans.values())
                    trans_list[0] = trans_list[0][:10].split("-")
                    trans_list[0].reverse()
                    trans_list[0] = "/".join(trans_list[0])

                    self.localTransactions.append(trans_list)

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
                logging.warning(str(t))


    def getTransactionsAccounts(self):
        self.readFile()
        return (self.localTransactions, self.localAccounts)

    def dateConverterXML(self, XMLdays):
        new_date = datetime(1900, 1, 1, 0, 0, 0) + timedelta(days = int(XMLdays))
        string_date = new_date.strftime("%d/%m/%Y")
        return string_date


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    finished = False

    while not finished:
        command = input("Enter command: ")
        commandSep = command.split(" ")

        if commandSep[0] == 'Import':
            p = Parser(commandSep[2])
            (t, a) = p.getTransactionsAccounts()

            transactions = transactions + t

            for person in a:
                if person in accounts:
                    accounts[person] += a[person]
                else:
                    accounts[person] = a[person]

        elif command == "List All":
            for account in accounts:
                print(account + " " + "£"+ str(round(accounts[account], 2)))

        elif commandSep[0] == "List" and " ".join(commandSep[1:]) in accounts:
            for t in transactions:
                if " ".join(commandSep[1:]) == t[1] or " ".join(commandSep[1:]) == t[2]:
                    print(t)

        elif commandSep[0] == "Export":
            with open(commandSep[2], 'w') as out_file:
                for t in transactions:
                    outputT = ",".join(map(lambda x: str(x), t))
                    out_file.write(outputT + "\n")

        elif command == "Done":
            finished = True

        else:
            print("Try again.")

