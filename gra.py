from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Stan gry - teraz globalny, ale będzie resetowany z nowym rozmiarem
game_state = {}

# Kombinacje wygrywające - będą generowane dynamicznie
winning_combinations = []

def generate_winning_combinations(size):
    combinations = []
    # Rzędy
    for i in range(size):
        combinations.append([i * size + j for j in range(size)])
    # Kolumny
    for j in range(size):
        combinations.append([i * size + j for i in range(size)])
    # Przekątne
    combinations.append([i * size + i for i in range(size)]) # Główna przekątna
    combinations.append([i * size + (size - 1 - i) for i in range(size)]) # Antyprzekątna
    return combinations

def initialize_game(board_size=3):
    global game_state, winning_combinations
    game_state = {
        'board': [''] * (board_size * board_size),
        'current_player': 'X',
        'game_over': False,
        'winner': None,
        'board_size': board_size
    }
    winning_combinations = generate_winning_combinations(board_size)
    print(f"Initialized game with board size: {board_size}") # Do debugowania
    return game_state

def check_winner(board, size):
    # Dynamicznie generujemy kombinacje wygrywające dla aktualnego rozmiaru planszy
    current_winning_combinations = generate_winning_combinations(size)
    for combo in current_winning_combinations:
        # Sprawdzamy, czy wszystkie komórki w kombinacji są takie same i niepuste
        first_cell_value = board[combo[0]]
        if first_cell_value and all(board[i] == first_cell_value for i in combo):
            return first_cell_value
    return None

def check_draw(board):
    return all(cell != '' for cell in board) and not game_state['winner']

@app.route('/')
def index():
    # Inicjalizujemy grę domyślnie z rozmiarem 3x3 przy pierwszym ładowaniu
    if not game_state: # Sprawdzamy, czy gra jest już zainicjowana
        initialize_game(3)
    return render_template('index.html', initial_game_state=game_state)

@app.route('/reset_game', methods=['POST'])
def reset_game():
    data = request.get_json()
    board_size = data.get('board_size', 3) # Pobierz rozmiar planszy z żądania POST, domyślnie 3
    initialize_game(board_size)
    return jsonify(game_state)

@app.route('/make_move', methods=['POST'])
def make_move():
    if game_state['game_over']:
        return jsonify(game_state)

    data = request.get_json()
    cell_index = data['cell_index']
    board_size = game_state['board_size'] # Pobierz rozmiar planszy z aktualnego stanu gry

    if 0 <= cell_index < len(game_state['board']) and game_state['board'][cell_index] == '':
        game_state['board'][cell_index] = game_state['current_player']

        winner = check_winner(game_state['board'], board_size)
        if winner:
            game_state['winner'] = winner
            game_state['game_over'] = True
        elif check_draw(game_state['board']):
            game_state['game_over'] = True
            game_state['winner'] = 'Remis'
        else:
            game_state['current_player'] = 'O' if game_state['current_player'] == 'X' else 'X'
    else:
        # Jeśli pole jest już zajęte lub indeks poza zakresem, zwróć aktualny stan bez zmian
        pass

    return jsonify(game_state)

if __name__ == '__main__':
    # Initializacja stanu gry przy starcie serwera, domyślnie 3x3
    initialize_game(3)
    app.run(debug=True)