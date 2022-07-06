import Parser
import logging

accounts = {}
transactions = []

logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    finished = False

    while not finished:
        command = input("Enter command: ")
        commandSep = command.split(" ")

        if commandSep[0] == 'Import':
            p = Parser.Parser(commandSep[2])
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

