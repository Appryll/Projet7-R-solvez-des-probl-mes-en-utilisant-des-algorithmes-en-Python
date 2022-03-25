import pandas as pd
from rich.console import Console
import time


console = Console()
COST_MAX = 500
df_actions = pd.read_csv('tables/liste des actions.csv')
df_actions_prix = (df_actions['price'])
df_actions_nom = df_actions['name']
profit_actions = df_actions['price'] * df_actions['profit'] / 100
print(profit_actions)
n = len(df_actions)


def table_entiers():
    tab_entiers = [i for i in range(2 ** n)]
    tab_binaire = [bin(i)[2:] for i in tab_entiers]
    combinaisons = ['0' * (n - len(k)) + k for k in tab_binaire]
    return combinaisons


def knapsack():
    combinaisons = table_entiers()

    # combinaisons possibles prix total = 500 euros

    combinaisons_valides = []
    for combi in combinaisons:
        prix_combi = 0
        profit_combi = 0
        for i in range(n):
            if combi[i] == '1':
                prix_combi = prix_combi + df_actions_prix[i]
                profit_combi = profit_combi + profit_actions[i]
        if prix_combi <= COST_MAX:
            combinaisons_valides.append((combi, profit_combi))  # 813 347 combinaisons_valides
    return combinaisons_valides


def sol_optimale():
    combinaisons_valides = knapsack()
    solution_optimale = combinaisons_valides[0][0]  # initialiser l'algorithme
    profit_max = combinaisons_valides[0][1]  # initialiser le valeur profit

    # algorithme recherche de maximum
    for combi in combinaisons_valides:
        if combi[1] > profit_max:
            profit_max = combi[1]
            solution_optimale = combi[0]

    liste_optimale_nom = []
    for i in range(len(solution_optimale)):
        if solution_optimale[i] == '1':
            liste_optimale_nom.append(df_actions_nom[i])

    liste_optimale_prix = []
    for i in range(len(solution_optimale)):
        if solution_optimale[i] == '1':
            liste_optimale_prix.append(df_actions_prix[i])

    prix_optimale = sum(liste_optimale_prix)

    console.print("Liste suggérée avec les actions les plus rentables:" + "\n""\n",
                  ', '.join(map(str, liste_optimale_nom)), "\n""\n" + "qui vous laissent un profit maximum de:",
                  round(profit_max, 2), "euros pour un coût de:", prix_optimale, "euros", style="magenta")


def main():
    start_time = time.time()
    sol_optimale()
    elapsed_time = time.time() - start_time
    console.print("\n" * 2 + "Le temps d'exécution était de:", round(elapsed_time, 2), "secondes",
                  style="italic yellow")


if __name__ == "__main__":
    main()
