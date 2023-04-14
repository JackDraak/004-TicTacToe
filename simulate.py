import json 
import main
import players

class TicTacToeSimulator:
    def __init__(self, grid_size=3, num_episodes=100):
        self.grid_size = grid_size
        self.num_episodes = num_episodes
        self.player_classes = {
            'AI_Jack': players.AI_Jack,
            'AI_MCTS': players.AI_MCTS,
            'AI_Rando': players.AI_Rando,
        }
        self.results = {'X': 0, 'O': 0, 'Draw': 0}

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

    def run_simulation(self):
        self.display_menu()
        episodes_choice = self.get_episodes(f'Enter the number of episodes to run: ')
        if episodes_choice != self.num_episodes:
            self.num_episodes = episodes_choice
        x_choice = self.get_player_assignment('Choose the AI player for X (enter the corresponding number): ')
        o_choice = self.get_player_assignment('Choose the AI player for O (enter the corresponding number): ')
        x_player_class = self.player_classes[list(self.player_classes.keys())[x_choice - 1]]
        o_player_class = self.player_classes[list(self.player_classes.keys())[o_choice - 1]]
        for episode in range(self.num_episodes):
            viewer = main.Simulation_Viewer(main.TicTacToeGame)
            game = main.TicTacToeGame(grid_size=self.grid_size, simulation=True)
            x_player = x_player_class('X', 'X', viewer, game)
            o_player = o_player_class('O', 'O', viewer, game)
            result = game.play_game(x_player, o_player, viewer)
            self.results[result] += 1
        new_results = self.return_results(x_player_class, o_player_class)
        print(new_results)
        simulator.save_results_as_json(new_results)

    def return_results(self, x_player_class, o_player_class):
        return (f'Result: Player X ({x_player_class.__name__}) wins: {self.results["X"]}, ' + 
              f'vs. Player O ({o_player_class.__name__}) wins: {self.results["O"]}, Draws: {self.results["Draw"]}')

    def save_results_as_json(self, results):
        results_file = 'results.json'
        # First, if there are existing results in the json file, tabulate them
        try:
            with open(results_file, 'r') as f:
                existing_results = json.load(f) # existing_results is a dictionary
        except FileNotFoundError:
            existing_results = {}  # if there is no existing json file, create an empty dictionary
        # Second, integrate the new results into the json file  
        new_results = results.split(': ')
        new_results = new_results[1].split(', ')
        for result in new_results:
            result = result.split(' ')
            if result[0] in existing_results:
                existing_results[result[0]] += int(result[1])
            else:
                existing_results[result[0]] = int(result[1])
        # Third, save the new results to the json file
        with open(results_file, 'w') as f:
            json.dump(existing_results, f, indent=4) # indent=4 for readability


if __name__ == '__main__':
    simulator = TicTacToeSimulator()
    simulator.run_simulation()
