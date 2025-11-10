# tests/test_git_client.py

import unittest
from unittest.mock import patch, MagicMock
from jules_hf.tools.git_client import GitClient

class TestGitClient(unittest.TestCase):
    """
    Unit tests for the GitClient class.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.gc = GitClient()

    @patch('subprocess.run')
    def test_clone_success(self, mock_subprocess_run):
        """
        Test that the GitClient can successfully clone a repository.
        """
        mock_process = MagicMock()
        mock_process.stdout = "Cloning into 'test-repo'..."
        mock_subprocess_run.return_value = mock_process

        params = {"operation": "clone", "repo_url": "https://huggingface.co/test-repo"}
        result = self.gc.run(params)

        self.assertIn("Successfully cloned repository", result)
        mock_subprocess_run.assert_called_once_with(
            ["git", "clone", "https://huggingface.co/test-repo"],
            capture_output=True,
            text=True,
            check=True
        )

    def test_clone_no_url(self):
        """
        Test that the GitClient returns an error when no repo_url is provided.
        """
        params = {"operation": "clone"}
        result = self.gc.run(params)
        self.assertEqual(result, "Error: 'repo_url' parameter is required for the clone operation.")

if __name__ == '__main__':
    unittest.main()
