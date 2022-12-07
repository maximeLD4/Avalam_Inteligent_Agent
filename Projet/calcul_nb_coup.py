import numpy as np
import matplotlib.pyplot as plt
import csv

if __name__ == "__main__":
    game_log = "game_log_test.csv"
    tab = []
    tab_x = []
    with open(game_log, 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        output = []
        for row in csvreader:
            output.append(row[:])
        print(output[0])
        i = 0
        somme = 0
        for elmt in output[0]:
            nb = float(elmt.replace(',', '.'))
            somme += nb
            tab.append(nb)
            tab_x.append(i)
            i += 1
        print(tab)

    plt.title("Nombre moyen de coups possibles en fonction du step")
    plt.xlabel("step")
    plt.xticks(np.arange(min(tab_x), max(tab_x)+2, 2.0))
    plt.yticks(np.arange(min(tab), max(tab)+1, 40.0))
    plt.ylabel("Nombre moyen de coups possibles")
    plt.plot(tab)
    plt.savefig("N_moy_c_per_step.png")
    plt.show()

