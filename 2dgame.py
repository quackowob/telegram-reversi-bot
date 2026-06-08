import random

# 定義棋盤大小
BOARD_SIZE = 8

# 定義棋盤狀態
EMPTY = 0
BLACK = 1
WHITE = 2

# 定義棋子顏色
PLAYER_COLOR = BLACK
AI_COLOR = WHITE

# 創建棋盤
board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]

# 初始化棋盤
def initialize_board():
    mid = BOARD_SIZE // 2
    board[mid][mid] = WHITE
    board[mid - 1][mid - 1] = WHITE
    board[mid][mid - 1] = BLACK
    board[mid - 1][mid] = BLACK

# 顯示棋盤
def display_board():
    print("  ", end="")
    for i in range(BOARD_SIZE):
        print(chr(ord('a') + i), end=" ")
    print()
    for i in range(BOARD_SIZE):
        print(i + 1, end=" ")
        for j in range(BOARD_SIZE):
            if board[i][j] == EMPTY:
                print(".", end=" ")
            elif board[i][j] == BLACK:
                print("B", end=" ")
            else:
                print("W", end=" ")
        print()

# 檢查移動是否合法
def is_valid_move(row, col, color):
    if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE or board[row][col] != EMPTY:
        return False
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            if board[row][col] == EMPTY:
                r, c = row + dr, col + dc
                if r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE and board[r][c] != color and board[r][c] != EMPTY:
                    while r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE:
                        r += dr
                        c += dc
                        if r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE and board[r][c] == color:
                            return True
    return False

# 執行玩家移動
def make_player_move():
    while True:
        move = input("輸入你的下一步位置（例如：c4）：")
        if len(move) != 2 or not move[0].isalpha() or not move[1].isdigit():
            print("無效的輸入！請重新輸入。")
            continue
        col = ord(move[0].lower()) - ord('a')
        row = int(move[1]) - 1
        if is_valid_move(row, col, PLAYER_COLOR):
            flip_tiles(row, col, PLAYER_COLOR)
            break
        else:
            print("無效的移動！請重新輸入。")

# 執行AI移動
def make_ai_move():
    valid_moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if is_valid_move(row, col, AI_COLOR):
                valid_moves.append((row, col))
    if len(valid_moves) > 0:
        row, col = random.choice(valid_moves)
        flip_tiles(row, col, AI_COLOR)

# 翻轉棋子
def flip_tiles(row, col, color):
    board[row][col] = color
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE and board[r][c] != color and board[r][c] != EMPTY:
                while r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE and board[r][c] != color and board[r][c] != EMPTY:
                    r += dr
                    c += dc
                    if r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE and board[r][c] == color:
                        while True:
                            r -= dr
                            c -= dc
                            if r == row and c == col:
                                return
                            board[r][c] = color

# 檢查遊戲是否結束
def is_game_over():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if is_valid_move(row, col, PLAYER_COLOR) or is_valid_move(row, col, AI_COLOR):
                return False
    return True

# 計算棋盤上的棋子數量
def count_pieces():
    black_count = sum(row.count(BLACK) for row in board)
    white_count = sum(row.count(WHITE) for row in board)
    return black_count, white_count

# 執行遊戲
def play_game():
    global PLAYER_COLOR
    initialize_board()
    display_board()

    while not is_game_over():
        if PLAYER_COLOR == BLACK:
            make_player_move()
            PLAYER_COLOR = WHITE
        else:
            make_ai_move()
            PLAYER_COLOR = BLACK

        display_board()

        black_count, white_count = count_pieces()
        print("黑子數量：", black_count)
        print("白子數量：", white_count)

        # PLAYER_COLOR, AI_COLOR = AI_COLOR, PLAYER_COLOR

    black_count, white_count = count_pieces()
    if black_count > white_count:
        print("黑子獲勝！")
    elif black_count < white_count:
        print("白子獲勝！")
    else:
        print("平局！")

# 開始遊戲
play_game()