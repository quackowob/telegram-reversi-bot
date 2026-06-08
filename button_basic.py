from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import os

Token = os.getenv("TELEGRAM_BOT_TOKEN")
if not Token:
    raise RuntimeError("Please set TELEGRAM_BOT_TOKEN before running the bot.")
black = '⚫️'
white = '⚪️'


def enc(board):
    # grid = [[board.get((row, col), '') for col in range(8)] for row in range(8)]
    number = 0
    base = 3
    for row in range(8):
        for col in range(8):
            number *= base
            # if grid[row][col] == black:
            if board.get((row, col)) == black:
                number += 1
            # elif grid[row][col] == white:
            elif board.get((row, col)) == white:
                number += 2
    return str(number)


def dec(number):
    board = {}
    base = 3
    for row in range(7, -1, -1):
        for col in range(7, -1, -1):
            if number % base == 1:
                # grid[row][col] = black
                board[(row, col)] = black
            elif number % base == 2:
                # grid[row][col] = white
                board[(row, col)] = white
            number //= base
    return board


def board_markup(board):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(board.get((row, col), ' '), callback_data=f'{row}{col}{enc(board)}') for col in
         range(8)]
        for row in range(8)])


async def func(update, context):
    data = update.callback_query.data
    row = int(data[0])
    col = int(data[1])
    await context.bot.answer_callback_query(update.callback_query.id,
                                            f'你按的 row={row},col={col}\n')
    # TODO: check if the button is clickable, if not, report it is not clickable and return

    board = dec(int(data[2:]))
    board[(row, col)] = black
    await context.bot.edit_message_text('目前盤面',
                                        reply_markup = board_markup(board),
                                        chat_id=update.callback_query.message.chat_id,
                                        message_id=update.callback_query.message.message_id)


async def start(update, context):
    board = {(3, 3): black, (3, 4): white, (4, 3): white, (4, 4): black}
    await update.message.reply_text('目前盤面', reply_markup = board_markup(board))


def main():
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(Token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    application.add_handler(CallbackQueryHandler(func))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
