<<<<<<< HEAD
import re
import random
from enum import Enum

games = {}


def xo_cmd(bot, update, args):
    player = update.message.chat.username
    games[player] = Game()

    update.message.reply_text(
        f"Your turn {player}:\n{games[player].pretty_field()}")


def xo_move(bot, update, args):
    def parse_move(move):
        letter, num = re.findall(r'([ABCDEFGHIJ])(\d{1,2})', move)[0]
        row = int(num) - 1
        col = ord(letter) - ord("A")
        return (row, col)

    def move_to_str(move):
        row, col = move
        return chr(col + ord("A")) + str(row + 1)

    def is_move(self, move):
        moves = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9',
                 'E10', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10', 'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10']
        return move in moves

    player = update.effective_message.chat.username
    if not games.get(player):
        game = games[player] = Game()
        update.message.reply_text(
            f"Your turn {player}:\n{game.pretty_field()}")

    game = games[player]
    text = args[0].upper()
    move = parse_move(text)
    is_empty = game.is_empty_cell(move)
    if not is_empty:
        update.message.reply_text(f"Move {text} has already done")
        return
    update.message.reply_text(f"Your move is {text}")

    move = game.move_player(move)
    result = game.get_result()
    if result:
        update.message.reply_text(result)
        update.message.reply_text(f"{game.pretty_field()}")
        games[player] = Game()
        return

    move = game.move_ai()
    result = game.get_result()
    if result:
        update.message.reply_text(result)
        update.message.reply_text(f"{game.pretty_field()}")
        games[player] = Game()
        return

    update.message.reply_text(f"AI move is {move_to_str(move)}")

    update.message.reply_text(f"Your turn {player}:\n{game.pretty_field()}")


class Player(Enum):
    HU = 1
    AI = 2


class Game:
    def __init__(self):
        self.win_length = 5
        self.field_size = 10
        self.field = [[0 for i in range(self.field_size)]
                      for i in range(self.field_size)]
        self.free_cells = self.field_size * self.field_size
        # typle ((row_start, col_start), (row_end, col_end))
        self.win_line = None
        self.player = None
        self.moves = dict()  # hash map of moves with theirs scores
        self.win_patterns = [
            r'0', r'(1{5})', r'(2{5})', r'([01]*7[01]*)', r'([02]*7[02]*)']
        self.patterns = [[], [], []]
        self.pre_pattern = [
            {'s': 'xxxxx', 'w': 99999},
            {'s': '0xxxx0', 'w': 7000},
            {'s': '0xxxx', 'w': 4000},
            {'s': 'xxxx0', 'w': 4000},
            {'s': '0x0xxx', 'w': 2000},
            {'s': '0xx0xx', 'w': 2000},
            {'s': '0xxx0x', 'w': 2000},
            {'s': 'xxx0x0', 'w': 2000},
            {'s': 'xx0xx0', 'w': 2000},
            {'s': 'x0xxx0', 'w': 2000},
            {'s': '0xxx0', 'w': 3000},
            {'s': '0xxx', 'w': 1500},
            {'s': 'xxx0', 'w': 1500},
            {'s': '0xx0x', 'w': 800},
            {'s': '0x0xx', 'w': 800},
            {'s': 'xx0x0', 'w': 800},
            {'s': 'x0xx0', 'w': 800},
            {'s': '0xx0', 'w': 200}
        ]

        for i, pat in enumerate(self.pre_pattern):
            s = pat['s']
            a = []
            pos = -1
            pos = s.find('x', pos + 1)
            while (pos != -1):
                a.append(s[0:pos] + '7' + s[pos + 1:])
                pos = s.find('x', pos + 1)
            s = '|'.join(a)

            self.patterns[0].append(self.pre_pattern[i]['w'])
            self.patterns[1].append(re.compile(s.replace(r'x', '1')))
            self.patterns[2].append(re.compile(s.replace(r'x', '2')))

    def pretty_field(self):
        sym = {1: "❌", 2: "⭕", 0: "⬜️"}
        res = ["A    B   C   D   E   F   G   H   I   J"]
        for i in range(self.field_size):
            line = []
            for s in self.field[i]:
                line.append(sym[s])
            line.append(str(i + 1))
            res.append(''.join(line))
        return '\n'.join(res)

    def is_over(self):
        return self.free_cells < 1 or self.win_line

    def is_empty_cell(self, move):
        row, col = move
        return self.field[row][col] == 0

    def get_result(self):
        if self.is_over():
            if not self.win_line:
                return 'It`s a DRAW'
            else:
                row, col = self.win_line[0]
                if self.field[row][col] == Player.HU.value:
                    return 'You win!'
                else:
                    return 'AI win!'
        return None

    def move_player(self, move):
        return self.move(move, Player.HU)

    def move_ai(self):
        self.score_moves()

        maximum = 0
        for row in self.moves.values():
            for col in row.values():
                maximum = max(col['sum'], maximum)

        best_moves = []
        for row in self.moves.keys():
            for col in self.moves[row].keys():
                if self.moves[row][col]['sum'] == maximum:
                    best_moves.append((row, col))

        move = best_moves[random.randint(0, len(best_moves) - 1)]
        return self.move(move, Player.AI)

    def move(self, move, player):
        row, col = move
        self.player = player

        if self.moves.get(row) and self.moves.get(row).get(col):
            del self.moves[row][col]

        self.field[row][col] = player.value
        self.free_cells -= 1

        self.win_line = self.check_win_line(move)

        if not self.is_over():
            self.update_possible_moves(move)

        return move

    def update_possible_moves(self, move):
        row, col = move

        for r in range(max(row - 2, 0), min(row + 3, self.field_size)):
            for c in range(max(col - 2, 0), min(col + 3, self.field_size)):
                if self.field[r][c] == 0:
                    if not self.moves.get(r):
                        self.moves[r] = {}
                    if not self.moves.get(r).get(c):
                        self.moves[r][c] = {
                            'sum': 0, 'attack': 0, 'defence': 0, 'attack_pattern': 0, 'defence_pattern': 0}
                    if self.player == Player.AI:
                        if abs(row - r) <= 1 and abs(col - c) <= 1:
                            self.moves[r][c]['attack'] += 10
                        else:
                            self.moves[r][c]['attack'] += 5
                    else:
                        if abs(row - r) <= 1 and abs(col - c) <= 1:
                            self.moves[r][c]['defence'] += 10
                        else:
                            self.moves[r][c]['defence'] += 5

    def check_win_line(self, move):
        row, col = move
        lines = ['', '', '', '']  # 4 directions \ - \ /

        rowT = min(row, 4)
        rowB = min(self.field_size - row - 1, 4)
        colL = min(col, 4)
        colR = min(self.field_size - col - 1, 4)

        for r in range(row - rowT, row + rowB + 1):
            lines[0] += str(self.field[r][col])
        for c in range(col - colL, col + colR + 1):
            lines[1] += str(self.field[row][c])
        for i in range(-min(rowT, colL), min(colR, rowB) + 1):
            lines[2] += str(self.field[row + i][col + i])
        for i in range(-min(rowB, colL), min(colR, rowT) + 1):
            lines[3] += str(self.field[row - i][col + i])

        win_pattern = str(self.player.value) * self.win_length

        for i in range(4):
            k = lines[i].find(win_pattern)
            if k >= 0:
                if i == 0:
                    return ((row - rowT + k, col), (row - rowT + k + 4, col))
                elif i == 1:
                    return ((row, col - colL + k), (row, col - colL + k + 4))
                elif i == 2:
                    return ((row - min(rowT, colL) + k, col - min(rowT, colL) + k), (row - min(rowT, colL) + k + 4, col - min(rowT, colL) + k + 4))
                elif i == 3:
                    return ((row + min(rowB, colL) - k, col - min(rowB, colL) + k), (row + min(rowB, colL) - k - 4, col - min(rowB, colL) + k + 4))

        return None

    def score_moves(self):
        for row in self.moves.keys():
            for col in self.moves[row].keys():
                self.moves[row][col]['sum'] = self.moves[row][col]['attack'] + \
                    self.moves[row][col]['defence']
                self.moves[row][col]['attack_pattern'] = 0
                self.moves[row][col]['defence_pattern'] = 0

                for q in range(1, 3):
                    for j in range(1, 5):
                        s = ''
                        for i in range(-4, 5):
                            if j == 1:
                                if row + i >= 0 and row + i < self.field_size:
                                    s += '7' if i == 0 else str(
                                        self.field[row + i][col])
                            elif j == 2:
                                if col + i >= 0 and col + i < self.field_size:
                                    s += '7' if i == 0 else str(
                                        self.field[row][col + i])
                            elif j == 3:
                                if row + i >= 0 and row + i < self.field_size:
                                    if col + i >= 0 and col + i < self.field_size:
                                        s += '7' if i == 0 else str(
                                            self.field[row + i][col + i])
                            elif j == 4:
                                if row - 1 >= 0 and row - i < self.field_size:
                                    if col + i >= 0 and col + i < self.field_size:
                                        s += '7' if i == 0 else str(
                                            self.field[row - i][col + i])

                        res = re.findall(self.win_patterns[Player.AI.value + 2], s) if q == 1 else re.findall(
                            self.win_patterns[Player.HU.value + 2], s)

                        if not res:
                            continue
                        if len(res[0]) < 5:
                            continue
                        if q == 1:
                            for i in range(len(self.patterns[2])):
                                if self.patterns[2][i].findall(s):
                                    self.moves[row][col]['attack_pattern'] += self.patterns[0][i]
                        else:
                            for i in range(len(self.patterns[1])):
                                if self.patterns[1][i].findall(s):
                                    self.moves[row][col]['defence_pattern'] += self.patterns[0][i]

                self.moves[row][col]['sum'] += 1.1 * self.moves[row][col]['attack_pattern'] + \
                    self.moves[row][col]['defence_pattern']
=======
from telegram.ext import BaseFilter
import re
from enum import Enum
from sys import maxsize
import time


SIZE = 10
WIN_LENGTH = 5
HU_PLAYER = 1
AI_PLAYER = -1

class XOFilter(BaseFilter):
  def filter(self, message):
    moves = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10', 'J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10']
    return message.text in moves

class State(Enum):
  NONE = "NONE"
  DRAW = "DRAW"
  WIN_X = "WIN_X"
  WIN_O = "WIN_O"

class Field:

  def __init__(self):
    self.moves = set()
    self.prev_moves = dict()
    self.field_size = SIZE
    self.win_length = WIN_LENGTH
    self.state = State.NONE
    self.hu_player = 1
    self.ai_player = -1
    self.field = [[0 for i in range(self.field_size)] for i in range(self.field_size)]

  def get_state(self):
    return self.state

  def pretty_field(self):
    sym = {1: "❌", -1: "⭕", 0: "⬜️"}
    res = ["A    B   C   D   E   F   G   H   I   J"]
    for i in range(self.field_size):
      line = []
      for s in self.field[i]:
        line.append(sym[s])
      line.append(str(i + 1))
      res.append(''.join(line))
    return '\n'.join(res)

  def is_game_over(self):
    return self.state != State.NONE

  def get_winner(self):
    return self.hu_player if self.state == State.WIN_X else self.ai_player if self.state == State.WIN_O else 0

  def is_full(self):
    for row in range(self.field_size):
      for col in range(self.field_size):
        if self.field[row][col] == 0:
          return False
    return True

  def is_empty(self, row, col):
    return self.field[row][col] == 0

  def get_neighbor_moves(self, row, col):
    mvs = []
    row_ = row - 1 if row > 0 else 0
    while(row_ < self.field_size and row_ < row + 2):
      col_ = col - 1 if col > 0 else 0
      while (col_ < self.field_size and col_ < col + 2):
        if self.field[row_][col_] == 0:
          mvs.append((row_, col_))
        col_ += 1
      row_ += 1

    return mvs

  def get_moves(self):
    return list(self.moves)

  def move(self, row, col, player):
    if self.field[row][col] != 0:
      return
    
    self.field[row][col] = player
    mvs = []
    ngbrs = self.get_neighbor_moves(row, col)
    for move in ngbrs:
      if (move not in self.moves):
        self.moves.add(move)
        mvs.append(move)
    self.prev_moves[str((row, col))] = mvs
    if (row, col) in self.moves:
      self.moves.remove((row, col))
    
    self.update_state()

  def undo_move(self, row, col):
    self.field[row][col] = 0
    self.state = State.NONE
    mvs = self.prev_moves[str((row, col))]
    self.prev_moves.pop(str((row, col)))
    self.moves.difference_update(set(mvs))
    self.moves.add((row, col))

  def update_state(self):
    line = self.get_win_line()
    if line:
      row, col = line[0]
      if self.field[row][col] == self.hu_player:
        self.state = State.WIN_X
      elif self.field[row][col] == self.ai_player:
        self.state = State.WIN_O
    elif self.is_full():
      self.state = State.DRAW

  def get_win_line(self):
    res = self.scan_rows()
    if ((res != None) and (len(res) >= self.win_length)):
      return res;
    res = self.scan_cols()
    if ((res != None) and (len(res) >= self.win_length)):
      return res;
    res = self.scan_diags()
    if ((res != None) and (len(res) >= self.win_length)):
      return res;

    return None

  def scan_rows(self):
    for i in range(self.field_size):
      line = self.scan_line(i, 0, 0, 1)
      if line:
        return line
    return None
  
  def scan_cols(self):
    for i in range(self.field_size):
      line = self.scan_line(0, i, 1, 0)
      if line:
        return line
    return None

  def scan_diags(self):
    for i in range(self.field_size):
      line = self.scan_up_diag(True, i)
      if line:
        return line
      line = self.scan_down_diag(True, i)
      if line:
        return line
      line = self.scan_up_diag(False, i)
      if line:
        return line
      line = self.scan_down_diag(False, i)
      if line:
        return line
    
    return None

  def scan_up_diag(self, direction, index):
    if direction:
      return self.scan_line(0, index, 1, 1)
    else:
      return self.scan_line(0, index, 1, -1)

  def scan_down_diag(self, direction, index):
    if direction:
      return self.scan_line(self.field_size - 1, index, -1, 1)
    else:
      return self.scan_line(self.field_size - 1, index, -1, -1)

  def scan_line(self, row, col, rInc, cInc):
    player = self.field[row][col]
    line = []

    while((row >= 0) and (row < self.field_size) and (col >= 0) and (col < self.field_size)):
      if (self.field[row][col] == 0):
        line = []
      elif (self.field[row][col] == player):
        line.append((row, col))
        if (len(line) >= self.win_length):
          return line
      else:
        player = self.field[row][col]
        line = []
        line.append((row, col))
      row += rInc
      col += cInc

    return None


class Game:
  
  def __init__(self):
    self.field = Field()
    self.max_depth = 3
  
  def pretty_field(self):
    return self.field.pretty_field()

  def get_winner(self):
    return self.field.get_winner()

  def new_game(self):
    self.field = Field()

  def is_game_over(self):
    return self.field.is_game_over()

  def is_empty_cell(self, row, col):
    return self.field.is_empty(row, col)

  def get_best_move(self):
    moves = self.field.get_moves()
    max_score = -maxsize
    best_move = None
    for move in moves:
      row, col = move
      self.field.move(row, col, AI_PLAYER)
      score = self.minimax(self.field, HU_PLAYER, 0, -maxsize, maxsize)
      self.field.undo_move(row, col)
      if score > max_score:
        max_score = score
        best_move = move

    return best_move


  def move_player(self, row, col):
    if self.field.is_game_over():
      return
    self.field.move(row, col, HU_PLAYER)
  
  def move_ai(self):
    if self.field.is_game_over():
      return None
    row, col = self.get_best_move()
    self.field.move(row, col, AI_PLAYER)
    return (row, col)
    
  def minimax(self, new_field, player, depth, alpha, beta):
    if new_field.get_state() == State.WIN_X:
      return depth -10
    elif new_field.get_state() == State.WIN_O:
      return 10 - depth
    elif new_field.get_state() == State.DRAW:
      return 2 - depth

    if depth == self.max_depth:
      return 0

    moves = new_field.get_moves()

    scores = []

    for move in moves:
      row, col = move
      self.field.move(row, col, player)
      res = self.minimax(new_field, -player, depth + 1, alpha, beta)
      self.field.undo_move(row, col)

    #   scores.append(res)

    # if player == HU_PLAYER:
    #   return min(scores)
    # else:
    #   return max(scores)

      if player == HU_PLAYER:
        if res < beta:
          beta = res
        if beta <= alpha:
          break
      else:
        if res > alpha:
          alpha = res
        if alpha >= beta:
          break
    if player == HU_PLAYER:
      return beta
    else:
      return alpha

games = {}

def xo_game(bot, update):
  player = update.message.chat.username
  games[player] = Game()

  field = games[player].pretty_field()
  update.message.reply_text(f"Your turn {player}:\n{field}")

def xo_move(bot, update):
  def parse_move(move):
    letter, num = re.findall(r'([ABCDEFGHIJ])(\d{1,2})', move)[0]
    row = int(num) - 1
    col = ord(letter) - ord("A")
    return (row, col)

  def move_to_str(move):
    row, col = move
    return chr(col + ord("A")) + str(row + 1)

  
  text = update.message.text
  player = update.effective_message.chat.username

  game = games[player]

  row, col = parse_move(text)
  is_empty = game.is_empty_cell(row, col)
  if not is_empty:
    update.message.reply_text(f"Move {text} has already done!")
    return 
  update.message.reply_text(f"Move {text}!")
  game.move_player(row, col)
  move = game.move_ai()
  if move:
    update.message.reply_text(f"AI move {move_to_str(move)}!")

  field = game.pretty_field()

  if game.is_game_over():
    winner = game.get_winner()
    if winner == HU_PLAYER:
      update.message.reply_text(f"You win!")
    elif winner == AI_PLAYER:
      update.message.reply_text(f"I win!")
    else:
      update.message.reply_text(f"Draw!")
    update.message.reply_text(f"{field}")
    return game.new_game()

  update.message.reply_text(f"Your turn {player}:\n{field}")
>>>>>>> 14b8720676c829c6cfe7324e293bee4bb2562469
