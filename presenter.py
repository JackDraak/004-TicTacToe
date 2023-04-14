# presenter.py - Presenter class for the Tic-Tac-Toe game simulation results.
import json
import os
import time

class ResultsPresenter:
    def __init__(self, results_file='results.json'):
        self.results_file = results_file
    
    def __call__(self):
        presenter = ResultsPresenter()
        presenter.load_results()
        presenter.display_results()

    def load_results(self):
        try:
            with open(self.results_file, 'r') as f:
                self.results = json.load(f)
        except FileNotFoundError:
            print(f"No results found in {self.results_file}")
            self.results = {}

    def display_results(self):
        if not self.results:
            print("No results to display")
            return
        mod_time = os.path.getmtime(self.results_file)
        print(f"\nResults from {self.results_file}: [Last modified time: {format(time.ctime(mod_time))}]\n")
        print("{:<30} {:^11} {:^11} {:^11} {:^11} {:^11}".format("", "X Wins", "O Wins", "Draws", "Total", "(W - L - D) time/match"))
        for key, result in self.results.items():
            sum = result['X'] + result['O'] + result['Draw']
            x_percent = "{:.1f}%".format((result['X'] / sum) * 100)
            o_percent = "{:.1f}%".format((result['O'] / sum) * 100)
            draw_percent = "{:.1f}%".format((result['Draw'] / sum) * 100)
            w_l_draw = f"({result['X']:<5} - {result['O']:<5} - {result['Draw']:<5})"
            average_time = "{:.5f}".format(result['Time']) # average_time = "{average_time:.3f}".format(result['Time'])
            print("{:<30} {:^11} {:^11} {:^11} {:^11} {:^11} {:<5}".format(key + ":", x_percent, o_percent, draw_percent, sum, w_l_draw, average_time))
        print()

# Usage example:
if __name__ == '__main__':
    presenter = ResultsPresenter()
    presenter.load_results()
    presenter.display_results()
