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
        diffs.update({d_index: 0})

    # calculate a sum of all diffs for all users
    for c_index in costs:
        cost = costs[c_index]
        if cost > 0:
            per_user = cost / user_count
            for d_index in diffs:
                diff = diffs[d_index]
                if d_index == c_index:
                    new_diff = float(diff) + float(cost) - per_user
                    diffs.update({d_index: new_diff})
                else:
                    new_diff = float(diff) - per_user
                    diffs.update({d_index: new_diff})

    # find all debtors and creditors
    debtors = {}
    creditors = {}
    for d_index in diffs:
        diff = diffs[d_index]
        if diff < 0:
            debtors[d_index] = diff
        elif diff > 0:
            creditors[d_index] = diff

    final_debtors = {}
    for debt_index in debtors:
        tmp_creditors = {}
        for credit_index in creditors:
            debt = abs(debtors[debt_index])
            credit = creditors[credit_index]
            if debt == credit:
                creditors.update({credit_index: 0})
                tmp_creditors[credit_index] = credit
                final_debtors[debt_index] = tmp_creditors
                break
            elif debt < credit:
                creditors.update({credit_index: credit - debt})
                tmp_creditors[credit_index] = debt
                final_debtors[debt_index] = tmp_creditors
                break
            else:
                creditors.update({credit_index: 0})
                debtors.update({debt_index: debt - credit})
                tmp_creditors[credit_index] = credit
                final_debtors[debt_index] = tmp_creditors

        if debtors[debt_index] == 0:
            break

    # filter out 0 debts
    for debtor in final_debtors:
        final_debtors[debtor] = dict(filter(lambda elem: elem[1] > 0, final_debtors[debtor].items()))

    return final_debtors
