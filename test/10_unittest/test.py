import unittest
from toutiao import create_app
from settings.testing import TestingConfig


class SuggestionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.flask_app = create_app(TestingConfig)
        self.client = self.flask_app.test_client()

    def test_miss_q(self):
        # 测试缺少q参数
        response = self.client.get('/v1_0/suggestion')
        self.assertEqual(response.status_code,400)
if __name__ == '__main__':
    unittest.main()