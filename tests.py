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

    def test_play_for(self):
        pass
if __name__ == '__main__':
    unittest.main()