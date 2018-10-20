#!/usr/bin/python

import sys
import json
import socket
import math

def get_move(player, board):
  result = minimax(player, board, 10, player)
  print('Move:', result)
  return [result[0][0], result[0][1]]

# Minimax
# Returns tuple (move, score)
def minimax(player, board, depth, current_player):
  # Maximize our players move
  maximizing_player = player == current_player
  # Get the valid moves
  valid_moves = get_valid_moves(current_player, board)

  # Base case
  if (not valid_moves or depth == 0):
      return ([0, 0], evalulate_board(board))

  best_move = [-1, -1]
  best_score = 0
  if maximizing_player:
    best_score = -math.inf
  else:
    best_score = math.inf

  print(valid_moves)
  # Recursive step
  if maximizing_player: # Me - maximize
    for move in valid_moves:
      board_copy = board.copy()
      make_move(current_player, board_copy, move)
      result = minimax(player, board_copy, depth - 1, get_opponent(current_player))
      if result[1] > best_score:
        best_move = move
        best_score = result[1]
  else: # Opponent - minimize
    for move in valid_moves:
      board_copy = board.copy()
      make_move(current_player, board_copy, move)
      result = minimax(player, board_copy, depth - 1, get_opponent(current_player))
      if result[1] < best_score:
        best_move = move
        best_score = result[1]

  # Return the best move and score that we found
  return (best_move, best_score)

def evalulate_board(board):
    return 0

def make_move(player, board, position):
  # Flip the tiles - need to optimize this
  for tile in is_valid_move(player, board, position[0], position[1]):
    board[tile[0]][tile[1]] = player
  # Set our tile
  board[position[0]][position[1]] = player

def on_board(x, y):
  return x >= 0 and x <= 7 and y >= 0 and y <= 7

def is_valid_move(player, board, x_start, y_start):
  # Check if move is even valid
  if not on_board(x_start, y_start) or board[x_start][y_start] != 0:
      return []

  tiles_to_flip = []
  for x_dir, y_dir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
    x = x_start + x_dir
    y = y_start + y_dir
    # While we are still on the board an opponent tiles
    while on_board(x, y) and board[x][y] == get_opponent(player):
      x += x_dir
      y += y_dir
      # If our next move is me, return the tiles to flip
      if on_board(x, y) and board[x][y] == player:
        # iterate back and add append to tiles_to_flip
        x -= x_dir
        y -= y_dir
        while not (x == x_start and y == y_start):
          tiles_to_flip.append([x, y])
          x -= x_dir
          y -= y_dir
        break

  return tiles_to_flip



def get_opponent(player):
  if player == 1:
      return 2
  return 1

def get_valid_moves(player, board):
  valid_moves = []

  for row in range(0, 8):
    for column in range(0, 8):
      if is_valid_move(player, board, row, column):
        valid_moves.append((row, column))
  return valid_moves










def prepare_response(move):
  response = '{}\n'.format(move).encode()
  print('sending {!r}'.format(response))
  return response

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect((host, port))
    while True:
      data = sock.recv(1024)
      if not data:
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8')))
      board = json_data['board']
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player']
      print(player, maxTurnTime, board)

      move = get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()
