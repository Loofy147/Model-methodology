# tests/test_huggingface_client.py

import unittest
from unittest.mock import patch, MagicMock
from jules_hf.tools.huggingface_client import HuggingFaceClient

class TestHuggingFaceClient(unittest.TestCase):
    """
    Unit tests for the HuggingFaceClient class.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.hfc = HuggingFaceClient()

    @patch('jules_hf.tools.huggingface_client.login')
    def test_login_success(self, mock_login):
        """
        Test that the HuggingFaceClient can successfully log in.
        """
        params = {"operation": "login", "token": "test_token"}
        result = self.hfc.run(params)

        self.assertEqual(result, "Successfully logged in to the Hugging Face Hub.")
        mock_login.assert_called_once_with(token="test_token", add_to_git_credential=True)

    @patch('jules_hf.tools.huggingface_client.create_repo')
    def test_create_repo_success(self, mock_create_repo):
        """
        Test that the HuggingFaceClient can successfully create a repository.
        """
        mock_create_repo.return_value = "https://huggingface.co/test-user/test-repo"
        params = {"operation": "create_repo", "repo_id": "test-user/test-repo"}
        result = self.hfc.run(params)

        self.assertIn("Successfully created repository", result)
        mock_create_repo.assert_called_once_with(repo_id="test-user/test-repo", repo_type="model")


if __name__ == '__main__':
    unittest.main()
