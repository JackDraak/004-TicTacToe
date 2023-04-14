#   main.py - Tic-Tac-Toe game with 3 AI players and a console viewer (Human vs AI, or AI vs AI)
#
#   AI_Rando is a random AI player
#   AI_MCTS (WIP) is a Monte Carlo Tree Search AI player
#   AI_Jack is a minimax AI player
#   AI_ML_template (WIP) is a template for a machine learning AI player: AI_ML_SVM, AI_ML_NN, or AI_ML_RL...
#
#   To demo, run this file in a terminal: python main.py
#   To run the simulation, run this file in a terminal: python simulate.py
#
from players import Human, AI_Jack, AI_Rando, AI_MCTS
from time import sleep
from typing import List


class BaseViewer:
    '''
    BaseViewer:     abstract class for all viewers (Console_Viewer, GUI_Viewer, Web_Viewer...)
    
                    __init__(self, game)    - game is the TicTacToeGame object
                    
                    __call__(self)          - update the view of the game board state
                    
                    message(self, message)  - print a message to the user
    '''
    def __init__(self, game) -> None:
        self.game = game
    
    def __call__(self) -> None:
        raise NotImplementedError('Subclasses must implement this method')
    
    def ask_to_continue(self) -> bool:
        return True

    
class Console_Viewer(BaseViewer):
    def __init__(self, game) -> None:
        self.game = game
        
    def __call__(self) -> None:
        print()
        print(self.game) 
    
    def ask_for_move(self, player) -> int:
        while True:
            cell_input = input(f'{player} - Enter the cell number for your next move [{self.game.get_valid_moves()}] or "q" to quit: ')
            if cell_input == 'q':
                self.game.quit_game(game)
                break
            try:
                cell = int(cell_input)
                if cell not in self.game.get_valid_moves():
                    self.message('Invalid move, try again')
                    continue
                else:
                    return cell
            except ValueError:
                self.message('Invalid move, try again')
        
    def ask_to_continue(self) -> bool:
        while True:
            continue_playing = input('Continue playing? (Y/n): ')
            if continue_playing.strip().lower() == 'y' or continue_playing == '':
                return True
            elif continue_playing.strip().lower() == 'n':
                return False
            else:
                self.message('Invalid input, try again')
                continue
    
    @staticmethod
    def message(message) -> None:
        print(message)
                
            
class Simulation_Viewer(BaseViewer):
    def __call__(self) -> None:
        pass
        
    def ask_to_continue(self) -> bool:
        return True
    
    def message(self, message) -> None:
        pass
    
    def update(self, message) -> None:
        print(message)


class TicTacToeGame:    
    '''
    class TicTacToeGame - the game board and state, including the current player, 
    and the 'score matrix' which is a tool used to evaluate each cell based on  
    its strategic value; for use by AIs.
    '''
    def __init__(self, grid_size: int, simulation: bool) -> None:
        self.AI_ONLY_MODE = not simulation
        self.conclusion = str
        self.grid_size = grid_size
        self.score_matrix = self._generate_score_matrix(grid_size)
        self.board = self._generate_board()
        self.current_player = 'X' #  First player is X
        self.simulation = simulation
        if simulation:
            self.view = Simulation_Viewer(self)
        else:
            self.view = Console_Viewer(self)
        
    def __str__(self) -> str:
        board_with_labels = [[f'{(row_idx * self.grid_size) + col_idx + 1:3d}' if cell == ' ' else f'{cell:^3s}' for col_idx, cell in enumerate(row)] for row_idx, row in enumerate(self.board)]
        formatted_board = []
        for i, row in enumerate(board_with_labels):
            formatted_row = ' | '.join(row)
            if i < self.grid_size - 1:
                formatted_row += '\n' + '-' * (6 * game.grid_size - 3)
            formatted_board.append(formatted_row)
        return "\n".join(formatted_board)
    
    def _count_claimed_cells_in_line(self, player, coords) -> int:
        count = 0
        for x, y in coords:
            if self.board[x][y] == player:
                count += 1
        return count
    
    def _generate_board(self):
        return [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)]              
        
    def _generate_score_matrix(self, grid_size) -> List[List[int]]:
        '''
        Generate a score matrix for the game board, where the score is the number of ways to win from that cell.
        '''
        assert grid_size % 2 == 1, "Grid size should be odd, comment-out this line if you feel otherwise (and good luck!)"
        matrix = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        for row in range(grid_size):
            for col in range(grid_size):
                score = 2          
                if row == col and (row == 0 or row == grid_size - 1 or row == grid_size // 2):
                    score += 1
                if row + col == grid_size - 1 and (row == 0 or row == grid_size - 1 or row == grid_size // 2):
                    score += 1
                matrix[row][col] = score
        return matrix
    
    def copy(self):
        new_game = TicTacToeGame(self.grid_size, self.simulation)
        new_game.board = [row[:] for row in self.board]
        new_game.current_player = self.current_player
        return new_game

    def get_cell_coords_by_label(self, cell_label):
        x = (int(cell_label) - 1) // self.grid_size
        y = (int(cell_label) - 1) % self.grid_size
        return x, y

    def get_valid_moves(self) -> List[int]:
        moves = [row * self.grid_size + col + 
                 1 for row in range(self.grid_size) for col in range(self.grid_size) if self.board[row][col] == ' ']
        return moves
 
    def is_blocking_move(self, cell, player) -> bool:
        x, y = self.get_cell_coords_by_label(cell)
        opponent = 'X' if player == 'O' else 'O'
        lines = [[(x, col) for col in range(self.grid_size)],[(row, y) for row in range(self.grid_size)],]
        if x == y:
            lines.append([(i, i) for i in range(self.grid_size)])
        if x + y == self.grid_size - 1:
            lines.append([(i, self.grid_size - 1 - i) for i in range(self.grid_size)])
        for line in lines:
            if self._count_claimed_cells_in_line(opponent, line) == self.grid_size - 1 and self.board[x][y] == ' ':
                return True
        return False
 
    def is_draw(self) -> bool:
        return not (self.is_winner('X') or self.is_winner('O')) and all([cell != ' ' for row in self.board for cell in row])

    def is_winner(self, player) -> bool:
        lines = [[(row, col) for col in range(self.grid_size)] for row in range(self.grid_size)] + [[(row, col) for row in range(self.grid_size)] for col in range(self.grid_size)] + [[(i, i) for i in range(self.grid_size)], [(i, self.grid_size - 1 - i) for i in range(self.grid_size)],]
        for line in lines:
            if self._count_claimed_cells_in_line(player, line) == self.grid_size:
                return True
        return False
    
    def is_winning_move(self, cell, player) -> bool:
        x, y = self.get_cell_coords_by_label(cell)
        lines = [[(x, col) for col in range(self.grid_size)],[(row, y) for row in range(self.grid_size)],]
        if x == y:
            lines.append([(i, i) for i in range(self.grid_size)])
        if x + y == self.grid_size - 1:
            lines.append([(i, self.grid_size - 1 - i) for i in range(self.grid_size)])
        for line in lines:
            if self._count_claimed_cells_in_line(player, line) == self.grid_size - 1 and self.board[x][y] == ' ':
                return True
        return False
    
    def message(self, msg) -> None:
        self.view.message(msg)

    def move(self, cell, player) -> bool:
        '''
        Return True if move is valid (AND claim cell, AND swap player), else False
        '''
        if cell is None:
            return False
        x, y = self.get_cell_coords_by_label(cell)
        if self.board[x][y] == ' ':
            self.board[x][y] = player
            self.current_player = 'X' if player == 'O' else 'O'
            return True
        return False
    
    def play_game(self, p1, p2, viewer) -> str:
        '''
        The Tic-Tac-Toe game loop.
        '''
        if self.AI_ONLY_MODE:
            pause = TURN_PAUSE 
        else:
            pause = 0
                      
        turn = 0
        while turn < self.grid_size ** 2:
            if self.current_player == 'X': 
                if not turn == 0:
                    sleep(pause)
                move = p1(self)
                player_id = p1.name
            else:
                sleep(pause) 
                move = p2(self)
                player_id = p2.name
            viewer.message(f"turn {turn + 1}: Player {self.current_player} ({player_id}) played {move}")
            valid_move = self.move(move, self.current_player)
            if valid_move:
                turn += 1
                viewer()
                if self.is_winner('X'):
                    viewer.message(f'{self.current_player} ({p1.name}) wins!')
                    conclusion = 'X'
                elif self.is_winner('O'):
                    viewer.message(f'{self.current_player} ({p2.name}) wins!')
                    conclusion = 'O'
                elif self.is_draw():
                    viewer.message('Draw!')
                    conclusion = 'Draw'
            if self.is_winner('X') or self.is_winner('O') or self.is_draw():
                break   
                 
        if not self.simulation:
            continue_playing = viewer.ask_to_continue()
            if not continue_playing:
                self.quit_game()

        self.board = self._generate_board()
        self.current_player = 'X'    
        return conclusion

    def quit_game(self) -> None:
        print("Quitting the game...")
        exit()
        
    def simulation_update(self, cell, player) -> None:
        x, y = self.get_cell_coords_by_label(cell)
        self.board[x][y] = player
        self.current_player = 'X' if player == 'O' else 'O'

                    
#  TODO once there are more Controllers, have __main__ allow for Controller selection(s) [also applies to Viewer]
if __name__ == '__main__':
    #  Mostly as an excersize in making robust Python code, the grid can be any size, 
    #  but the strategies for larger boards do not improve, it only protracts the game.
    GRID_SIZE = 3

    #  Setup a generic Tic-Tac-Toe game on the console:
    this_viewer = Console_Viewer(TicTacToeGame)  
    game = TicTacToeGame(GRID_SIZE, simulation=False)
    this_viewer = Console_Viewer(game)
    
    AI_ONLY_MODE = False #  DEBUG: to allow for slowed-play while debugging
    TURN_PAUSE = 0.05     #  DEBUG: to allow for slowed-play while debugging
    
    #  Menu & Game loop:
    while True:
        this_viewer.message('Welcome to Tic-Tac-Toe! Play modes: ' + 
                            
                            '\n\tHuman play modes:' +
                            '\n\t1. Human as X vs. AI_Rando as O' + 
                            '\n\t2. Human as X vs. AI_MCTS as O' +
                            '\n\t3. Human as X vs. AI_Jack as O' + 
                            '\n\t4. AI_Jack as X vs. Human as O' +
                            
                            '\n\tAI vs. AI modes:' +
                            '\n\t5. AI_Rando as X vs. AI_Jack as O' +
                            '\n\t6. AI_MCTS as X vs. AI_Jack as O' +
                            '\n\t7. AI_Jack as X vs. AI_Rando as O' +
                            '\n\t8. AI_Jack as X vs. AI_MCTS as O' +
                            '\n\tq. Quit')
        
        mode = input("Select a play mode or enter 'q' to quit: ")
        AI_ONLY_MODE = False
        if bool(mode.strip() == '1'): #  play Human vs AI_Rando
            game.play_game(Human('Human', 'X', this_viewer, game), AI_Rando('AI_Rando', 'O', this_viewer, game), this_viewer) 
        elif bool(mode.strip() == '2'):   #  play Human vs AI_MCTS
            game.play_game(Human('Human', 'X', this_viewer, game), AI_MCTS('AI_MCTS', 'O', this_viewer, game), this_viewer)
        elif bool(mode.strip() == '3'): #  play Human vs AI_Jack
            game.play_game(Human('Human', 'X', this_viewer, game), AI_Jack('AI_Jack', 'O', this_viewer, game), this_viewer)       
        elif bool(mode.strip() == '4'): #  play AI_Jack vs Human
            game.play_game(AI_Jack('AI_Jack', 'X', this_viewer, game), Human('Human', 'O', this_viewer, game), this_viewer) 
        elif bool(mode.strip() == '5'): #  play AI_Rando vs AI_Jack
            AI_ONLY_MODE = True
            game.play_game(AI_Rando('AI_Rando', 'X', this_viewer, game), AI_Jack('AI_Jack', 'O', this_viewer, game), this_viewer)       
        elif bool(mode.strip() == '6'): #  play AI_MCTS vs AI_Jack
            AI_ONLY_MODE = True
            game.play_game(AI_MCTS('AI_MCTS', 'X', this_viewer, game), AI_Jack('AI_Jack', 'O', this_viewer, game), this_viewer)    
        elif bool(mode.strip() == '7'): #  play AI_Jack vs AI_Rando
            AI_ONLY_MODE = True
            game.play_game(AI_Jack('AI_Jack', 'X', this_viewer, game), AI_Rando('AI_Rando', 'O', this_viewer, game), this_viewer)   
        elif bool(mode.strip() == '8'): #  play AI_Jack vs AI_MCTS 
            AI_ONLY_MODE = True
            game.play_game(AI_Jack('AI_Jack', 'X', this_viewer, game), AI_MCTS('AI_MCTS', 'O', this_viewer, game), this_viewer)       
        elif bool(mode.strip().lower() == 'q'):
            game.quit_game()
        else:
            this_viewer.message('Invalid input, try again')
            continue 
    