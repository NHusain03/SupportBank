class Transaction():
    def __init__(self, Date,From,To,Narrative,Amount):
        self.date = Date
        self.personA = From
        self.personB = To
        self.narrative = Narrative
        self.amount = float(Amount)

    def __str__(self):
        return self.date + "," + self.personA + "," + self.personB + "," + self.narrative + "," + str(self.amount)
