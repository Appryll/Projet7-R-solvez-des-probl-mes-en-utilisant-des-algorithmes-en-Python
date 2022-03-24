import csv
import time
from rich.console import Console

CSV_FILE = 'tables/liste des actions.csv'  # bénéfice maximum de: 97.48 euros pour un coût de: 498.0 euros
# CSV_FILE = 'tables/dataset1_Python+P7.csv'  # bénéfice maximum de: 198.51 euros pour un coût de: 499.94 euros
# CSV_FILE = 'tables/dataset2_Python+P7.csv'  # bénéfice maximum de: 197.77 euros pour un coût de: 499.98 euros
COST_MAX = 500
console = Console()


class ListeOptimize:
    list_action = []

    def __init__(self, name, price, profit):
        self.price = price
        self.name = name
        self.profit = profit
        if price == 0:
            self.benefit = 0
        else:
            self.benefit = (price * profit) / 100

        # Calcule du ratio : Gain/prix
        if price == 0:
            self.rendement = 0
        else:
            self.rendement = self.benefit / self.price
        self.list_action.append(self)

    def __repr__(self):
        return self.name + " | Price: " + str(self.price) + "euros | Profit: " + str(self.profit) + "euros | " \
               "Rendement: " + str(self.rendement)


def read_file(file):
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            ListeOptimize(row['name'], float(row['price']), float(row['profit']))


def knapsack():
    sorted_list = sorted(ListeOptimize.list_action, key=lambda listeoptimise: listeoptimise.rendement, reverse=True)

    cost_total = 0
    total_benefit = 0
    liste_optimale_sad = []
    for el in sorted_list:
        if (cost_total + el.price) <= COST_MAX and (el.price > 0):
            liste_optimale_sad.append(el)
            cost_total += el.price
            total_benefit += (el.price * el.profit) / 100
        if cost_total >= COST_MAX:
            break
    console.print("La solution optimale est:" + "\n", style="magenta")
    for combi in liste_optimale_sad:
        print(combi)
    console.print("\n" + "qui vous laissent un bénéfice maximum de:", round(total_benefit, 2), "euros pour un coût de:",
                  round(cost_total, 2), "euros", style="magenta")


def main(file):
    start_time = time.time()

    read_file(file)
    knapsack()

    elapsed_time = time.time() - start_time
    console.print("\n" * 2 + "Le temps d'exécution était de:", round(elapsed_time, 2), "secondes",
                  style="italic yellow")


if __name__ == "__main__":
    main(CSV_FILE)
