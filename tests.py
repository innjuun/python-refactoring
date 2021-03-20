import unittest
from statement import html_statement, statement
class StatementTest(unittest.TestCase):

    def setUp(self):
        self.plays = {
            "hamlet": {"name": "Hamlet", "type": "tragedy"},
            "as-like": {"name": "As you like it", "type": "comedy"},
            "othello": {"name": "Othello", "type": "tragedy"}
        }
        self.invoices = [
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

    def test_statement(self):
        result = statement(self.invoices[0], self.plays)
        expected = '청구 내역 (고객명: BigCo)Hamlet: 650 (55석)\nAs you like it: 580 (35석)\nOthello: 500 (40석)\n총액: 1730\n적립 포인트: 47점\n'
        self.assertEqual(
            result, expected
        )

    def test_render_html(self):
        result = html_statement(self.invoices[0], self.plays)
        expected = '<h1>청구 내역 (고객명: BigCo</h1><table>\n<tr><th>연극</th><th>좌석 수</th><th>금액</th></tr><tr><td>Hamlet</td><td>(55석)</td><td>65000</td></tr><tr><td>As you like it</td><td>(35석)</td><td>58000</td></tr><tr><td>Othello</td><td>(40석)</td><td>50000</td></tr></trble>\n<p>총액: <em>173000</em></p>\n<p>적립 포인트: <em>47</em>점</p>\n'
        self.assertEqual(
            result, expected
        )

if __name__ == '__main__':
    unittest.main()