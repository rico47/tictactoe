from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Stan gry
# plansza: lista 9 elementów ('', 'X', 'O')
# aktualny_gracz: 'X' lub 'O'
# koniec_gry: True/False
game_state = {
    'board': ['', '', '', '', '', '', '', '', ''],
    'current_player': 'X',
    'game_over': False,
    'winner': None
}

# Kombinacje wygrywające
winning_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rzędy
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Kolumny
    [0, 4, 8], [2, 4, 6]              # Przekątne
]

def check_winner(board):
    for combo in winning_combinations:
        a, b, c = combo
        if board[a] and board[a] == board[b] and board[a] == board[c]:
            return board[a]
    return None

def check_draw(board):
    return all(cell != '' for cell in board)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset_game', methods=['POST'])
def reset_game():
    global game_state
    game_state = {
        'board': ['', '', '', '', '', '', '', '', ''],
        'current_player': 'X',
        'game_over': False,
        'winner': None
    }
    return jsonify(game_state)

@app.route('/make_move', methods=['POST'])
def make_move():
    global game_state
    if game_state['game_over']:
        return jsonify(game_state)

    data = request.get_json()
    cell_index = data['cell_index']

    if game_state['board'][cell_index] == '':
        game_state['board'][cell_index] = game_state['current_player']

        winner = check_winner(game_state['board'])
        if winner:
            game_state['winner'] = winner
            game_state['game_over'] = True
        elif check_draw(game_state['board']):
            game_state['game_over'] = True
            game_state['winner'] = 'Remis' # Ustawienie na 'Remis' dla rozróżnienia
        else:
            game_state['current_player'] = 'O' if game_state['current_player'] == 'X' else 'X'
    else:
        # Jeśli pole jest już zajęte, zwróć aktualny stan bez zmian
        pass

    return jsonify(game_state)

if __name__ == '__main__':
    app.run(debug=True)