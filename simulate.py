# simulate.py is for running the simulation (interactively).
import datetime
import json 
import main
import players
from time import time

class TicTacToeSimulator:
    def __init__(self, grid_size=3, num_episodes=100):
        self.grid_size = grid_size
        self.num_episodes = num_episodes
        self.player_classes = {
            'AI_Jack': players.AI_Jack,
            'AI_MCTS': players.AI_MCTS,
            'AI_Rando': players.AI_Rando,}
        self.results = {'X': 0, 'O': 0, 'Draw': 0}

    # run the simulation for each pairing of players N times (incl A:A pairings)      
    def __call__(self, num_episodes):
        for player1 in self.player_classes.keys():
            for player2 in self.player_classes.keys():
                # print the current player pairing with timestamp, as a progress indicator:
                timestamp = datetime.datetime.now().strftime('%H:%M:%S:%f')[:-3]
                print(f'{timestamp} Running {num_episodes} episodes of {player1} vs {player2}...')
                time_begin = time()
                new_results = self.simulate(self.player_classes[player1], self.player_classes[player2], num_episodes)
                time_end = time()
                time_elapsed = time_end - time_begin
                avg_time_per_episode = (time_elapsed / num_episodes)
                new_results['Time'] = round(avg_time_per_episode, 6)
                self.save_results_as_json(self.player_classes[player1], self.player_classes[player2], new_results)

    def display_menu(self):
        print('Tic-Tac-Toe AI vs AI Simulator')
        print('--------------------------------')
        print(f'Available AI Players: ')
        for idx, player in enumerate(self.player_classes.keys(), start=1):
            print(f'{idx}. {player}')
        print('')
        
    def get_episodes(self, prompt):
        while True:
            try:
                choice = int(input(prompt))
                if 1 <= choice <= 10000: # arbitrary limit of simulation episodes
                    break
                else:
                    print('Invalid choice. Please choose a valid option.')
            except ValueError:
                print('Invalid input. Please enter a number.')
        return choice

    def get_player_assignment(self, prompt):
        while True:
            try:
                choice = int(input(prompt))
                if 1 <= choice <= len(self.player_classes):
                    break
                else:
                    print('Invalid choice. Please choose a valid option.')
            except ValueError:
                print('Invalid input. Please enter a number.')
        return choice
            
    def return_results(self, x_player_class, o_player_class, avg_time_per_episode):
        return {'matchup': f'Player X ({x_player_class.__name__}) vs. Player O ({o_player_class.__name__})',
            'X': self.results['X'],
            'O': self.results['O'],
            'Draw': self.results['Draw'],
            'Time': round(avg_time_per_episode, 6)}
    
    def run_pairwise_simulations(self, num_episodes):
        for i, (x_name, x_class) in enumerate(self.player_classes.items()):
            for j, (o_name, o_class) in enumerate(self.player_classes.items()):
                # include A-A matchups for the sake of completeness
                print(f"Running simulation: {x_name}(X) vs {o_name}(O)")
                time_begin = time()
                self.simulate(x_class, o_class, num_episodes) 
                time_end = time()
                time_elapsed = time_end - time_begin
                avg_time_per_episode = time_elapsed / num_episodes
                new_results = self.return_results(x_class, o_class, avg_time_per_episode)
                print(new_results) # one set of pairing episodes completed
                self.save_results_as_json(x_class, o_class, new_results)
                
    def run_simulation(self):
        self.display_menu()
        episodes_choice = self.get_episodes(f'Enter the number of episodes to run: ')
        if episodes_choice != self.num_episodes:
            self.num_episodes = episodes_choice
        x_choice = self.get_player_assignment('Choose the AI player for X (enter the corresponding number): ')
        o_choice = self.get_player_assignment('Choose the AI player for O (enter the corresponding number): ')
        x_player_class = self.player_classes[list(self.player_classes.keys())[x_choice - 1]]
        o_player_class = self.player_classes[list(self.player_classes.keys())[o_choice - 1]]
        time_begin = time()
        for _ in range(self.num_episodes):
            viewer = main.Simulation_Viewer(main.TicTacToeGame)
            game = main.TicTacToeGame(grid_size=self.grid_size, simulation=True)
            x_player = x_player_class('X', 'X', viewer, game)
            o_player = o_player_class('O', 'O', viewer, game)
            result = game.play_game(x_player, o_player, viewer)
            self.results[result] += 1
        time_end = time()
        time_elapsed = time_end - time_begin
        avg_time_per_episode = (time_elapsed / self.num_episodes)
        
        new_results = self.return_results(x_player_class, o_player_class, avg_time_per_episode)
        print(new_results) # episodes completed
        print(f"Average time per episode: {avg_time_per_episode} seconds")
        self.save_results_as_json(x_player_class, o_player_class, new_results)

    def save_results_as_json(self, x_player_class, o_player_class, new_results):
        results_file = 'results.json'
        # First, if there are existing results in the json file, tabulate them
        try:
            with open(results_file, 'r') as f:
                existing_results = json.load(f) # existing_results is a dictionary
        except FileNotFoundError:
            existing_results = {}
        # Second, integrate the new results into the json file
        key = f"{x_player_class.__name__}(X) vs. {o_player_class.__name__}(O)"
        if key not in existing_results:
            existing_results[key] = {"X": 0, "O": 0, "Draw": 0, "Time": 0}
        existing_results[key]["X"] += new_results["X"]
        existing_results[key]["O"] += new_results["O"]
        existing_results[key]["Draw"] += new_results["Draw"]
        # Only keep time data for the most recent simulation so as AIs improve their 
        # performance, the time data will be updated apropriately
        existing_results[key]["Time"] = new_results["Time"] 
        with open(results_file, 'w') as f:
            json.dump(existing_results, f, indent=4)

    def simulate(self, x_class, o_class, num_episodes):
        results = {'X': 0, 'O': 0, 'Draw': 0}
        for _ in range(num_episodes):
            viewer = main.Simulation_Viewer(main.TicTacToeGame)
            game = main.TicTacToeGame(grid_size=self.grid_size, simulation=True)
            x_player = x_class('X', 'X', viewer, game)
            o_player = o_class('O', 'O', viewer, game)
            result = game.play_game(x_player, o_player, viewer)
            results[result] += 1
        return results


if __name__ == '__main__':
    simulator = TicTacToeSimulator()
    simulator.run_simulation()
