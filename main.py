from telegram import *
from telegram.ext import *
import pandas as pd

import keys

# Console logging the bot start
print('The bot is working')

# Dictionary to store chat session history of each user
session_history_df = pd.DataFrame(columns=['User ID', 'Username', 'Message'])
session_history = {}

# This is the Function for the /start command
def start_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    username = update.effective_user.username
    session_history[user_id] = {'username': username, 'history': []}
    update.message.reply_text(keys.start)

# This is the Function for the /help command
def help_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    session_history[user_id]['history'].append(update.message.text)
    update.message.reply_text(keys.help)

# This is the Function for the /menu command
def menu_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    session_history[user_id]['history'].append(update.message.text)
    buttons = [[KeyboardButton(keys.product1)], [KeyboardButton(keys.product2)], [KeyboardButton(keys.product3)], [KeyboardButton(keys.product4)]]
    update.message.reply_text(keys.menu, reply_markup=ReplyKeyboardMarkup(buttons))

# This is the Menu Handler
def menuHandler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    message_text = update.message.text
    session_history[user_id]['history'].append(f'{user_id}: {message_text}')
    
    product = None
    for p in keys.products:
        if p in message_text:
            product = p
            break
    if product is not None:
        price = keys.products[product]['price']
        reply_text = f'This costs {price}'
    else:
        reply_text = handle_response(update, message_text)
        
    session_history[user_id]['history'].append(f'Bot: {reply_text}')
    button = [[KeyboardButton(keys.send)]]
    update.message.reply_text(reply_text, reply_markup=ReplyKeyboardMarkup(button))

# This is the Function to log the session history of a user
def log_session_history(user_id):
    username = session_history[user_id]['username']
    history = session_history[user_id]['history']
    log_message = f'Session history for user {username}:\n'
    for message in history:
        log_message += f'- {message}\n'
    print(log_message)

    log_data = {'User ID': user_id, 'Username': username, 'Message': '\n'.join(history)}

    global session_history_df
    session_history_df = session_history_df.append(log_data, ignore_index=True)
    session_history_df.to_excel('venv/session_history.xlsx', index=False)
    session_history[user_id]['history'] = []

# Command to handle other responses and log history
def handle_response(update: Update, text) -> str:
    user_id = update.effective_user.id
    if keys.send in text:
        log_session_history(user_id)
        return keys.finalText
    return keys.random_text

# Log errors
def error(update: Update, context: CallbackContext):
    print(f'Update {update} caused error {context.error}')

# Run the program
if __name__ == '__main__':
    updater = Updater(keys.token, use_context=True)
    dp = updater.dispatcher

    # Handlers
    dp.add_handler(CommandHandler(keys.command1, start_command))
    dp.add_handler(CommandHandler(keys.command2, help_command))
    dp.add_handler(CommandHandler(keys.command3, menu_command))
    dp.add_handler(MessageHandler(Filters.text, menuHandler))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()
