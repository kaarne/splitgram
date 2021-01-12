import logging
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PicklePersistence
from utils import split_costs, parse_message

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# TODO:
DEBUG = True

def start(update, context):
    update.message.reply_text('Terve!')

def reset(update, context):
    context.chat_data['state'] = { 'payments': dict() }
    update.message.reply_text('Reset done')

def status(update, context):
    update.message.reply_text(context.chat_data['state'])

def help(update, context):
    update.message.reply_text('Sorry, no help')

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def handle(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if DEBUG:
        # In debug mode, first name is used as user id, and you can fake
        # multiple users by typing a name after the amount, e.g '19.99 Bob'
        arr = update.effective_message.text.split(" ")
        user_id = update.effective_user.first_name
        if len(arr) > 1:
            user_id = arr[1]

    added_cost = parse_message(update.effective_message.text)

    if (added_cost is not None):
        if 'state' not in context.chat_data:
            context.chat_data['state'] = { 'payments': dict() }

        if user_id not in context.chat_data['state']['payments']:
            context.chat_data['state']['payments'][user_id] = float(0)

        new_costs = context.chat_data['state']['payments'][user_id] + added_cost
        if new_costs < 0:
            new_costs = 0
        context.chat_data['state']['payments'][user_id] = new_costs

        results = split_costs(context.chat_data['state']['payments'])

        status_strings = []
        for debtor in results:
            for creditor, amount in results[debtor].items():
                if DEBUG:
                    debtor_name = debtor
                    creditor_name = creditor
                else:
                    debtor_name = context.bot.get_chat_member(chat_id, debtor)
                    creditor_name = context.bot.get_chat_member(chat_id, creditor)
                status_strings.append(debtor_name + ' owes ' + creditor_name + ' ' + str(round(amount, 2)) + ' €')
        reply_message = '\n'.join(status_strings) or 'No one owes anything!'
    else:
        reply_message = "Oops!"

    context.bot.sendMessage(chat_id, reply_message)


def main():
    TOKEN = sys.argv[1]

    state = PicklePersistence(filename='state')

    updater = Updater(TOKEN, persistence=state, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("reset", reset))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, handle))
    #dp.add_error_handler(error)

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()