import math


class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []

    def __str__(self):
        rs = ""
        rs += "{:*^30s}\n".format(self.category)
        for transaction in self.ledger:
            if len(transaction["description"]) > 23:
                tx = transaction["description"][:23]
            else:
                tx = transaction["description"]
            rs += "{:<23s}{:>7.2f}\n".format(tx, transaction["amount"])
        rs += "Total: {:.2f}".format(self.get_balance())
        return rs

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, "Transfer to {}".format(category.category))
            category.deposit(amount, "Transfer from {}".format(self.category))
            return True
        else:
            return False

    def check_funds(self, amount):
        if self.get_balance() >= amount:
            return True
        else:
            return False

    def get_balance(self):
        balance = 0.00
        for transaction in self.ledger:
            balance += transaction["amount"]

        return balance

    def get_total_spent(self):
        spent = 0.00
        for transaction in self.ledger:
            if transaction["amount"] < 0:
                spent += transaction["amount"]

        return -spent


def create_spend_chart(categories):
    graph = []
    total = 0.00
    # Gather the basics for the chart.
    for category in categories:
        spent = category.get_total_spent()
        total += spent
        graph.append({"category": category, "amount": spent, "percent": 0})
    # Calculate the percent spent of total spent for each category,
    # rounded down to the nearest 10%.
    new_graph = []
    for bar in graph:
        new_graph.append(
            {
                "category": bar["category"],
                "amount": bar["amount"],
                "percent": math.floor((bar["amount"] * 100 / total) / 10) * 10,
            }
        )
    cs = ""
    cs += "Percentage spent by category\n"

    lines = []
    for i in reversed(range(11)):
        line = ""
        percentile = i * 10
        line += "{:3d}| ".format(percentile)
        for bar in new_graph:
            if bar["percent"] >= percentile:
                line += "o  "
            else:
                line += "   "
        lines.append(line)
    cs += "\n".join(lines)

    dashes = "\n    -"
    for category in categories:
        dashes += "---"
    cs += dashes + "\n"

    lines = []
    for letter in range(get_longest_category_length(categories)):
        line = "     "
        for category in categories:
            try:
                entry = category.category[letter]
            except IndexError:
                entry = " "
            line += entry + "  "
        lines.append(line)
    cs += "\n".join(lines)

    return cs


def get_longest_category_length(categories):
    length = 0
    for category in categories:
        mine = len(category.category.strip())
        if mine > length:
            length = mine
    return length
