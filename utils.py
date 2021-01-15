def parse_message(message):
    amount = message.split(" ")[0]
    try:
        result = float(amount)
        return result
    except ValueError:
        return None


def split_costs(costs):
    if len(costs) == 0:
        return {}

    results = dict()
    creditors = []
    debtors = []
    cost_per_user = sum(costs.values()) / len(costs)

    for user, value in costs.items():
        if value < cost_per_user:
            debtors.append({'user': user, 'value': cost_per_user - value})
            results[user] = dict()
        elif value > cost_per_user:
            creditors.append({'user': user, 'value': value - cost_per_user})

    for debtor in debtors:
        for creditor in creditors:
            if creditor['value'] > 0:
                remaining = creditor['value'] - debtor['value']
                if remaining == 0:
                    results[debtor['user']][creditor['user']] = creditor['value']
                    creditor['value'] = 0
                    break
                elif remaining < 0:
                    results[debtor['user']][creditor['user']] = creditor['value']
                    creditor['value'] = 0
                    debtor['value'] = abs(remaining)
                    continue
                else:  # remaining > 0
                    results[debtor['user']][creditor['user']] = debtor['value']
                    creditor['value'] -= debtor['value']
                    break
    return results
