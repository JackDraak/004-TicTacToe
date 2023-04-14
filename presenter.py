import json

class ResultsPresenter:
    def __init__(self, results_file='results.json'):
        self.results_file = results_file

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

        print(f"Results from {self.results_file}:\n")
        for key, result in self.results.items():
            print(f"{key}:")
            print(f"  Player X wins: {result['X']}")
            print(f"  Player O wins: {result['O']}")
            print(f"  Draws: {result['Draw']}\n")

# Usage example:
if __name__ == '__main__':
    presenter = ResultsPresenter()
    presenter.load_results()
    presenter.display_results()
