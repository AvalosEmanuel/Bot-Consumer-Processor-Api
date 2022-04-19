import unittest
from api_secret import get_secret

class TestSecret(unittest.TestCase):
    def test_get_secret(self):
        """
        Tests that the key returned by the function is correct
        """
        secret = get_secret()
        key = "sdInnRoPyoqBotVk8r6e2f4zTPc_khXy"
        self.assertEqual(secret, key)


    def test_get_secret_type_return(self):
        """
        Check that the key returned by the function is of the correct data type (str)
        """
        secret= get_secret()
        self.assertIs(type(secret), str)


if __name__ == 'main':
    unittest.main()