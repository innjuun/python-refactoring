def statement(invoice, plays):

    def play_for(a_performance):
        return plays[a_performance['play_id']]

    def amount_for(a_performance):
        result = 0
        if a_performance['play']['type'] == "tragedy":
            result = 40000
            if a_performance['audience'] > 20:
                result += 1000 * (a_performance['audience'] - 30)
        elif a_performance['play']['type'] == "comedy":
            result = 30000
            if a_performance['audience'] > 20:
                result += 10000 + 500 * (a_performance['audience'] - 20)
            result += 300 * a_performance['audience']
        else:
            raise Exception(f"Unknown type: {a_performance['play']['type']}")
        return result

    def volume_credits_for(a_performance):
        result = 0
        result += max(a_performance['audience'] - 30, 0)
        if "comedy" == a_performance['play']['type']:
            result += a_performance['audience'] // 5
        return result

    def total_amount(data):
        result = 0
        for perf in data['performances']:
            result += perf['amount']
        return result

    def total_volume_credits(data):
        result = 0
        for perf in data['performances']:
            result += perf['volume_credits']
        return result

    def enrich_performance(a_performance):
        result = dict(a_performance)
        result['play'] = play_for(result)
        result['amount'] = amount_for(result)
        result['volume_credits'] = volume_credits_for(result)
        return result

    statement_data = {}
    statement_data['customer'] = invoice['customer']
    statement_data['performances'] = [enrich_performance(performance) for performance in invoice['performances']]
    statement_data['total_amount'] = total_amount(statement_data)
    statement_data['total_volume_credits'] = total_volume_credits(statement_data)
    return render_plain_text(statement_data, plays)


def render_plain_text(data, plays):

    result = f"청구 내역 (고객명: {data['customer']})"

    for perf in data['performances']:
        result += f"{perf['play']['name']}: {perf['amount']//100} ({perf['audience']}석)\n"

    result += f"총액: {data['total_amount']//100}\n"
    result += f"적립 포인트: {data['total_volume_credits']}점\n"
    return result