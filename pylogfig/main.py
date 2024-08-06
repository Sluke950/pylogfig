import tomllib
import json
import yaml
import xml.etree.ElementTree as ET
import configparser
from dotenv import dotenv_values
import os
import logging


LOGGER = logging.getLogger(__name__)


class ConfigParseError(Exception):
    """Custom exception for configuration parsing errors."""
    pass


class Config:
    _instance = None

    def __new__(cls, config_file_path='config.toml', config_file_type=None, logging_config_file_path=None, logging_config_file_type=None):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._setup(config_file_path, config_file_type, logging_config_file_path, logging_config_file_type)
        return cls._instance

    def _setup(self, config_file_path, config_file_type, logging_config_file_path, logging_config_file_type):
        self._config = self._load_config(config_file_path, config_file_type)
        self._logging_config = (
            self._load_config(logging_config_file_path, logging_config_file_type)
            if logging_config_file_path
            else None
        )
        if self._logging_config:
            logging.config.dictConfig(self._logging_config)

    def _load_config(self, file_path, file_type):
        try:
            if file_type:
                file_extension = file_type
            else:
                file_extension = os.path.splitext(file_path)[1]

            LOGGER.debug(f"Loading '{file_extension}' file '{file_path}'.")
            if file_extension == '.toml':  # TOML files
                return Config.parse_toml_file(file_path)
            elif file_extension == '.json':  # JSON files
                return Config.parse_json_file(file_path)
            elif file_extension == '.yaml' or file_extension == '.yml':  # YAML files
                return Config.parse_yaml_file(file_path)
            elif file_extension == '.ini':  # INI files
                return Config.parse_ini_file(file_path)
            elif file_extension == '.xml':  # XML files
                return Config.parse_xml_file(file_path)
            elif file_extension == '.properties':  # Properties files
                return Config.parse_properties_file(file_path)
            elif file_extension == '.env':  # .env files
                return Config.parse_env_file(file_path)
            elif file_extension == '.config':  # Config files
                raise ConfigParseError(f"Must specify file extension to parse as for '.config' file '{file_path}'.")
            else:
                raise ConfigParseError(
                    f"Invalid file extension: {file_path}. Expected a '.toml', '.json', '.yaml', '.ini', '.xml', '.properties', '.env', or '.config' file.")

        except Exception as e:
            LOGGER.exception(f'Could not load configuration.')
            raise

    @staticmethod
    def parse_ini_file(file_path):
        """Parse INI file and return a dictionary of its contents."""
        config = configparser.ConfigParser()
        try:
            config.read(file_path)
            # Convert the INI file content to a nested dictionary
            config_dict = {section: dict(config.items(section)) for section in config.sections()}
            return config_dict
        except (configparser.Error, FileNotFoundError) as e:
            raise ValueError(f"Failed to parse INI file '{file_path}': {e}")

    @staticmethod
    def parse_xml_file(file_path):
        """Parse XML file."""
        def xml_to_dict(element):
            """Convert XML element to a dictionary."""
            if len(element) == 0:
                return element.text
            result = {}
            for child in element:
                result[child.tag] = xml_to_dict(child)
            return result

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            return xml_to_dict(root)
        except (ET.ParseError, FileNotFoundError) as e:
            raise ConfigParseError(f"Failed to parse XML file: {e}")

    @staticmethod
    def parse_json_file(file_path):
        """Parse JSON file."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise ConfigParseError(f"Failed to parse JSON file: {e}")

    @staticmethod
    def parse_yaml_file(file_path):
        """Parse YAML file."""
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except (yaml.YAMLError, FileNotFoundError) as e:
            raise ConfigParseError(f"Failed to parse YAML file: {e}")

    @staticmethod
    def parse_toml_file(file_path):
        """Parse TOML file."""
        try:
            with open(file_path, 'rb') as file:
                return tomllib.load(file)
        except (tomllib.TOMLDecodeError, FileNotFoundError) as e:
            raise ConfigParseError(f"Failed to parse TOML file: {e}")

    @staticmethod
    def parse_env_file(file_path):
        config = dotenv_values(file_path)
        return config

    @staticmethod
    def parse_properties_file(file_path):
        """Parse properties file and return a dictionary of the contents."""
        config_dict = {}
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Strip whitespace and ignore comments
                    line = line.strip()
                    if not line or line.startswith('#') or line.startswith('!'):
                        continue
                    # Split line into key and value
                    if '=' in line:
                        key, value = line.split('=', 1)
                    elif ':' in line:
                        key, value = line.split(':', 1)
                    else:
                        continue  # Skip lines that don't match key-value pattern
                    config_dict[key.strip()] = value.strip()
            return config_dict
        except FileNotFoundError:
            raise ConfigParseError(f"File not found: {file_path}")
        except IOError as e:
            raise ConfigParseError(f"IO error while reading file: {e}")
        except Exception as e:
            raise ConfigParseError(f"Failed to parse properties file: {e}")

    def load_logging_config(self, input):
        if isinstance(input, dict):
            self._logging_config = input
            LOGGER.debug('Loaded logging configuration from dictionary.')
        elif isinstance(input, str):
            self._logging_config = self._load_config(input)
            LOGGER.debug(
                f"Loaded logging configuration from filepath '{input}'.")
        else:
            raise TypeError(
                f"Expected type 'dict' or 'str' for input, got {type(input)}")

        if self._logging_config:
            logging.config.dictConfig(self._logging_config)

    def get(self, key=None, default=None):
        value = self._config
        if key:
            keys = key.split('.')
            for key in keys:
                value = value.get(key, default)
                if value is None:
                    LOGGER.warn(f'No value found for [{key}], using default.')
                    return default
        LOGGER.debug(f'Value [{value}] found for key [{key}].')
        return value
