def statement(invoice, plays):
    return render_plain_text(create_statement_data(invoice, plays))


def html_statement(invoice, plays):
    return render_html(create_statement_data(invoice, plays))


def create_statement_data(invoice, plays):

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

    result = {}
    result['customer'] = invoice['customer']
    result['performances'] = [enrich_performance(performance) for performance in invoice['performances']]
    result['total_amount'] = total_amount(result)
    result['total_volume_credits'] = total_volume_credits(result)

    return result

def render_plain_text(data):
    result = f"청구 내역 (고객명: {data['customer']})"

    for perf in data['performances']:
        result += f"{perf['play']['name']}: {perf['amount']//100} ({perf['audience']}석)\n"

    result += f"총액: {data['total_amount']//100}\n"
    result += f"적립 포인트: {data['total_volume_credits']}점\n"
    return result

def render_html(data):
    result = f"<h1>청구 내역 (고객명: {data['customer']}</h1>"
    result += "<table>\n"
    result += "<tr><th>연극</th><th>좌석 수</th><th>금액</th></tr>"
    for perf in data['performances']:
        result += f"<tr><td>{perf['play']['name']}</td><td>({perf['audience']}석)</td>"
        result += f"<td>{perf['amount']}</td></tr>"
    result += "</trble>\n"
    result += f"<p>총액: <em>{data['total_amount']}</em></p>\n"
    result += f"<p>적립 포인트: <em>{data['total_volume_credits']}</em>점</p>\n"
    return result