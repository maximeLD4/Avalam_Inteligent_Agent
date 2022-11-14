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
from tree_node import Node
from math import sqrt, log, exp
from decimal import Decimal
import time

CONSTANTE_C = 12.2

# pour le joueur qui commence au tour 5
# 12.7*(sqrt(35)+sqrt(33)+sqrt(31)+sqrt(29)+sqrt(27)+sqrt(25)+sqrt(23)+sqrt(21)+sqrt(19)+sqrt(17)+sqrt(15)
# +sqrt(13)+sqrt(11)+sqrt(9)+sqrt(7)+sqrt(5)) < 900

# pour le joueur qui commence au tour 6
# 12.7*(sqrt(36)+sqrt(34)+sqrt(32)+sqrt(30)+sqrt(28)+sqrt(26)+sqrt(24)+sqrt(22)+sqrt(20)+sqrt(18)+sqrt(16)+sqrt(14)
# +sqrt(12)+sqrt(10)+sqrt(8)+sqrt(6)) < 900

class MyAgent(Agent):
    """My Avalam agent."""

    def play(self, percepts, player, step, time_left):

        print("percept:", np.array(percepts))
        print("player:", player)
        print("step:", step)
        print("time left:", time_left if time_left else '+inf')
        start = time.time()
        board = dict_to_board(percepts)

        def time_limit(x):
            return CONSTANTE_C * sqrt(x)

        def get_score(board_game):
            board_clone = board_game.clone()
            rows = board_clone.rows
            columns = board_clone.columns
            score_game = 0
            for row in range(0, rows, 1):
                for column in range(0, columns, 1):
                    tower_score = board_clone.m[row][column]
                    if tower_score != 0:
                        if tower_score > 0:
                            score_game += 1
                        elif tower_score < 0:
                            score_game -= 1
            return player * score_game

        def select(root_node, start_time, step_arg):
            current_node = root_node
            time_left_to_play = min(time_limit(step_arg), time_left)
            # time_lim(step) est toujours < timeleft sauf peut etre pour le dernier coup si jamais erreur dans
            # les calculs et en fait on a pris plus de temps que prévus ...
            while not current_node.get_is_leaf():
                if time.time() - start_time >= time_left_to_play:
                    return False, current_node
                if current_node.get_n() != 0 and current_node.get_children()[0].get_n() != 0:
                    u1 = Decimal(current_node.get_children()[0].get_u())
                    n1 = Decimal(current_node.get_children()[0].get_n())
                    log_n = Decimal(log(Decimal(current_node.get_n())))
                    u1_d_n1 = Decimal(u1 / n1)
                    sqrt_2_log_n_d_n1 = Decimal(sqrt(2 * log_n / n1))
                    max_ucb1 = u1_d_n1 + sqrt_2_log_n_d_n1

                else:
                    max_ucb1 = 0
                node_max_ucb1 = current_node.get_children()[0]
                for child in current_node.get_children():
                    if child.get_n() != 0 and current_node.get_n() != 0:
                        u1 = Decimal(child.get_u())
                        n1 = Decimal(child.get_n())
                        log_n = Decimal(log(Decimal(current_node.get_n())))
                        u1_d_n1 = Decimal(u1 / n1)
                        sqrt_2_log_n_d_n1 = Decimal(sqrt(2 * log_n / n1))
                        ucb1 = u1_d_n1 + sqrt_2_log_n_d_n1
                    else:
                        ucb1 = 0
                    if max_ucb1 <= ucb1:
                        max_ucb1 = ucb1
                        node_max_ucb1 = child
                    current_node = node_max_ucb1
            return True, current_node

        def expend(n, start_time, step_arg):
            board_clone = n.get_board()
            time_left_to_play = min(time_limit(step_arg), time_left)
            if n.get_n() > 0 or n.get_is_root():
                if list(board_clone.get_actions()):
                    for action in list(board_clone.get_actions()):
                        if time.time() - start_time >= time_left_to_play:
                            return False, n
                        node_child = Node(action, n, board_clone)
                        n.set_child(node_child)
                    return True, n.get_children()[0]
            return True, n

        def predict_score(board_game, action):
            board_clone = board_game.clone()
            board_clone.play_action(action)
            return board_clone.m[action[2]][action[3]]

        def simulate(n, start_time, step_arg):
            clone_board = n.get_board()
            step_player = n.get_step_player()
            time_left_to_play = min(time_limit(step_arg), time_left)
            while not clone_board.is_finished():
                if time.time() - start_time >= time_left_to_play:
                    return False, n
                actions = list(clone_board.get_actions())
                #order = [step_player * 5, step_player * 4, step_player * 3, step_player * 2, -step_player * 2,
                #         -step_player * 3, -step_player * 4, -step_player * 5]
                #srt = {b: i for i, b in enumerate(order)}
                #sorted_actions = sorted(actions, key=lambda a: srt[predict_score(clone_board, a)])
                #action = sorted_actions[0]
                action = random.choice(actions)
                clone_board = clone_board.play_action(action)
                #step_player = -step_player
            score = get_score(clone_board)
            return True, score

        def backpropagation(v, n, start_time, step_arg):
            current_node = n
            time_left_to_play = min(time_limit(step_arg), time_left)
            while not (current_node.get_is_root()):
                if time.time() - start_time >= time_left_to_play:
                    return False, current_node
                current_node.incr_u(v)
                current_node.incr_n()
                current_node = current_node.get_parent()
            current_node.incr_u(v)
            current_node.incr_n()
            return True, current_node

        def best_action(node):
            child_max_n = node.get_children()[0]
            max_n = node.get_children()[0].get_n()
            for child in node.get_children():
                n = child.get_n()
                if n >= max_n:
                    max_n = n
                    child_max_n = child
            return child_max_n.get_action()

        def mcts_middle(board_game, step_arg):
            board_clone = board_game.clone()
            root_node = Node(None, None, board_clone)
            root_node.set_is_root(True)
            root_node.set_step_player(player)
            emergence_root_node = root_node
            start_time = time.time()
            time_left_to_play = min(time_limit(step_arg), time_left)
            print("time_left_to_play : ", time_left_to_play)
            while time.time() - start_time <= time_left_to_play:
                boolean, node_leaf = select(root_node, start_time, step_arg)
                if not boolean:
                    return best_action(emergence_root_node)
                boolean, node_child = expend(node_leaf, start_time, step_arg)
                if not boolean:
                    return best_action(emergence_root_node)
                boolean, v = simulate(node_child, start_time, step_arg)
                if not boolean:
                    return best_action(emergence_root_node)
                boolean, root_node = backpropagation(v, node_child, start_time, step_arg)
                if not boolean:
                    return best_action(emergence_root_node)
                emergence_root_node = root_node
            return best_action(root_node)

        def mcts_end(board_game, step_arg):
            board_clone = board_game.clone()
            root_node = Node(None, None, board_clone)
            root_node.set_is_root(True)
            root_node.set_step_player(player)
            #emergence_root_node = root_node
            start_time = time.time()
            time_left_to_play = min(time_limit(step_arg), time_left)
            while time.time() - start_time <= time_left_to_play:
                boolean, node_leaf = select(root_node, start_time, step_arg)
                if not boolean:
                    return best_action(root_node)
                boolean, node_child = expend(node_leaf, start_time, step_arg)
                if not boolean:
                    return best_action(root_node)
                boolean, v = simulate(node_child, start_time, step_arg)
                if not boolean:
                    return best_action(root_node)
                boolean, root_node = backpropagation(v, node_child, start_time, step_arg)
                if not boolean:
                    return best_action(root_node)
                #semergence_root_node = root_node
            return best_action(root_node)

        def play_greedy(board_arg):
            actions = list(board_arg.get_actions())
            order = [player * 5, player * 4, player * 3, player * 2, -player * 2, -player * 3, -player * 4, -player * 5]
            srt = {b: i for i, b in enumerate(order)}
            sorted_actions = sorted(actions, key=lambda a: srt[predict_score(board_arg, a)])
            return sorted_actions[0]

        def expend_only_on_adv(n, start_time, step_arg):
            board_clone = n.get_board()
            time_left_to_play = min(sqrt(step_arg) * CONSTANTE_C, time_left)
            if n.get_n() > 0 or n.get_is_root():
                if list(board_clone.get_actions()):
                    for action in list(board_clone.get_actions()):
                        if time.time() - start_time >= time_left_to_play:
                            return False, n
                        if board_clone.m[action[2]][action[3]]*player < 0:
                            node_child = Node(action, n, board_clone)
                            n.set_child(node_child)
                    return True, n.get_children()[0]
            return True, n

        def gain_tower_move(board_arg):
            board_clone = board_arg.clone()
            rows = board_clone.rows
            columns = board_clone.columns
            row_ev, column_ev, row_i_ev, column_j_ev = 0, 0, 0, 0
            boolean = False
            for k in range(3, 5, 1):
                for row in range(0, rows, 1):
                    for column in range(0, columns, 1):
                        tower_score = board_clone.m[row][column]
                        if tower_score == -player * k:
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if ((j == 0 and i != 0) or (j != 0 or i == 0) or (j != 0 or i != 0)) and row + i < board_clone.rows and column + j < board_clone.columns and row + i > 0 and column + j > 0:
                                        # dans le meilleur des cas on recouvre par un élément de notre signe une tour du signe adverse
                                        if board_clone.m[row + i][column + j] == player * (5 - k):
                                            return (row + i, column + j, row, column), True
                                        # eventuellement sinon on essaye d'empecher l'adversaire de completer si lui il peut ...
                                        # elif (...)
                        elif tower_score == player * k:
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    if j != 0 and i != 0 and row + i < board_clone.rows and column + j < board_clone.columns and row + i > 0 and column + j > 0:
                                        # Au mieux ici on recouvre un élément du signe adverse
                                        if board_clone.m[row + i][column + j] == -player * (5 - k):
                                            return (row, column, row + i, column + j), True
                                        # dans le pire des cas on recouvre un élément de notre signe
                                        elif board_clone.m[row + i][column + j] == player * (5 - k):
                                            row_ev, column_ev, row_i_ev, column_j_ev = row, column, row + i, column + j
                                            boolean = True
            return (row_ev, column_ev, row_i_ev, column_j_ev), boolean

        action_gain_tower_move, boolean_gain_tower_move = gain_tower_move(board)

        # Si on peut completer/bloquer direct une tour on le fait sans "réfléchir"
        if boolean_gain_tower_move:
            action_to_play = action_gain_tower_move
        # les 3 4 premier step peuvent être fais intuitivement "au meilleur coup dispo" sans trop "réfléchir"
        elif step <= 4:
            action_to_play = play_greedy(board)
        # Sinon on procède a mcts
        # d'abord "mcts_middle" en millieu de partie, on cherche a ne jouer de sur des pions adverses
        #elif step <= 15:
        #    action_to_play = mcts_middle(board, step)
        # puis "mcts_end" en fin de partie, on cherche a jouer parmis tous les coups possibles
        else:
            action_to_play = mcts_end(board, step)
        return action_to_play


if __name__ == "__main__":
    agent_main(MyAgent())
