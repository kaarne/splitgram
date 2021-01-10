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
    context.chat_data['state'] = { "users": dict() }
    update.message.reply_text('reset done')

def status(update, context):
    update.message.reply_text(context.chat_data['state'])

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

def split_costs(costs):
    user_count = len(costs)

    # init diffs
    diffs = costs.copy()
    for d_index in diffs:
        diffs.update({d_index : 0})

    # calculate a sum of all diffs for all users
    for c_index in costs:
        cost = costs[c_index]
        if cost > 0:
            per_user = cost/user_count
            for d_index in diffs:
                diff = diffs[d_index]
                if d_index == c_index:
                    new_diff = float(diff) + float(cost) - per_user
                    diffs.update({d_index : new_diff})
                else:
                    new_diff = float(diff) - per_user
                    diffs.update({d_index : new_diff})

    # print("diffs:", diffs)

    # find all debtors and creditors
    debtors = {}
    creditors = {}
    for d_index in diffs:
        diff = diffs[d_index]
        if diff < 0:
            debtors[d_index] = diff
        elif diff > 0:
            creditors[d_index] = diff

    # print("creditors:", creditors)
    # print("debtors:", debtors)

    final_debtors = {}
    for debt_index in debtors:
        tmp_creditors = {}
        for credit_index in creditors:
            debt = abs(debtors[debt_index])
            credit = creditors[credit_index]
            if debt == credit:
                # print("debt == credit")
                creditors.update({credit_index: 0})
                tmp_creditors[credit_index] = credit
                final_debtors[debt_index] = tmp_creditors
                break
            elif debt < credit:
                # txt = "debt: {0} < credit: {1}"
                # print(txt.format(debt, credit))
                creditors.update({credit_index: credit - debt})
                tmp_creditors[credit_index] = debt
                final_debtors[debt_index] = tmp_creditors
                break
            else:
                # print("debt > credit")
                creditors.update({credit_index: 0})
                debtors.update({debt_index: debt - credit})
                tmp_creditors[credit_index] = credit
                final_debtors[debt_index] = tmp_creditors

        # print("final_debtors: ", final_debtors)
        if debtors[debt_index] == 0:
            break

    # filter out 0 debts
    for debtor in final_debtors:
        final_debtors[debtor] = dict(filter(lambda elem: elem[1] > 0, final_debtors[debtor].items()))

    return final_debtors


def handle(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name

    # for debugging purposes only
    if True:
       arr = update.effective_message.text.split(" ")
       if len(arr) > 1:
           user = arr[1]

    added_cost = parse_message(update.effective_message.text)

    if (added_cost is not None):
        if 'state' not in context.chat_data:
            context.chat_data['state'] = { "users": dict() }

        if user not in context.chat_data['state']['users']:
            context.chat_data['state']['users'][user] = float(0)

        new_costs = context.chat_data['state']['users'][user] + added_cost
        if new_costs < 0:
            new_costs = 0
        context.chat_data['state']['users'][user] = new_costs

        results = split_costs(context.chat_data['state']['users'])

        messages = []
        for debtor in results:
            for creditor, amount in results[debtor].items():
                messages.append(debtor + ' owes ' + creditor + ' ' + str(round(amount, 2)) + ' €')

        context.bot.sendMessage(chat_id, '\n'.join(messages) or user + ' is the only participant so far')

    else:
        context.bot.sendMessage(chat_id, 'oops :(')

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