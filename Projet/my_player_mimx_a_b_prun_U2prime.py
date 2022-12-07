#!/usr/bin/env python3
"""
Avalam agent.
Copyright (C) 2022, <<<<<<<<<<< YOUR NAMES HERE >>>>>>>>>>>
Polytechnique Montréal

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
import random
from avalam import *
import numpy as np
import time

DEFAULT_PROF = 2
CONST_MULT = 165
CONST_STEP_1 = 1.4 / 12
CONST_STEP_2 = 1 / 12


class MyAgent(Agent):
    """My Avalam agent."""

    def play(self, percepts, player, step, time_left):

        print("player:", player, "step:", step, "time left:", time_left if time_left else '+inf')
        board = dict_to_board(percepts)

        def time_limit(step_arg):
            if step_arg <= 26:
                return 1.45*(20 + 170*(1 / (2*(np.sqrt(15 * np.pi)))) * (np.exp((-1 / 2) * (step_arg-20) * (step_arg-20)/(15*15))))
            else:
                return 1.45*31

        def utility_2(board_arg):
            board_clone = board_arg.clone()
            rows = board_clone.rows
            columns = board_clone.columns
            positives_tower_score = 0
            negatives_tower_score = 0
            for row in range(0, rows, 1):
                for column in range(0, columns, 1):
                    # Partie d'Heuristique qui permet de compter le score actuel par tour
                    tower_score = board_clone.m[row][column]
                    if tower_score != 0:
                        if tower_score > 0:
                            positives_tower_score += tower_score
                        elif tower_score < 0:
                            negatives_tower_score += tower_score
                    # Partie d'Heuristique qui permet de ne pas laisser une tour completable ( de 2, 3 et 4 vers 5 ) par l'adversaire
                    # au prochain tour, et qui minimise le score si c'est le cas. Attention minimisation des 10, à modifier eventuellement !
                    for score_incomplet in range(2, 4, 1):
                        if abs(tower_score) == score_incomplet:
                            for row_conv_1 in range(-1, 2, 1):
                                for column_conv_1 in range(-1, 2, 1):
                                    if row + row_conv_1 < 8 and row + row_conv_1 > 0 and column + column_conv_1 < 8 and column + column_conv_1 > 0:
                                        current_tower_score_check = board_clone.m[row + row_conv_1][
                                            column + column_conv_1]
                                        if (current_tower_score_check == 5 - score_incomplet):
                                            positives_tower_score += 10
                                            negatives_tower_score += 10
                                        elif (current_tower_score_check == -5 + score_incomplet):
                                            negatives_tower_score -= 10
                                            positives_tower_score -= 10
            if player > 0:
                return positives_tower_score
            elif player < 0:
                return negatives_tower_score

        def minimax_search(board_arg):
            alpha = -100000
            beta = 100000
            profondeur = 0
            start_time = time.time()
            current_step = step
            time_limit_to_play = time_limit(current_step)
            if player > 0:
                v, m = max_val(board_arg, time_limit_to_play, alpha, beta, start_time, profondeur)
            elif player < 0:
                v, m = min_val(board_arg, time_limit_to_play, alpha, beta, start_time, profondeur)
            return v, m

        def max_val(board_arg, time_lim, alpha, beta, start_t, profondeur):
            actions = list(board_arg.get_actions())
            time_left_to_play = min(time_lim, time_left)
            if player > 0:
                actions.reverse()
            if time.time() - start_t >= time_left_to_play and profondeur != 0:
                return utility_2(board_arg), None
            else:
                score_best_action = -10000
                best_action = None
                for action in actions:
                    board_arg_clone = board_arg.clone()
                    board_arg_clone.play_action(action)
                    score_intermediaire1, an_action = min_val(board_arg_clone, time_lim, alpha, beta, start_t,
                                                              profondeur + 1)
                    if score_intermediaire1 > score_best_action:
                        score_best_action = score_intermediaire1
                        best_action = action
                        alpha = max(alpha, score_best_action)
                    if (score_best_action >= beta):
                        return score_best_action, best_action  # pruning
                return score_best_action, best_action

        def min_val(board_arg, time_lim, alpha, beta, start_t, profondeur):
            actions = list(board_arg.get_actions())
            time_left_to_play = min(time_lim, time_left)
            if player < 0:
                actions.reverse()
            if time.time() - start_t >= time_left_to_play and profondeur != 0:
                return utility_2(board_arg), None
            else:
                score_best_action = 100000
                best_action = None
                for action in actions:
                    board_arg_clone = board_arg.clone()
                    board_arg_clone.play_action(action)
                    score_intermediaire1, an_action = max_val(board_arg_clone, time_lim, alpha, beta, start_t,
                                                              profondeur + 1)
                    if score_intermediaire1 < score_best_action:
                        score_best_action = score_intermediaire1
                        best_action = action
                        beta = min(beta, score_best_action)
                    if score_best_action <= alpha:
                        return score_best_action, best_action
                return score_best_action, best_action

        def predict_score(board_arg, action):
            board_clone = board_arg.clone()
            board_clone.play_action(action)
            return board_clone.m[action[2]][action[3]]

        if step == 1:
            print("Played_(1,1,1,2)")
            return 1, 1, 1, 2
        score_best_action, best_action = minimax_search(board)
        if best_action is None:
            actions = list(board.get_actions())
            order = [player * 5, player * 4, player * 3, player * 2, -player * 2, -player * 3, -player * 4, -player * 5]
            srt = {b: i for i, b in enumerate(order)}
            sorted_actions = sorted(actions, key=lambda a: srt[predict_score(board, a)])
            print("Played_Greedy")
            return sorted_actions[0]
        print("Played_Minimax")
        return best_action


if __name__ == "__main__":
    agent_main(MyAgent())
