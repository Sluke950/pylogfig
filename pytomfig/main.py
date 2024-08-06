import tomllib
import json
import os
import logging

LOGGER = logging.getLogger(__name__)


class Config:
    _instance = None

    def __new__(cls, config_file_path='config.toml', logging_config_file_path=None):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._setup(config_file_path, logging_config_file_path)
        return cls._instance

    def _setup(self, config_file_path, logging_config_file_path):
        self.config = self._load_config(config_file_path)
        self.logging_config = self._load_config(
            logging_config_file_path) if logging_config_file_path else None

    def _load_config(self, file_path):
        try:
            file_extension = os.path.splitext(file_path)[1]

            LOGGER.debug(f'Loading {file_extension} file {file_path}.')
            if file_extension == '.toml':  # TOML files
                with open(file_path, 'rb') as file:
                    return tomllib.load(file)
            elif file_extension == '.json':  # JSON files
                return json.load(file_path)
            elif file_extension == '.yaml' or file_extension == '.yml':  # YAML files
                return
            elif file_extension == '.ini':  # INI files
                return
            elif file_extension == '.xml':  # XML files
                return
            elif file_extension == '.properties':  # Properties files
                return
            elif file_extension == '.env':  # .env files
                return
            elif file_extension == '.sh' or file_extension == '.bash':  # Shell files
                return
            elif file_extension == '.md':  # Markdown files
                return
            elif file_extension == '.config':  # Config files
                return
            else:
                raise ValueError(
                    f"Invalid file extension: {file_path}. Expected a '.toml', '.json', or '.yaml' file.")

        except Exception as e:
            LOGGER.exception(f'Could not load configuration.')
            raise

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for key in keys:
            value = value.get(key, default)
            if value is None:
                LOGGER.warn(f'No value found for [{key}], using default.')
                return default
        LOGGER.debug(f'Value [{value}] found for key [{key}].')
        return value
