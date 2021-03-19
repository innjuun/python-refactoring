plays ={
    "hamlet": {"name": "Hamlet", "type": "tragedy"},
    "as-like": {"name": "As you like it", "type": "tragedy"},
    "othello": {"name": "Othello", "type": "tragedy"}
}

invoices = [
    {
        "customer": "BigCo",
        "performances": [
            {
                "play_id": "hamlet",
                "audience": 55,
            },
            {
                "play_id": "as-like",
                "audience": 35
            },
            {
                "play_id": "othello",
                "audience": 40
            }
        ]
    }
]


def statement(invoice, plays):
    def play_for(a_performance):
        return plays[a_performance['play_id']]

    def amount_for(a_performance):
        result = 0
        if play_for(a_performance)['type'] == "tragedy":
            result = 40000
            if a_performance['audience'] > 20:
                result += 1000 * (a_performance['audience'] - 30)
        elif play_for(a_performance)['type'] == "comedy":
            result = 30000
            if a_performance['audience'] > 20:
                result += 10000 + 500 * (a_performance['audience'] - 20)
            result += 300 * a_performance['audience']
        else:
            raise Exception(f"Unknown type: {play_for(a_performance)['type']}")
        return result

    total_amount = 0
    volume_credits = 0
    result = f"청구 내역 (고객명: {invoices['customer']})"

    for perf in invoices['performances']:

        volume_credits += max(perf['audience'] - 30, 0)
        if "comedy" == play_for(perf)['type']:
            volume_credits += perf['audience'] // 5

        result += f"{play_for(perf)['name']}: {amount_for(perf)//100} ({perf['audience']}석)\n"
        total_amount += amount_for(perf)

    result += f"총액: {total_amount//100}\n"
    result += f'적립 포인트: {volume_credits}점\n'
    return result