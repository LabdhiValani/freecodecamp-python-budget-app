class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({
            'amount': amount,
            'description': description
        })

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({
                'amount': -amount,
                'description': description
            })
            return True
        return False

    def get_balance(self):
        balance = 0

        for item in self.ledger:
            balance += item['amount']

        return balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(
                amount,
                'Transfer to ' + category.name
            )

            category.deposit(
                amount,
                'Transfer from ' + self.name
            )

            return True

        return False

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        return True

    def __str__(self):
        result = self.name.center(30, '*') + '\n'

        for item in self.ledger:
            description = item['description'][:23]
            amount = f"{item['amount']:.2f}"

            result += f"{description:<23}{amount:>7}\n"

        result += f"Total: {self.get_balance():.2f}"

        return result


def create_spend_chart(categories):

    # Find total amount spent
    total_spent = 0

    for category in categories:
        for item in category.ledger:
            if item['amount'] < 0:
                total_spent += -item['amount']

    # Calculate spending percentage for each category
    percentages = []

    for category in categories:
        category_spent = 0

        for item in category.ledger:
            if item['amount'] < 0:
                category_spent += -item['amount']

        percentage = int(category_spent / total_spent * 100)
        percentage = (percentage // 10) * 10

        percentages.append(percentage)

    # Chart title
    chart = "Percentage spent by category\n"

    # Bars
    for level in range(100, -1, -10):
        chart += f"{level:>3}|"

        for percentage in percentages:
            if percentage >= level:
                chart += " o "
            else:
                chart += "   "

        chart += " \n"

    # Horizontal line
    chart += "    " + "-" * (3 * len(categories) + 1) + "\n"

    # Find longest category name
    max_length = 0

    for category in categories:
        if len(category.name) > max_length:
            max_length = len(category.name)

    # Category names vertically
    for i in range(max_length):
        chart += "     "

        for category in categories:
            if i < len(category.name):
                chart += category.name[i]
            else:
                chart += " "

            chart += "  "

        chart += "\n"

    # Remove ONLY the final newline.
    # Keep the required spaces at the end of each line.
    return chart[:-1]
