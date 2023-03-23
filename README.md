# telegram-chatbot

ℹ️ The purpose of the bot is to create a simple chat flow for ordering purposes and then log the message and username to an Excel table using pandas. There are three commands which are set in the <b>keys.py</b> file as well as every variable used in the main logic.

The <b>main.py</b> is where the logic is. We use several libraries:
- telegram - Latest
- telegram.ext - 13.7 Version
- pandas - Latest
- openpyxl - Latest

Make sure you create a virtual enviroment, change the token variable value in the <b>keys.py</b> file, as well as any other variable's value according your needs and then just run the bot.

The bot with log every entry on a new row in the spreadsheet. On the first submit, it will create the spreadsheet itself. We can keep track of every entry that way so we can act upon the order.
