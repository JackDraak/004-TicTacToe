main.py:class BaseViewer:
main.py:    def __init__(self, game) -> None:
main.py:    def __call__(self) -> None:
main.py:    def message(message) -> None:
main.py:    def ask_to_continue(self) -> bool:

main.py:class Console_Viewer(BaseViewer):
main.py:    def __call__(self) -> None:
main.py:    def ask_for_move(self, player) -> int:
main.py:    def ask_to_continue(self) -> bool:

main.py:class Simulation_Viewer(BaseViewer):
main.py:    def __call__(self) -> None:
main.py:    def ask_to_continue(self) -> bool:
main.py:    def update(self) -> None:

main.py:class TicTacToeGame:    
main.py:    def __init__(self, grid_size: int, simulation: bool) -> None:
main.py:    def __str__(self) -> str:
main.py:    def _count_claimed_cells_in_line(self, player, coords) -> int:
main.py:    def _generate_board(self):
main.py:    def _generate_score_matrix(self, grid_size) -> List[List[int]]:
main.py:    def copy(self):
main.py:    def get_cell_coords_by_label(self, cell_label):
main.py:    def get_valid_moves(self) -> List[int]:
main.py:    def is_blocking_move(self, cell, player) -> bool:
main.py:    def is_draw(self) -> bool:
main.py:    def is_winner(self, player) -> bool:
main.py:    def is_winning_move(self, cell, player) -> bool:
main.py:    def message(self, msg) -> None:
main.py:    def move(self, cell, player) -> bool:
main.py:    def play_game(self, p1, p2, viewer) -> str:
main.py:    def quit_game(self) -> None:
main.py:    def simulation_update(self, cell, player) -> None:

players.py:class BasePlayer:
players.py:    def __init__(self, player_ID, player_symbol, viewer, game):
players.py:    def __call__(self, game) -> int:
players.py:    def __str__(self) -> str:

players.py:class Human(BasePlayer):
players.py:    def __call__(self, game) -> int:

players.py:class AI_Jack(BasePlayer):
players.py:    def __call__(self, game) -> int:  

players.py:class AI_MCTS(BasePlayer):
players.py:    def __init__(self, player_ID, player_symbol, viewer, game, exploration_param=1.4, max_iterations=4000):
players.py:    def __call__(self, game):
players.py:    def tree_policy(self, node):

players.py:class AI_ML_template(BasePlayer):
players.py:    def __call__(self, game):

players.py:class AI_Rando(BasePlayer):
players.py:    def __call__(self, game):

players.py:class Node:
players.py:    def __init__(self, game_state, parent=None, move=None):
players.py:    def add_child(self, child_node):
players.py:    def update(self, result):
players.py:    def fully_expanded(self):
players.py:    def untried_moves(self):
players.py:    def best_child(self, exploration_param):
players.py:    def rollout_policy(self, valid_moves):
players.py:    def rollout(self):
players.py:    def expand(self):
players.py:    def backpropagate(self, result):

simulate.py:def simulate_game(player1, player2, viewer):
simulate.py:def run_simulations(player1, player2, num_simulations, results):