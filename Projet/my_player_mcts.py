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
from math import sqrt, log
from decimal import Decimal
import time

DEFAULT_PROF = 2


class MyAgent(Agent):
    """My Avalam agent."""

    def play(self, percepts, player, step, time_left):

        print("percept:", np.array(percepts))
        print("player:", player)
        print("step:", step)
        print("time left:", time_left if time_left else '+inf')
        start = time.time()
        board = dict_to_board(percepts)

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

        def select(root_node, start_time):
            current_node = root_node
            k = 1
            while not current_node.get_is_leaf():
                if time.time() - start_time >= 80:
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

        def expend(n, start_time):
            board_clone = n.get_board()
            if n.get_n() > 0 or n.get_is_root():
                if list(board_clone.get_actions()):
                    for action in list(board_clone.get_actions()):
                        if time.time() - start_time >= 80:
                            return False, n
                        node_child = Node(action, n, board_clone)
                        n.set_child(node_child)
                    return True, n.get_children()[0]
            return True, n

        def predict_score(board_game, action):
            board_clone = board_game.clone()
            board_clone.play_action(action)
            return board_clone.m[action[2]][action[3]]

        def simulate(n, start_time):
            clone_board = n.get_board()
            step_player = n.get_step_player()
            k = 1
            while not clone_board.is_finished():
                if time.time() - start_time >= 80:
                    return False, n
                actions = list(clone_board.get_actions())
                order = [step_player * 5, step_player * 4, step_player * 3, step_player * 2, -step_player * 2,
                         -step_player * 3, -step_player * 4, -step_player * 5]
                srt = {b: i for i, b in enumerate(order)}
                sorted_actions = sorted(actions, key=lambda a: srt[predict_score(clone_board, a)])
                action = sorted_actions[0]
                # action = random.choice(actions)
                clone_board = clone_board.play_action(action)
                step_player = -step_player
            score = get_score(clone_board)
            return True, score

        def backpropagation(v, n, start_time):
            current_node = n
            while not (current_node.get_is_root()):
                if time.time() - start_time >= 80:
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

        def mcts(board_game, start_time):
            board_clone = board_game.clone()
            root_node = Node(None, None, board_clone)
            root_node.set_is_root(True)
            root_node.set_step_player(player)
            emergence_root_node = root_node
            while time.time() - start_time <= 90:
                print("select")
                boolean, node_leaf = select(root_node, start_time)
                if not boolean:
                    return best_action(emergence_root_node)
                print("expend")
                boolean, node_child = expend(node_leaf, start_time)
                if not boolean:
                    return best_action(emergence_root_node)
                print("simulate")
                boolean, v = simulate(node_child, start_time)
                if not boolean:
                    return best_action(emergence_root_node)
                print("backpropagate")
                boolean, root_node = backpropagation(v, node_child, start_time)
                if not boolean:
                    return best_action(emergence_root_node)
                emergence_root_node = root_node
            return best_action(root_node)

        best_action = mcts(board, start)
        return best_action


if __name__ == "__main__":
    agent_main(MyAgent())
