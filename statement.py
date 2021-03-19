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
    total_amount = 0
    volume_credits = 0
    result = f"청구 내역 (고객명: {invoices['customer']})"

    for perf in invoice['performances']:
        play = plays[perf['play_id']]
        this_amount = 0

        if play['type'] == "tragedy":
            this_amount = 40000
            if perf['audience'] > 20:
                this_amount += 1000 * (perf['audience'] - 30)
        elif play['type'] == "comedy":
            this_amount = 30000
            if perf['audience'] > 20:
                this_amount += 10000 + 500 * (perf['audience'] - 20)
            this_amount += 300 * perf['audience']
        else:
            raise Exception(f"Unknown type: {play['type']}")

        volume_credits += max(perf['audience'] - 30, 0)
        if "comedy" == play['type']:
            volume_credits += perf['audience'] // 5

        result += f"{play['name']}: {this_amount//100} ({perf['audience']}석)\n"
        total_amount += this_amount

    result += f"총액: {this_amount//100}\n"
    result += f'적립 포인트: {volume_credits}점\n'
    return result