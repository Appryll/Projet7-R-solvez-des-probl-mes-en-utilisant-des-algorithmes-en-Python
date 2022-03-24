import pandas as pd
from rich.console import Console
import time

# Le principe est simple : il faut étudier tous les cas possibles. Ainsi, pour appliquer cette stratégie, il faut :
# d'abord énumérer toutes les combinaisons possibles des actions
# puis conserver celles dont la capacité maximale n'est pas dépassée
# enfin, trouver la meilleure solution parmi les combinaisons restantes

# Liste des actions
start_time = time.time()
df_actions = pd.read_csv('tables/liste des actions.csv')
# Liste prix et nom des actions
df_actions_prix = (df_actions['price'])
df_actions_nom = df_actions['name']

# calculer profit
profit_actions = df_actions['price'] * df_actions['profit'] / 100
# print(profit_actions)

n = len(df_actions)  # nombre des actions = 20

tab_entiers = [i for i in range(2 ** n)]  # création d'un tableau avec tous les entiers entre 0 et 2**n-1

tab_binaire = [bin(i)[2:] for i in
               tab_entiers]  # conversion binaire des entiers du tableau précédent, le [2:] permet de supprimer les
# caractères de tête '0b' renvoyés par la fonction bin

combinaisons = ['0' * (n - len(k)) + k for k in
                tab_binaire]  # ajout des zéros pour obtenir des mots binaires de longueur n  = (11111111000011110100)
nc = len(combinaisons)  # 1 048 576 = 2 (soit 0 soit 1) ** 20

# combinaisons possibles prix total = 500 euros
prix_max = 500
combinaisons_valides = []

for combi in combinaisons:  # on parcourt chaque combinaison du tableau combinaisons
    prix_combi = 0
    profit_combi = 0
    for i in range(n):  # on parcourt la combinaison caractère par caractère
        # si le caractère est '1', alors on met à jour le prix et le profit de la combinaison
        if combi[i] == '1':
            prix_combi = prix_combi + df_actions_prix[i]
            profit_combi = profit_combi + profit_actions[i]

    # si la combi est valide alors on ajoute le couple (combi, profit_combi) à notre liste de combinaisons valides
    if prix_combi <= prix_max:
        combinaisons_valides.append((combi, profit_combi))  # 813 347 combinaisons_valides

# algorithme recherche de maximum: on parcur le tableau element par element et a chaque fois on compare à notre maximum
# temporaire et si on le trouve, on modifie on metre a jour notre maximum provisoire.
# il faut toujojurs initialiser le maximale temporaire et on l'initialise au prémier element du tableau

solution_optimale = combinaisons_valides[0][0]
profit_max = combinaisons_valides[0][1]

for combi in combinaisons_valides:
    if combi[1] > profit_max:
        profit_max = combi[1]
        solution_optimale = combi[0]

# liste optimale
liste_optimale_nom = []
for i in range(len(solution_optimale)):
    if solution_optimale[i] == '1':
        liste_optimale_nom.append(df_actions_nom[i])

liste_optimale_prix = []
for i in range(len(solution_optimale)):
    if solution_optimale[i] == '1':
        liste_optimale_prix.append(df_actions_prix[i])
prix_optimale = sum(liste_optimale_prix)

console = Console()

console.print("Liste suggérée avec les actions les plus rentables:" + "\n",
              ','.join(map(str, liste_optimale_nom)), "\n" + "qui vous laissent un bénéfice maximum de:",
              round(profit_max, 2), "euros pour un coût de:", prix_optimale, "euros", style="magenta")

elapsed_time = time.time() - start_time
console.print("\n" * 2 + "Le temps d'exécution était de:", round(elapsed_time, 2), "secondes",  style="italic yellow")
