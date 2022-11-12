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

DEFAULT_PROF = 2


class MyAgent(Agent):
    """My Avalam agent."""

    def play(self, percepts, player, step, time_left):

        print("percept:", np.array(percepts))
        print("player:", player)
        print("step:", step)
        print("time left:", time_left if time_left else '+inf')
        board = dict_to_board(percepts)

        def utility_2(board):
            #compte seulement les points par tour
            board = board.clone()
            rows = board.rows
            columns = board.columns
            positives_tower_score_1 = 0
            positives_tower_score_2 = 0
            negatives_tower_score_1 = 0
            negatives_tower_score_2 = 0
            for row in range(0, rows, 1):
                for column in range(0, columns, 1):
                    tower_score = board.m[row][column]
                    if tower_score != 0:
                        #print(tower_score)
                        if tower_score > 0:
                            positives_tower_score_1 += tower_score
                            positives_tower_score_2 += tower_score/tower_score
                        elif tower_score < 0:
                            negatives_tower_score_1 += tower_score
                            negatives_tower_score_2 += tower_score/abs(tower_score)
            if player > 0:
                return positives_tower_score_2
            elif player < 0:
                return negatives_tower_score_2

        def minimax_search(board, profondeur=DEFAULT_PROF, alpha=-100000, beta=100000):
            if player > 0:
                v, m = max_val(board, profondeur, alpha, beta)
            elif player < 0:
                v, m = min_val(board, profondeur, alpha, beta)
            return v, m

        def max_val(board, profondeur, alpha, beta):
            actions = list(board.get_actions())
            if profondeur == 0:
                return utility_2(board), None
            else:
                score_best_action = -10000
                best_action = None
                for action in actions:
                    score_intermediaire0 = board.clone()
                    score_intermediaire0.play_action(action)
                    score_intermediaire1, an_action = min_val(score_intermediaire0, profondeur - 1, alpha, beta)
                    if score_intermediaire1 > score_best_action:
                        score_best_action = score_intermediaire1
                        best_action = action
                        alpha = max(alpha, score_best_action)
                    if (score_best_action >= beta):
                        return score_best_action, best_action #pruning
                return score_best_action, best_action

        def min_val(board, profondeur, alpha, beta):
            actions = list(board.get_actions())
            if profondeur == 0:
                return utility_2(board), None
            else:
                score_best_action = 100000
                best_action = None
                for action in actions:
                    score_intermediaire0 = board.clone()
                    score_intermediaire0.play_action(action)
                    score_intermediaire1, an_action = max_val(score_intermediaire0, profondeur - 1, alpha, beta)
                    if score_intermediaire1 < score_best_action:
                        score_best_action = score_intermediaire1
                        best_action = action
                        beta = min(beta, score_best_action)
                    if(score_best_action <= alpha):
                        return score_best_action, best_action
                return score_best_action, best_action

        score_best_action, best_action = minimax_search(board, 2)
        return best_action


if __name__ == "__main__":
    agent_main(MyAgent())
