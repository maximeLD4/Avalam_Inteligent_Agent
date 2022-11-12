from avalam import *


class Node:
    def __init__(self, action, parent, board):
        self.action = action
        self.children = []
        self.parent = parent
        self.is_leaf = True
        self.U = 0
        self.N = 0
        self.board = board
        self.is_root = False
        if parent is not None:
            self.step_player = -self.parent.step_player
        else:
            self.step_player = 0

    def get_is_leaf(self):
        return self.is_leaf

    def get_u(self):
        return self.U

    def get_n(self):
        return self.N

    def incr_u(self, u):
        self.U += u

    def incr_n(self):
        self.N += 1

    def get_children(self):
        if self.children:
            return self.children
        return None

    #def set_child(self, action, parent, board):
    #    new_board = board.clone().play_action(action)
    #    node = Node(action, parent, new_board)
    #    self.children.append(node)
    #    self.is_leaf = False

    def set_child(self, node):
        self.children.append(node)
        self.is_leaf = False

    def get_info(self):
        print("U=", self.U, ", N=", self.N, ", action qui amene ici :", self.action)

    def get_board(self):
        return self.board.clone()

    def set_is_root(self, booleen):
        self.is_root = booleen

    def get_is_root(self):
        return self.is_root

    def get_parent(self):
        return self.parent

    def get_action(self):
        return self.action

    def get_step_player(self):
        return self.step_player

    def set_step_player(self, step):
        self.step_player = step
