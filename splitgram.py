import logging
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PicklePersistence

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('Terve!')

def reset(update, context):
    update.message.reply_text('reset')

def help(update, context):
    update.message.reply_text('sorry, no help')

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def parse_message(message):
    amount = message.split(" ")[0]
    try:
        result = float(amount)
        return result
    except ValueError:
        return None

# TODO: implement
def split_costs(costs):
    per_user = sum(costs.values()) / len(costs)
    print("per user:", per_user)

    debtors = {"lulu": {"lala" : 10, "chuchu": 20} }
    return debtors


def handle(update, context):
    print(update)
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name

    command = parse_message(update.effective_message.text)

    print("chat_id", chat_id)
    print("user", user)
    print("command", command)

    if (command is not None):
        current = context.chat_data.get('state')
        if (current is None):
            current = {}
            current['users'] = {}
            current['users'][user] = float(0)

        # TODO: limit to 2 decimals
        updated = current['users'][user] + command
        context.chat_data['state']['users'][user] = updated

        results = split_costs(context.chat_data['state']['users'])
        context.bot.sendMessage(chat_id, results)
    else:
        context.bot.sendMessage(chat_id, 'oops :(')


def main():
    TOKEN = sys.argv[1]

    state = PicklePersistence(filename='state')

    updater = Updater(TOKEN, persistence=state, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("reset", reset))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, handle))
    dp.add_error_handler(error)

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()