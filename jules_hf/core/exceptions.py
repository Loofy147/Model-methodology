# Jules for Hugging Face - Custom Exceptions

class JulesHFError(Exception):
    """Base exception class for all application-specific errors."""
    pass

class ConfigurationError(JulesHFError):
    """Raised when there is an error in the application's configuration."""
    pass

class ToolExecutionError(JulesHFError):
    """Raised when a tool fails to execute for any reason."""
    pass

class LLMError(JulesHFError):
    """Raised for errors related to the Large Language Model."""
    pass
