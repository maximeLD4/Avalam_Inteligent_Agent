import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd

if __name__ == "__main__":
    game_log = "game_log.csv"
    results = pd.read_csv(game_log)
    n_tot_ligne = len(results) + 1
    tab = []
    tab_x = []
    with open(game_log, 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        output = []
        somme = 0
        for row in csvreader:
            output.append(row[:])
        for i in range(n_tot_ligne):
            for elmt in output[i]:
                if elmt != '':
                    tab.append(int(elmt.replace(',', '.')))
            somme += len(tab)
            tab = []
        print("moy de mouvement : ", somme/n_tot_ligne, " pour ", n_tot_ligne, " lignes")


