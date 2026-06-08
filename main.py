import os
import random

from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

Token = os.getenv("TELEGRAM_BOT_TOKEN")
if not Token:
    raise RuntimeError("Please set TELEGRAM_BOT_TOKEN before running the bot.")

# 定義棋盤大小
BOARD_SIZE = 8

# 定義棋盤狀態
EMPTY = '  .  '
BLACK = '⚫️'
WHITE = '⚪️'

# 定義棋子顏色
PLAYER_COLOR = BLACK
AI_COLOR = WHITE

# 創建棋盤
board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]

PLAYER_ROUND= range(1)
AI_move = [0,0]

# 初始化棋盤
def initialize_board():
    global board
    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    mid = BOARD_SIZE // 2
    board[mid][mid] = WHITE
    board[mid - 1][mid - 1] = WHITE
    board[mid][mid - 1] = BLACK
    board[mid - 1][mid] = BLACK

# 顯示棋盤
async def display_board(update, context):
    global board
    # 將二維陣列轉換為字串
    board_str = "------------------ 目前盤面 ------------------\n" + \
                "     a    b    c    d    e    f    g    h\n"

    for i in range(8):
        board_str += str(i + 1) + " "
        for j in range(8):
            board_str += " "
            if board[i][j] == EMPTY:
                board_str += EMPTY
            elif board[i][j] == BLACK:
                board_str += BLACK
            else:
                board_str += WHITE
        board_str += '\n'

    # 回覆訊息，顯示棋盤
    await update.message.reply_text(board_str)

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
                        if r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE and board[r][c] == EMPTY:
                            break
    return False

# 執行玩家移動
async def make_player_move(update, context) -> int:
    global PLAYER_COLOR, board
    while True:
        move = update.message.text
        if len(move) != 2 or not move[0].isalpha() or not move[1].isdigit():
            await update.message.reply_text("輸入無效，請重新輸入")
        else:
            col = ord(move[0].lower()) - ord('a')
            row = ord(move[1]) - ord('1')
            if is_valid_move(row, col, BLACK):
                flip_tiles(row, col, BLACK)
                PLAYER_COLOR = WHITE
                return
            else:
                await update.message.reply_text("不能在此處落子，請重新輸入")
        # 等待下一個輸入
        update = await context.bot.get_updates()[-1]


# 執行AI移動
def make_ai_move():
    global PLAYER_COLOR, AI_move
    valid_moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if is_valid_move(row, col, AI_COLOR):
                valid_moves.append((row, col))
    if len(valid_moves) > 0:
        row, col = random.choice(valid_moves)
        flip_tiles(row, col, AI_COLOR)
        AI_move[0] = col+1
        AI_move[1] = row+1
    return len(valid_moves) > 0


# 翻轉棋子
def flip_tiles(row, col, color):
    global board
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
                            board[r][c] = color
                            if r == row and c == col:
                                break
    return

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

async def start_game(update, context) -> int:
    global PLAYER_COLOR, board
    initialize_board()
    await update.message.reply_text("來玩黑白棋吧，你先開始！ ouob")
    await display_board(update, context)
    await update.message.reply_text("請輸入你的下一步位置（例如：c4）")
    return PLAYER_ROUND

# 執行遊戲
async def play_game(update, context) -> int:
    global PLAYER_COLOR, board

    while not is_game_over():
        if PLAYER_COLOR == BLACK:
            await make_player_move(update, context)
        else:
            if make_ai_move():
                await update.message.reply_text("我下在 " + chr(AI_move[0]+ord("a")-1) + str(AI_move[1]))
            PLAYER_COLOR = BLACK
        await display_board(update, context)

        if not is_game_over() and PLAYER_COLOR == BLACK:
            await update.message.reply_text("輪到你了！請輸入你的下一步位置（例如：c4）")
            # 等待下一個輸入
            update = await context.bot.get_updates()[-1]

    black_count, white_count = count_pieces()
    await update.message.reply_text("黑子數量：" + str(black_count))
    await update.message.reply_text("白子數量：" + str(white_count))

    if black_count > white_count:
        await update.message.reply_text("我輸了 இдஇ")
    elif black_count < white_count:
        await update.message.reply_text("我贏了 ⁽⁽٩(๑˃̶͈̀ ᗨ ˂̶͈́)۶⁾⁾")
    else:
        await update.message.reply_text("平局！")

    return ConversationHandler.END


async def restart(update, context) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text("好啊！再來一局 owob")
    await start_game(update, context)
    return ConversationHandler.END


# 開始遊戲
def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(Token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_game)],
        states={
            PLAYER_ROUND: [MessageHandler(filters.TEXT & ~filters.COMMAND, play_game)]
        },
        fallbacks=[CommandHandler("restart", restart)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()

