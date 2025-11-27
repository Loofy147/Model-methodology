# tests/test_huggingface_client.py

import unittest
from unittest.mock import patch, MagicMock
from jules_hf.tools.huggingface_client import HuggingFaceClient
from jules_hf.core.exceptions import ConfigurationError, ToolExecutionError

class TestHuggingFaceClient(unittest.TestCase):
    """
    Unit tests for the HuggingFaceClient class.
    """

    @patch.dict('os.environ', {'HUGGING_FACE_HUB_TOKEN': 'test_token'})
    def setUp(self):
        """
        Set up the test case with a mocked environment variable.
        """
        self.hfc = HuggingFaceClient()

    def test_init_raises_error_if_token_missing(self):
        """
        Test that the client raises a ConfigurationError if the token is not set.
        """
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(ConfigurationError):
                HuggingFaceClient()

    @patch('jules_hf.tools.huggingface_client.login')
    def test_login_success(self, mock_login):
        """
        Test that the HuggingFaceClient can successfully log in.
        """
        params = {"operation": "login"}
        result = self.hfc.run(params)

        self.assertEqual(result, "Successfully logged in to the Hugging Face Hub.")
        mock_login.assert_called_once_with(token="test_token", add_to_git_credential=True)

    @patch('jules_hf.tools.huggingface_client.login')
    def test_login_failure_raises_exception(self, mock_login):
        """
        Test that a login failure raises a ToolExecutionError.
        """
        mock_login.side_effect = Exception("Invalid token")
        with self.assertRaises(ToolExecutionError):
            self.hfc.run({"operation": "login"})

    @patch('jules_hf.tools.huggingface_client.create_repo')
    def test_create_repo_success(self, mock_create_repo):
        """
        Test that the HuggingFaceClient can successfully create a repository.
        """
        mock_create_repo.return_value = "https://huggingface.co/test-user/test-repo"
        params = {"operation": "create_repo", "repo_id": "test-user/test-repo"}
        result = self.hfc.run(params)

        self.assertIn("Successfully created repository", result)
        mock_create_repo.assert_called_once_with(repo_id="test-user/test-repo", repo_type="model", token="test_token")

    def test_unsupported_operation_raises_exception(self):
        """
        Test that an unsupported operation raises a ToolExecutionError.
        """
        with self.assertRaises(ToolExecutionError):
            self.hfc.run({"operation": "delete_repo"})


if __name__ == '__main__':
    unittest.main()
