# sim_runner.py is for batch running the simulation.
from simulate import TicTacToeSimulator
from presenter import ResultsPresenter

if __name__ == '__main__':
    # get the number of episodes to run
    episodes = int(input(f'Enter the number of episodes to run: '))
    
    # run the simulation
    simulator = TicTacToeSimulator()
    simulator(episodes)

    # display the results
    presenter = ResultsPresenter()
    presenter()
