import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd

if __name__ == "__main__":
    game_log_time_J1 = "game_log_time_J1_1.csv"
    game_log_time_J2 = "game_log_time_J2_1.csv"
    results = pd.read_csv(game_log_time_J1)
    n_tot_ligne = len(results) + 1
    tab = []
    tab_x = []
    steps_J1 = [22, 24, 26, 28, 30, 32, 34]
    steps_J2 = [21, 23, 25, 27, 29, 31, 33, 35]
    steps_J1_1 = [29, 31, 33, 35, 37]
    steps_J2_1 = [28, 30, 32, 34, 36, 38]
    with open(game_log_time_J1, 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        output = []
        somme_1 = [0, 0, 0, 0, 0, 0, 0]
        n_tot = [0, 0, 0, 0, 0, 0, 0]
        somme_1_1 = [0, 0, 0, 0, 0]
        n_tot_1 = [0, 0, 0, 0, 0]
        for row in csvreader:
            output.append(row[:])
        for i in range(n_tot_ligne):
            for elmt in output[i]:
                if elmt != '':
                    tab.append(float(elmt))
            for k in range(len(tab)):
                somme_1_1[k] += tab[k]
                n_tot[k] += 1
            tab = []
        for j in range(len(somme_1_1)):
            somme_1_1[j] = somme_1_1[j]/n_tot[j]
        print(somme_1_1)

    results_2 = pd.read_csv(game_log_time_J2)
    n_tot_ligne_2 = len(results_2) + 1
    tab = []
    tab_x = []
    with open(game_log_time_J2, 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        output = []
        somme_2_1 = [0, 0, 0, 0, 0, 0]
        n_tot_1 = [0, 0, 0, 0, 0, 0]
        for row in csvreader:
            output.append(row[:])
        for i in range(n_tot_ligne):
            for elmt in output[i]:
                if elmt != '':
                    tab.append(float(elmt))
            for k in range(len(tab)):
                somme_2_1[k] += tab[k]
                n_tot[k] += 1
            tab = []
        for j in range(len(somme_2_1)):
            somme_2_1[j] = somme_2_1[j]/n_tot[j]
        print(somme_2_1)

        plt.xticks(np.arange(min(steps_J1_1), max(steps_J1_1)+2, 1.0))
        plt.yticks(np.arange(min(somme_2_1), max(somme_2_1)+1, 2.0))
        plt.title("temps de jeu du Joueur en fonction du step")
        plt.xlabel("step")
        plt.ylabel("temps de jeu du Joueur")
        plt.plot(steps_J1_1, somme_1_1, "-r", label="J1")
        plt.plot(steps_J2_1, somme_2_1, "-b", label="J2")
        plt.legend()
        plt.savefig("temps.png")
        plt.show()

