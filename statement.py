def statement(invoice, plays):
    return render_plain_text(create_statement_data(invoice, plays))


def html_statement(invoice, plays):
    return render_html(create_statement_data(invoice, plays))


class PerformanceCalculator:
    def __init__(self, a_performance, a_play):
        self.performance = a_performance
        self.play = a_play

    def amount(self):
        raise NotImplementedError("서브 클래스에서 처리합니다")

    def volume_credits(self):
        return max(self.performance['audience'] - 30, 0)

class TragedyCalculator(PerformanceCalculator):
    def amount(self):
        result = 40000
        if self.performance['audience'] > 20:
            result += 1000 * (self.performance['audience'] - 30)
        return result

class ComedyCalculator(PerformanceCalculator):
    def amount(self):
        result = 30000
        if self.performance['audience'] > 20:
            result += 10000 + 500 * (self.performance['audience'] - 20)
        result += 300 * self.performance['audience']
        return result

    def volume_credits(self):
        return super().volume_credits() + self.performance['audience'] // 5


def create_performance_calculator(a_performance, a_play):
    if a_play['type'] == "tragedy":
        return TragedyCalculator(a_performance, a_play)
    elif a_play['type'] == "comedy":
        return ComedyCalculator(a_performance, a_play)
    else:
        raise Exception(f"알 수 없는 장르: {a_play['type']}")


def create_statement_data(invoice, plays):

    def play_for(a_performance):
        return plays[a_performance['play_id']]


    def total_amount(data):
        return sum((performance['amount'] for performance in data['performances']))

    def total_volume_credits(data):
        return sum((performance['volume_credits'] for performance in data['performances']))


    def enrich_performance(a_performance):
        calculator = create_performance_calculator(a_performance, play_for(a_performance))
        result = dict(a_performance)
        result['play'] = calculator.play
        result['amount'] = calculator.amount()
        result['volume_credits'] = calculator.volume_credits()
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