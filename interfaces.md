# grep -r -e '^class ' -e 'def ' *.py

main.py:class BaseViewer:
main.py:    def __init__(self, game) -> None:
main.py:    def __call__(self) -> None:
main.py:    def ask_to_continue(self) -> bool:

main.py:class Console_Viewer(BaseViewer):
main.py:    def __init__(self, game) -> None:
main.py:    def __call__(self) -> None:
main.py:    def ask_for_move(self, player) -> int:
main.py:    def ask_to_continue(self) -> bool:
main.py:    def message(message) -> None:

main.py:class Simulation_Viewer(BaseViewer):
main.py:    def __call__(self) -> None:
main.py:    def ask_to_continue(self) -> bool:
main.py:    def message(self, message) -> None:
main.py:    def update(self, message) -> None:

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
players.py:    def __init__(self, player_ID, player_symbol, viewer, game, exploration_param=1.4, max_iterations=500):
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


plotter.py:    def autolabel(rects):


presenter.py:class ResultsPresenter:
presenter.py:    def __init__(self, results_file='results.json'):
presenter.py:    def __call__(self):
presenter.py:    def load_results(self):
presenter.py:    def display_results(self):


sim_runner.py:class BatchRunner:
sim_runner.py:    def __init__(self):
sim_runner.py:    def __call__(self, episodes):  

simulate.py:class TicTacToeSimulator:
simulate.py:    def __init__(self, grid_size=3, num_episodes=100):
simulate.py:    def __call__(self, num_episodes):
simulate.py:    def display_menu(self):
simulate.py:    def get_episodes(self, prompt):
simulate.py:    def get_player_assignment(self, prompt):
simulate.py:    def run_simulation(self):
simulate.py:    def return_results(self, x_player_class, o_player_class, avg_time_per_episode):
simulate.py:    def save_results_as_json(self, x_player_class, o_player_class, new_results):
simulate.py:    def run_pairwise_simulations(self, num_episodes):
simulate.py:    def simulate(self, x_class, o_class, num_episodes):