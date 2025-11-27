# Jules for Hugging Face - Configuration Management

import yaml
from typing import Any

class Config:
    """
    Handles loading and accessing application configuration from a YAML file.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, config_path: str = 'config.yaml'):
        if not hasattr(self, 'initialized'):
            self.config_path = config_path
            self.settings = self._load_config()
            self.initialized = True

    def _load_config(self) -> dict:
        """
        Loads the configuration from the YAML file.
        """
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # In a real application, you might want to create a default config
            # or raise a more specific error.
            return {}
        except yaml.YAMLError as e:
            # Handle YAML parsing errors
            raise ValueError(f"Error parsing YAML file at {self.config_path}: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a configuration value for a given key.
        """
        return self.settings.get(key, default)

# Singleton instance for easy access across the application
config = Config()
