


def matches_cmd(bot, update, args):
    pass


def matches_cb(bot, update, args):
    pass

init_state = 21



def round(state):
    if state == 1:
        return "You lose"

    print('-'*10)
    print(f'State: {state}')

    player_move = 0
    while player_move < 1 or player_move > 4:
        try:
            player_move = int(input('Your turn: '))
        except Exception as e:
            print('Choose 1 to 4 matches')

    state -= player_move

    ai_move = 5 - player_move
    print(f'Computer turn: {ai_move}')

    state -= ai_move
    print(f'{state} matches left')

    return round(state)

