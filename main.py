#   main.py - Tic-Tac-Toe game 
#   Currently configured for 3x3 grid size with Human vs AI_Jack playmode.
#   AI_MCTS and AI_ML_template are not yet implemented...
import math
import random
from time import sleep

from typing import List


class BasePlayer:
    '''
    BasePlayer:     abstract class for all players (Human, AI_Jack, AI_MCTS, AI_ML_template...)
    
                    __init__(self, player)  - player is either 'X' or 'O'
                
                    __call__(self, game)    - returns the next move by the player
    '''
    def __init__(self, player) -> None:
        self.player = player
    
    def __call__(self, game):
        raise NotImplementedError('Subclasses must implement this method')


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
    
    @staticmethod
    def message(message) -> None:
        print(message)
        
    def ask_to_continue(self) -> bool:
        return True

    
class Console_Viewer(BaseViewer):
    def __call__(self) -> None:
        print()
        print(self.game) 
    
    def ask_for_move(self, player) -> int:
        while True:
            cell_input = input(f'{player} - Enter the cell number for your next move '
                   f'{self.game.get_valid_moves()} or "q" to quit: ')
            if cell_input == 'q':
                self.game.quit_game()
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


class Human(BasePlayer):
    def __init__(self, player) -> None:
        self.view = Console_Viewer(game)
        self.player = player

    def __call__(self, game) -> int:
        while True:
            cell_input = self.view.ask_for_move(self.player)
            if cell_input == 'q':
                game.quit_game()
                break
            try:
                cell = int(cell_input)
                if cell not in game.get_valid_moves():
                    game.message('Invalid move, try again')
                    continue
                else:
                    return cell
            except ValueError:
                game.message('Invalid move, try again')


class AI_Jack(BasePlayer):
    def __call__(self, game) -> int:  
        moves = game.get_valid_moves()
        if len(moves) == 0:
            game.message('AI_Jack: No valid moves!')
            return None
        if len(moves) == 1:
            game.message('AI_Jack: Last move, ' + str(moves[0]) + '!')
            return moves[0]
        # 1. AI_Jack: if there is a winning move, play it
        for move in moves:
            if game.is_winning_move(move, self.player):
                game.message('AI_Jack: Winning move, ' + str(move) + '!')
                return move
        # 2. AI_Jack: if there are blocking moves, play one from the set with the highest score_matrix
        blocking_moves = []
        for move in moves:
            if game.is_blocking_move(move, self.player):
                blocking_moves.append(move)
        if len(blocking_moves) > 0:
            max_score = 0
            best_moves = []
            for move in blocking_moves:
                x, y = game.get_cell_coords_by_label(move)
                score = game.score_matrix[x][y]
                if score > max_score:
                    max_score = score
                    best_moves = [move]
                elif score == max_score:
                    best_moves.append(move)
            game.message('AI_Jack: Blocking move, ' + str(move) + '!')
            return random.choice(best_moves)    
        # 3. AI_Jack: if there are no blocking moves, play a random move from the set with the highest score_matrix
        max_score = 0
        best_moves = []
        for move in moves:
            x, y = game.get_cell_coords_by_label(move)
            score = game.score_matrix[x][y]
            if score > max_score:
                max_score = score
                best_moves = [move]
            elif score == max_score:
                best_moves.append(move)
        move = random.choice(best_moves)
        game.message('AI_Jack: I\'ll try this, ' + str(move) + '!')
        return move


class AI_MCTS(BasePlayer):
    def __init__(self, player, num_simulations=50, exploration_param=1.4):
        super().__init__(player)
        self.num_simulations = num_simulations
        self.exploration_param = exploration_param

    def __call__(self, game):
        root = Node(game.copy())
        for _ in range(self.num_simulations):
            node = root
            while node.fully_expanded():
                node = node.best_child(self.exploration_param)
            if not node.game_state.is_winner("X") and not node.game_state.is_winner("O") and not node.game_state.is_draw():
                node = node.expand()
            result = node.rollout()
            node.backpropagate(result)
        best_child = root.best_child(0)
        return best_child.move


class AI_ML_template(BasePlayer):
    def __call__(self, game):
        # implement template for further AI_ML algorithms
        # e.g. AI_ML_SVM, AI_ML_NN, AI_ML_RL, etc.
        pass
    
    
class AI_Rando(BasePlayer):
    def __call__(self, game):
        move = random.choice(game.get_valid_moves())
        comments = ['AI_Rando: Thinking... thinking... thinking... I\'ll claim cell ' + str(move) + '! ', 
                    'AI_Rando: Thinking... thinking... I\'ll claim cell ' + str(move) + '! ',
                    'AI_Rando: Thinking... I\'ll claim cell ' + str(move) + '! ',
                    'AI_Rando: I\'ll claim cell ' + str(move) + '!', 
                    'AI_Rando: I\'ve got it, taking ' + str(move) + '! ',]
        game.message(random.choice(comments))
        return move
    
    
class Node:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0

    def add_child(self, child_node):
        self.children.append(child_node)

    def update(self, result):
        self.visits += 1
        self.wins += result

    def fully_expanded(self):
        return len(self.children) == len(self.game_state.get_valid_moves())

    def untried_moves(self):
        tried_moves = [child.move for child in self.children]
        return [move for move in self.game_state.get_valid_moves() if move not in tried_moves]

    def best_child(self, exploration_param):
        best_score = float('-inf')
        best_child = None
        for child in self.children:
            exploit = child.wins / child.visits
            explore = math.sqrt(math.log(self.visits) / child.visits)
            score = exploit + exploration_param * explore
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def rollout_policy(self, valid_moves):
        return random.choice(valid_moves)

    def rollout(self):
        current_rollout_state = self.game_state.copy()
        while not current_rollout_state.is_winner("X") and not current_rollout_state.is_winner("O") and not current_rollout_state.is_draw():
            possible_moves = current_rollout_state.get_valid_moves()
            action = self.rollout_policy(possible_moves)
            current_rollout_state.move(action, current_rollout_state.current_player)
        return current_rollout_state.game_result()

    def expand(self):
        untried_moves = self.untried_moves()
        move = random.choice(untried_moves)
        next_state = self.game_state.copy()
        next_state.move(move, next_state.current_player)
        child_node = Node(next_state, self, move)
        self.add_child(child_node)
        return child_node

    def backpropagate(self, result):
        self.update(result)
        if self.parent:
            self.parent.backpropagate(1 - result)
                

class TicTacToeGame:    
    '''
    class TicTacToeGame - the game board and state, including the current player, 
    and the 'score matrix' which is a tool used to evaluate each cell based on  
    its strategic value; for use by AIs.
    '''
    def __init__(self, grid_size) -> None:
        self.view = Console_Viewer(self)
        self.grid_size = grid_size
        self.board = self._generate_board()
        self.current_player = 'X' #  First player is X
        self.score_matrix = self._generate_score_matrix(grid_size)
        
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
        new_game = TicTacToeGame(self.grid_size)
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
    
    def play_game(self, p1, p2, viewer) -> None:
        '''
        The Tic-Tac-Toe game loop.
        '''
        if AI_ONLY_MODE:
            pause = TURN_PAUSE 
        else:
            pause = 0
        turn = 0
        while turn < self.grid_size ** 2:
            if self.current_player == 'X': 
                if not turn == 0:
                    sleep(pause)
                move = p1(self)
            else:
                sleep(pause) 
                move = p2(self)
            print(f"turn {turn + 1}: Player {self.current_player} played {move}")
            valid_move = self.move(move, self.current_player)
            if valid_move:
                turn += 1
                viewer()
                if self.is_winner('X'):
                    viewer.message('X wins!')
                elif self.is_winner('O'):
                    viewer.message('O wins!')
                elif self.is_draw():
                    viewer.message('Draw!')
            if self.is_winner('X') or self.is_winner('O') or self.is_draw():
                break   
        continue_playing = viewer.ask_to_continue()
        if not continue_playing:
            self.quit_game()
        else:
            self.board = self._generate_board()
            self.current_player = 'X'

    def quit_game(self) -> None:
        print("Quitting the game...")
        exit()

                    
#  TODO once there are more Controllers, have __main__ allow for Controller selection(s) [also applies to Viewer]
if __name__ == '__main__':
    #  Mostly as an excersize in making robust Python code, the grid can be any size, 
    #  but the strategies for larger boards do not improve, it only protracts the game.
    GRID_SIZE = 3

    #  Setup a generic Tic-Tac-Toe game on the console:
    game = TicTacToeGame(GRID_SIZE)
    this_viewer = Console_Viewer(game)
    
    AI_ONLY_MODE = False #  DEBUG: to allow for slowed-play while debugging
    TURN_PAUSE = 0.4     #  DEBUG: to allow for slowed-play while debugging
    
    #  Menu & Game loop:
    while True:
        this_viewer.message('Welcome to Tic-Tac-Toe! Play modes: ' + 
                            '\n\tHuman play modes:' +
                            '\n\t1. Human as X vs. AI_Jack as O' + 
                            '\n\t2. AI_Jack as X vs. Human as O' +
                            '\n\t3. Human as X vs. AI_Rando as O' + 
                            '\n\tAI vs. AI modes:' +
                            '\n\t4. AI_Rando as X vs. AI_Jack as O' +
                            '\n\t5. AI_Jack as X vs. AI_Rando as O' +
                            '\n\t6. AI_Jack as X vs. AI_MCTS as O' +
                            '\n\tq. Quit')
        mode = input("Select a play mode or enter 'q' to quit: ")
        if bool(mode.strip() == '1'):                           #  play Human vs AI_Jack
            AI_ONLY_MODE = False
            game.play_game(Human('X'), AI_Jack('O'), this_viewer)       
        elif bool(mode.strip() == '2'):                         #  play AI_Jack vs Human
            AI_ONLY_MODE = False
            game.play_game(AI_Jack('X'), Human('O'), this_viewer)
        elif bool(mode.strip() == '3'):                         #  play Human vs AI_Rando
            AI_ONLY_MODE = False
            game.play_game(Human('X'), AI_Rando('O'), this_viewer)
        elif bool(mode.strip() == '4'):                         #  play AI_Rando vs AI_Jack
            AI_ONLY_MODE = True
            game.play_game(AI_Rando('X'), AI_Jack('O'), this_viewer)      
        elif bool(mode.strip() == '5'):                         #  play AI_Jack vs AI_Rando
            AI_ONLY_MODE = True
            game.play_game(AI_Jack('X'), AI_Rando('O'), this_viewer)   
        elif bool(mode.strip() == '6'):                         #  play AI_Jack vs AI_MCTS 
            AI_ONLY_MODE = True
            game.play_game(AI_Jack('X'), AI_MCTS('O'), this_viewer)     
        elif bool(mode.strip().lower() == 'q'):
            game.quit_game()
        else:
            this_viewer.message('Invalid input, try again')
            continue 
    