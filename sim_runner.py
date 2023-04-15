# sim_runner.py is for batch running the simulation.
from simulate import TicTacToeSimulator
from presenter import ResultsPresenter

class BatchRunner:
    def __init__(self):
        self.simulator = TicTacToeSimulator()
        self.presenter = ResultsPresenter()
    
    def __call__(self, episodes):  
        self.simulator(episodes)
        self.presenter()


if __name__ == '__main__':
    runner = BatchRunner()
    episodes = int(input(f'Enter the number of episodes to run: '))
    runner(episodes)
