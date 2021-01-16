import logging
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PicklePersistence
from utils import split_costs, parse_message
from strings import translations

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

DEBUG = False


def _t(context, string):
    lang = context.user_data['lang'] or 'en'
    if lang not in translations:
        lang = 'en'
    return translations[lang][string]


def reset(update, context):
    context.chat_data['state'] = {'payments': dict()}
    update.message.reply_text(_t(context, 'reset'))


def status(update, context):
    update.message.reply_text(context.chat_data['state'])


def set_language(update, context):
    context.user_data['lang'] = context.args[0]


def error(update, context):
    logger.warning('update {}, err {}'.format(update, context.error))

# potentially needed in the future
def get_tagged_users(update):
    tagged_users = [update.effective_user.id]
    for entity in update.effective_message.entities:
        if entity.type == 'text_mention':
            if entity.user.id not in tagged_users:
                tagged_users.append(entity.user.id)
    if len(tagged_users) > 1:
        return tagged_users.sort()
    return []

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
        if 'lang' not in context.user_data:
            context.user_data['lang'] = 'en'

        if 'state' not in context.chat_data:
            context.chat_data['state'] = {'payments': dict()}

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
                    debtor_name = context.bot.get_chat_member(chat_id, debtor).user.first_name
                    creditor_name = context.bot.get_chat_member(chat_id, creditor).user.first_name
                status_strings.append(_t(context, 'status').format(debtor_name, creditor_name, str(round(amount, 2))))
        reply_message = '\n'.join(status_strings) or _t(context, 'even')
    else:
        reply_message = _t(context, 'error')

    context.bot.sendMessage(chat_id, reply_message)


def main():
    TOKEN = sys.argv[1]
    state = PicklePersistence(filename='state')
    updater = Updater(TOKEN, persistence=state, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("reset", reset))
    dp.add_handler(CommandHandler("language", set_language, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text, handle))
    # dp.add_error_handler(error)

    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
