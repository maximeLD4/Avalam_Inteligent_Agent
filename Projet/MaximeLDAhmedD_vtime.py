#!/usr/bin/env python3
"""
Avalam agent. LE MEILLEUR
Maxime LE DOEUFF 2234867, Ahmed DHAHIR - 2239705
Polytechnique Montréal
"""
import random
from avalam import *
import numpy as np
import time

CST_ADD = 20
CST_MULT_1 = 1.45
CST_MULT_2 = 170
STEP_CHANGE = 26
SIGMA = 15
MOY = 20
WEIGHT_0 = 10
WEIGHT_1 = 50
WEIGHT_2 = 100
MAX_STEP_PLAY_FAST = 15
BOARD_MAX_HEIGHT = 5
INF = 1000000000
THRESHOLD = 0


class MyAgent(Agent):
    """My Avalam agent."""

    def play(self, percepts, player, step, time_left):

        print("player:", player, "step:", step, "time left:", time_left if time_left else '+inf')
        board = dict_to_board(percepts)
        h = BOARD_MAX_HEIGHT

        def play_fast(board_arg):
            board_clone = board_arg.clone()
            rows = board_clone.rows
            columns = board_clone.columns
            row_ev, column_ev, row_i_ev, column_j_ev = 0, 0, 0, 0
            boolean = False
            for k in range(1, h, 1):  # board.max_height()
                for row in range(0, rows, 1):
                    for column in range(0, columns, 1):
                        tower_score = board_clone.m[row][column]
                        if tower_score == -player * k:
                            for i in range(-1, 2, 1):
                                for j in range(-1, 2, 1):
                                    if 0 < (row + i) < board_clone.rows and 0 < (column + j) < board_clone.columns:
                                        if board_clone.m[row + i][column + j] == player * (h - k):
                                            return (row + i, column + j, row, column), True
                        elif tower_score == player * k:
                            for i in range(-1, 2, 1):
                                for j in range(-1, 2, 1):
                                    if 0 < (row + i) < board_clone.rows and 0 < (column + j) < board_clone.columns:
                                        if board_clone.m[row + i][column + j] == player * (h - k):
                                            row_ev, column_ev, row_i_ev, column_j_ev = row + i, column + j, row, column
                                            boolean = True
            return (row_ev, column_ev, row_i_ev, column_j_ev), boolean

        def time_limit(step_arg):
            cst = 1.8
            if step_arg <= 29:
                return cst*(21.6 + 170*(1 / (2*(np.sqrt(15 * np.pi)))) * (np.exp((-1 / 2) * (step_arg-15) * (step_arg-15)/(20*20))))
            else:
                return 10

        def utility(board_arg):
            board_clone = board_arg.clone()
            rows = board_clone.rows
            columns = board_clone.columns
            score_tot = 0
            for row in range(0, rows, 1):
                for column in range(0, columns, 1):
                    # Partie d'Heuristique qui permet de compter le score actuel par tour
                    tower_score = board_clone.m[row][column]
                    if tower_score != 0:
                        if player * tower_score > 0:
                            score_tot += player * WEIGHT_0
                    # Strategy A (Imitation)
                    # Partie d'Heuristique qui permet de ne pas laisser une tour completable ( de +- 1,2,3 et 4 vers +-5 ) par l'adversaire
                    # au prochain tour, et qui minimise le score si c'est le cas. Attention minimisation des 10, à modifier eventuellement !
                    for score_incomplet in range(1, h, 1):
                        if abs(tower_score) == score_incomplet:
                            for row_conv_1 in range(-1, 2, 1):
                                for column_conv_1 in range(-1, 2, 1):
                                    if 8 > (row + row_conv_1) > 0 and 8 > (column + column_conv_1) > 0:
                                        current_tower_score_check = board_clone.m[row + row_conv_1][
                                            column + column_conv_1]
                                        if current_tower_score_check == -player * (
                                                h - score_incomplet) and tower_score == -player * score_incomplet:
                                            score_tot += -player * WEIGHT_1
                                            break
                                        elif current_tower_score_check == -player * (
                                                h - score_incomplet) and tower_score == player * score_incomplet:
                                            score_tot += -player * WEIGHT_2
                                            break
            return score_tot

        def minimax_search(board_arg):
            alpha = -INF
            beta = INF
            depth = 0
            start_time = time.time()
            current_step = step
            time_limit_to_play = time_limit(current_step)
            if player > 0:
                v, m = max_val(board_arg, time_limit_to_play, alpha, beta, start_time, depth)
            elif player < 0:
                v, m = min_val(board_arg, time_limit_to_play, alpha, beta, start_time, depth)
            return v, m

        def max_val(board_arg, time_lim, alpha, beta, start_t, depth):
            actions = list(board_arg.get_actions())
            random.shuffle(actions)
            time_left_to_play = min(time_lim, time_left)
            if player > 0:
                actions.reverse()
            if time.time() - start_t >= time_left_to_play and depth != 0:
                return utility(board_arg), None
            if not actions:
                return utility(board_arg), None
            else:
                score_best_action_max = -INF
                best_action_max = None
                for action in actions:
                    board_clone = board_arg.clone()
                    board_clone.play_action(action)
                    # Strategy B
                    if player * utility(board_clone) >= THRESHOLD:
                        score_intermediate, an_action = min_val(board_clone, time_lim, alpha, beta, start_t, depth + 1)
                        if score_intermediate > score_best_action_max:
                            score_best_action_max = score_intermediate
                            best_action_max = action
                            alpha = max(alpha, score_best_action_max)
                        if score_best_action_max >= beta:
                            return score_best_action_max, best_action_max  # pruning
                        if time.time() - start_t >= time_left_to_play and depth != 0 and best_action_max is not None:
                            return score_best_action_max, best_action_max
                return score_best_action_max, best_action_max

        def min_val(board_arg, time_lim, alpha, beta, start_t, depth):
            actions = list(board_arg.get_actions())
            random.shuffle(actions)
            time_left_to_play = min(time_lim, time_left)
            if player < 0:
                actions.reverse()
            # si time left
            if time.time() - start_t >= time_left_to_play and depth != 0:
                return utility(board_arg), None
            # ou si noeud terminal
            if not actions:
                return utility(board_arg), None
            else:
                score_best_action_min = INF
                best_action_min = None
                for action in actions:
                    board_clone = board_arg.clone()
                    board_clone.play_action(action)
                    # Strategy B
                    if player * utility(board_clone) >= THRESHOLD:
                        score_intermediate, an_action = max_val(board_clone, time_lim, alpha, beta, start_t, depth + 1)
                        if score_intermediate < score_best_action_min:
                            score_best_action_min = score_intermediate
                            best_action_min = action
                            beta = min(beta, score_best_action_min)
                        if score_best_action_min <= alpha:
                            return score_best_action_min, best_action_min
                        if time.time() - start_t >= time_left_to_play and depth != 0 and best_action_min is not None:  # AJOUT NEW
                            return score_best_action_min, best_action_min  # AJOUT NEW
                return score_best_action_min, best_action_min

        def predict_score(board_arg, action):
            board_clone = board_arg.clone()
            board_clone.play_action(action)
            return board_clone.m[action[2]][action[3]]

        # jeu direct au step 1, tout les coups sont équivalents)
        if step == 1:
            return 1, 1, 1, 2
        # si jamais on a une oportunitée simple (cela n'arrive pas si l'agent en face est vigilant)
        action_fast, bool_fast = play_fast(board)
        if bool_fast and step <= MAX_STEP_PLAY_FAST:
            return action_fast
        if step <= 20:
            actions = list(board.get_actions())
            return random.choice(actions)
        score_best_action, best_action = minimax_search(board)
        if best_action is None:  # filet dans le cas ou on a un dépassement de temps de jeu
            actions = list(board.get_actions())
            order = [player * 5, player * 4, player * 3, player * 2, -player * 2, -player * 3, -player * 4, -player * 5]
            srt = {b: i for i, b in enumerate(order)}
            sorted_actions = sorted(actions, key=lambda a: srt[predict_score(board, a)])
            return sorted_actions[0]
        return best_action


if __name__ == "__main__":
    agent_main(MyAgent())
