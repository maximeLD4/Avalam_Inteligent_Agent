import os
os.system('python random_player.py --bind 127.0.0.1 --port 8000')
os.system('python my_player_mcts_V1.py --bind 127.0.0.1 --port 8004')
os.system('python my_player_mcts_V2.py --bind 127.0.0.1 --port 8009')
os.system('python game.py http://localhost:8000 http://localhost:8080 --time 900 --verbose --no-gui')
