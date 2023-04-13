#  simulate.py
import main
import players
import itertools
from collections import defaultdict

def simulate_game(player1, player2):
    # Initialize the game
    game = main.TicTacToeGame(3, True)
    player1.game = game
    player2.game = game

    # Main game loop
    while not game.is_draw():
        if game.current_player == 'X':
            move = player1(game)
        else:
            move = player2(game)

        game.move(move, game.current_player)

    # Return the game outcome
    if game.is_draw():
        return 'Draw'
    else:
        return game.winner

def run_simulations(player1, player2, num_simulations):
    results = defaultdict(int)
    for _ in range(num_simulations):
        outcome = simulate_game(player1, player2)
        results[outcome] += 1
    return results

view = None
def assign_viewer(game):
    view = game.view
    
player_combinations = [
    (players.AI_Jack("Jack-X", "X", view, None), players.AI_Jack("Jack-O", "O", view, None)),
    (players.AI_MCTS("MCTS-X", "X", view, None), players.AI_MCTS("MCTS-O", "O", view, None)),
    (players.AI_Rando("Rando-X", "X", view, None), players.AI_Rando("Rando-O", "O", view, None))
]

num_simulations = 10  # Number of simulations to run for each player combination

# Run simulations for all possible player combinations
for player1, player2 in itertools.product(player_combinations, repeat=2):
    results = run_simulations(player1[0], player2[1], num_simulations)
    print(f"{player1[0].name} vs {player2[1].name}: {results}")

    
# player_list = [
#     (players.AI_Jack("Jack-X", "X", view, None), players.AI_Jack("Jack-O", "O", view, None)),
#     (players.AI_MCTS("MCTS-X", "X", view, None), players.AI_MCTS("MCTS-O", "O", view, None)),
#     (players.AI_Rando("Rando-X", "X", view, None), players.AI_Rando("Rando-O", "O", view, None))
# ]

# num_simulations = 10  # Number of simulations to run for each player combination
# results = defaultdict(int)

# # Run simulations for all possible player combinations
# for (player1_X, player1_O), (player2_X, player2_O) in itertools.product(player_list, repeat=2):
#     run_simulations(player1_X, player2_O, num_simulations, results)
#     print(f"{player1_X.name} vs {player2_O.name}: {results}")
#     results.clear()
