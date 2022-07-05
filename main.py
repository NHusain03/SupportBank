import logging
import csv
import json

with open('Transactions2013.json', 'r') as fcc_file:
    fcc_data = json.load(fcc_file)
    print(list(fcc_data[0].values()))

accounts = {}
transactions = []

logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)

# for t in transactions:
#     try:
#         if t[1] in accounts:
#             accounts[t[1]] -= float(t[4])
#         else:
#             accounts[t[1]] = (float(t[4]) * -1)
#
#         if t[2] in accounts:
#             accounts[t[2]] += float(t[4])
#         else:
#             accounts[t[2]] = float(t[4])
#     except:
#         logging.warning(str(t))

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

        elif self.filename[-1] == "n":
            with open(self.filename, 'r') as fcc_file:
                trans_data = json.load(fcc_file)
                for trans in trans_data:
                    self.localTransactions.append(list(trans.values()))


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

        self.localTransactions = self.localTransactions[1:]

    def getTransactionsAccounts(self):
        self.readFile()
        return (self.localTransactions, self.localAccounts)


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

        elif command == "Done":
            finished = True

        else:
            print("Try again.")

