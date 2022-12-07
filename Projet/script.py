import os

if __name__ == "__main__":
    k = 0
    while k < 100:
        os.system("python game.py http://localhost:8104 http://localhost:8105 --time 900 --verbose --no-gui")
        k += 1
