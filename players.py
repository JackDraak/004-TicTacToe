# players.py - BasePlayer, Human, AI_Jack, AI_MCTS, AI_Rando...
import math
import random


class BasePlayer:
    '''
    BasePlayer: abstract class for all players (Human, AI_Rando, AI_Jack, AI_MCTS...)                                                
    '''
    def __init__(self, player_ID, player_symbol, viewer, game):
        self.name = player_ID
        self.player_symbol = player_symbol
        self.view = viewer
        self.game = game
    
    def __call__(self, game) -> int:
        raise NotImplementedError('Subclasses must implement this method')
    
    def __str__(self) -> str:
        return f'{self.player_symbol}'


class Human(BasePlayer):
    def __call__(self, game) -> int:
        while True:
            cell_input = self.view.ask_for_move(self.player_symbol)
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
            if game.is_winning_move(move, self.player_symbol):
                game.message('AI_Jack: Winning move, ' + str(move) + '!')
                return move
        # 2. AI_Jack: if there are blocking moves, play one from the set with the highest score_matrix
        blocking_moves = []
        for move in moves:
            if game.is_blocking_move(move, self.player_symbol):
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
    def __init__(self, player_ID, player_symbol, viewer, game, exploration_param=1.4, max_iterations=4000):
        super().__init__(player_ID, player_symbol, viewer, game)
        self.exploration_param = exploration_param
        self.max_iterations = max_iterations

    def __call__(self, game):
        self.root = Node(game)
        
        for _ in range(self.max_iterations):
            selected_node = self.tree_policy(self.root)
            result = selected_node.rollout()
            selected_node.backpropagate(result)

        best_child_node = self.root.best_child(0)  # exploitation only
        if best_child_node is not None:
            game.message(f'AI_MCTS: I\'ve calculated my move, taking {best_child_node.move}!')
            return best_child_node.move
        else:
            game.message('AI_MCTS: No valid moves!')
            return None

    def tree_policy(self, node):
        while not node.game_state.is_winner("X") and not node.game_state.is_winner("O") and not node.game_state.is_draw():
            if not node.fully_expanded():
                return node.expand()
            else:
                node = node.best_child(self.exploration_param)
        return node


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
        
        if current_rollout_state.is_winner(self.game_state.current_player):
            return 1
        elif current_rollout_state.is_winner("X" if self.game_state.current_player == "O" else "O"):
            return 0
        else:
            return 0.5  # draw

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
                