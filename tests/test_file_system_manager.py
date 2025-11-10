# tests/test_file_system_manager.py

import unittest
import os
from jules_hf.tools.file_system_manager import FileSystemManager

class TestFileSystemManager(unittest.TestCase):
    """
    Unit tests for the FileSystemManager class.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.fsm = FileSystemManager()
        self.test_file = "test_file.txt"

    def tearDown(self):
        """
        Tear down the test case.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_create_file_success(self):
        """
        Test that the FileSystemManager can successfully create a file.
        """
        params = {"file_path": self.test_file}
        result = self.fsm.create_file(params)
        self.assertEqual(result, f"Successfully created file: {self.test_file}")
        self.assertTrue(os.path.exists(self.test_file))

    def test_create_file_no_path(self):
        """
        Test that the FileSystemManager returns an error when no file path is provided.
        """
        params = {}
        result = self.fsm.create_file(params)
        self.assertEqual(result, "Error: 'file_path' parameter is required.")
        self.assertFalse(os.path.exists(self.test_file))

if __name__ == '__main__':
    unittest.main()
