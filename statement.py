def statement(invoice, plays):

    def play_for(a_performance):
        return plays[a_performance['play_id']]

    def enrich_performance(a_performance):
        result = dict(a_performance)
        result['play'] = play_for(a_performance)
        return result

    statement_data = {}
    statement_data['customer'] = invoice['customer']
    statement_data['performances'] = [enrich_performance(performance) for performance in invoice['performances']]
    return render_plain_text(statement_data, plays)


def render_plain_text(data, plays):

    def volume_credits_for(a_performance):
        result = 0
        result += max(a_performance['audience'] - 30, 0)
        if "comedy" == a_performance['play']['type']:
            result += a_performance['audience'] // 5
        return result

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

    def total_amount():
        result = 0
        for perf in data['performances']:
            result += amount_for(perf)
        return result

    def total_volume_credits():
        result = 0
        for perf in data['performances']:
            result += volume_credits_for(perf)
        return result

    result = f"청구 내역 (고객명: {data['customer']})"

    for perf in data['performances']:
        result += f"{perf['play']['name']}: {amount_for(perf)//100} ({perf['audience']}석)\n"

    result += f"총액: {total_amount()//100}\n"
    result += f'적립 포인트: {total_volume_credits()}점\n'
    return result