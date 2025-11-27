# tests/test_tool_abstraction_layer.py

import unittest
from jules_hf.tools.abstraction_layer import ToolAbstractionLayer
from jules_hf.core.exceptions import ToolExecutionError

class MockTool:
    def run(self, parameters):
        return f"MockTool executed with: {parameters}"

class TestToolAbstractionLayer(unittest.TestCase):
    """
    Unit tests for the ToolAbstractionLayer class.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.tal = ToolAbstractionLayer()
        self.tal.register_tool("mock_tool", MockTool)

    def test_get_tools(self):
        """
        Test that the ToolAbstractionLayer can correctly list registered tools.
        """
        self.assertEqual(self.tal.get_tools(), ["mock_tool"])

    def test_execute_tool_success(self):
        """
        Test that the ToolAbstractionLayer can successfully execute a registered tool.
        """
        params = {"param1": "value1"}
        expected_result = "MockTool executed with: {'param1': 'value1'}"
        actual_result = self.tal.execute_tool("mock_tool", params)
        self.assertEqual(actual_result, expected_result)

    def test_execute_tool_not_found_raises_exception(self):
        """
        Test that executing a non-existent tool raises a ToolExecutionError.
        """
        with self.assertRaises(ToolExecutionError):
            self.tal.execute_tool("non_existent_tool", {})

class MockToolWithoutRun:
    pass

    def test_tool_without_run_method_raises_exception(self):
        """
        Test that a tool without a 'run' method raises a ToolExecutionError.
        """
        self.tal.register_tool("bad_tool", MockToolWithoutRun)
        with self.assertRaises(ToolExecutionError):
            self.tal.execute_tool("bad_tool", {})

if __name__ == '__main__':
    unittest.main()
