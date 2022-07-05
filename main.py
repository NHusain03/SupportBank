import logging
import csv


accounts = {}
transactions = []
dodgyTransactions = []

logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)

with open('Transactions2014.csv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',')
    for row in csvReader:
        transactions.append(row)

with open('DodgyTransactions2015.csv') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',')
    for row in csvReader:
        dodgyTransactions.append(row)

transactions = transactions[1:]
dodgyTransactions = dodgyTransactions[1:]
transactions = transactions + dodgyTransactions

for t in transactions:
    try:
        if t[1] in accounts:
            accounts[t[1]] -= float(t[4])
        else:
            accounts[t[1]] = (float(t[4]) * -1)

        if t[2] in accounts:
            accounts[t[2]] += float(t[4])
        else:
            accounts[t[2]] = float(t[4])
    except:
        logging.warning(str(t))




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    finished = False

    while not finished:
        command = input("Enter command: ")
        if command == "All":
            for account in accounts:
                print(account + " " + "£"+ str(round(accounts[account], 2)))
        elif command in accounts:
            for t in transactions:
                if command == t[1] or command == t[2]:
                    print(t)
        elif command == "Done":
            finished = True
        else:
            print("Try again.")

