class Category:

    def __init__(self, category):
        self.category = category
        self.ledger = list()
        self.balance = 0

    def check_funds(self, amount):
        if self.balance >= amount:
            return True
        else:
            return False

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
        self.balance += amount

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            self.balance -= amount
            return True
        else:
            return False

    def get_balance(self):
        return self.balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, description=f"Transfer to {category.category}")
            category.deposit(amount, description=f"Transfer from {self.category}")
            return True
        else:
            return False

    def __repr__(self):
        first_line = self.category.center(30, '*')
        items = [self.ledger[i]["description"][:23] + str(('%7.2f' % self.ledger[i]["amount"])[:7]).rjust(
            30 - len(self.ledger[i]["description"])) for i in range(len(self.ledger))]
        items_lines = "\n".join(items)
        total_line = "Total: " + str(self.balance)

        return first_line + '\n' + items_lines + '\n' + total_line

def create_spend_chart(categories):
    first_line = "Percentage spent by category"
    total_withdrawals = 0
    withdrawals_dic = dict()

    for category in categories:
        category_withdrawals = 0

        for item in category.ledger:
            if item['amount'] < 0:
                category_withdrawals += abs(item['amount'])

        total_withdrawals += category_withdrawals
        withdrawals_dic[category.category] = float('{:.2f}'.format(category_withdrawals))

    ratios = [withdrawals_dic[category.category] / total_withdrawals * 100 for category in categories]

    labels = list(range(0, 110, 10))
    labels.reverse()

    o_lines = ""
    for i in range(len(labels)):
        o_lines += (str(labels[i]) + '|').rjust(4) + " "

        for j in range(len(withdrawals_dic.keys())):
            if ratios[j] >= labels[i]:
                o_lines += "o  "
            else:
                o_lines += "   "

        o_lines += "\n"

    horizontal_line = " " * 4 + "-" * (3 * len(categories) + 1)
    longest_word = max([len(i) for i in withdrawals_dic.keys()])
    words = [i + " " * (longest_word - len(i)) for i in withdrawals_dic.keys()]

    words_lines = "     "
    for i in range(longest_word):
        for word in words:
            words_lines = words_lines + word[i] + '  '
        words_lines = words_lines + '\n     '

    return first_line + '\n' + o_lines + horizontal_line + '\n' + words_lines[:-6]
