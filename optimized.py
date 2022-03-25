import csv
import time
from rich.console import Console

# CSV_FILE = 'tables/liste des actions.csv'  # bénéfice maximum de: 97.48 euros pour un coût de: 498.0 euros
CSV_FILE = 'tables/dataset1_Python+P7.csv'  # profit maximum de: 197.09 euros pour un coût de: 499.99 euros.
# CSV_FILE = 'tables/dataset2_Python+P7.csv'  # bénéfice maximum de: 197.77 euros pour un coût de: 499.98 euros
COST_MAX = 500
console = Console()


class ListeOptimize:
    list_action = []

    def __init__(self, name, price, rendement):
        self.price = price
        self.name = name
        self.rendement = rendement  # % !! rendement * 100 / prix
        self.profit = round(rendement * price / 100, 2)  # EUROS !! profit * prix / 100

        self.list_action.append(self)

    def __repr__(self):
        return self.name + " | Price: " + str(self.price) + " euros | Rendement: " + str(self.rendement) + " % | " \
               "Profit: " + str(self.profit) + " euros "


def read_file(file):
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if float(row['price']) <= 0 or float(row['profit']) <= 0:
                pass
            else:
                ListeOptimize(row['name'], float(row['price']), float(row['profit']))


def knapsack():
    sorted_list = sorted(ListeOptimize.list_action, key=lambda listeoptimise: listeoptimise.profit, reverse=True)

    cost_total = 0
    total_profit = 0
    liste_optimale_sad = []

    for el in sorted_list:
        if (cost_total + el.price) <= COST_MAX:
            liste_optimale_sad.append(el)
            cost_total += el.price
            total_profit += el.profit
        if cost_total >= COST_MAX:
            break
    console.print("La solution optimale est:" + "\n", style="magenta")
    for combi in liste_optimale_sad:
        print(combi)
    console.print("\n" + "qui vous laissent un profit maximum de:", round(total_profit, 2), "euros pour un coût de:",
                  round(cost_total, 2), "euros.", style="magenta")


def main(file):
    start_time = time.time()

    read_file(file)
    knapsack()

    elapsed_time = time.time() - start_time
    console.print("\n" * 2 + "Le temps d'exécution était de:", round(elapsed_time, 2), "secondes",
                  style="italic yellow")


if __name__ == "__main__":
    main(CSV_FILE)
