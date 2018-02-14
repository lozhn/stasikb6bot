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
