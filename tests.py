import unittest
from statement import statement
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

        self.assertEqual(
            result, '청구 내역 (고객명: BigCo)Hamlet: 650 (55석)\nAs you like it: 580 (35석)\nOthello: 500 (40석)\n총액: 1730\n적립 포인트: 47점\n'
        )

if __name__ == '__main__':
    unittest.main()