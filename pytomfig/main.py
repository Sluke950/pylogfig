import tomllib

class Config:
    _instance = None

    def __new__(cls, file_path='config.toml'):
        """Creates new instance, loads super init and the toml configuration file.

        Args:
            file_path (str, optional): File path to configuration toml file. Defaults to 'config.toml'.

        Returns:
            Config: instance.
        """
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config(file_path)
        return cls._instance

    def _load_config(self):
        """
        Loads configuration data from the specified TOML file into the instance.

        This method reads the configuration file specified by `self.config_file_path` and 
        parses its content using the `tomllib` module. The parsed configuration data is 
        stored in the instance attribute `_config`.

        Raises:
            FileNotFoundError: If the file specified by `self.config_file_path` does not exist.
            IsADirectoryError: If the path specified by `self.config_file_path` is a directory.
            tomllib.TOMLDecodeError: If there is an error parsing the TOML file.

        Returns:
            None
        """
        with open(self.config_file_path, 'r') as file:
            self._config = tomllib.load(file)

    def get(self, key, default=None):
        """Return a value from the config toml file.

        Args:
            key (str): Parameter name.
            default (Any, optional): Default value to return if value can't be found in the config file. Defaults to None.

        Returns:
            Any: the value from the configuration file.
        """
        keys = key.split('.')
        value = self.config
        for key in keys:
            value = value.get(key, default)
            if value is None:
                #log warning no value found, using default
                return default
        return value
                
            