import json
class Config:
    def __init__(self, file_config: str):
        self._file_config = file_config
        self._theme = self.read_config()

    @property
    def file_config(self):
        """Getter for file config"""
        return self._file_config

    @file_config.setter
    def file_config(self, value):
        """Setter for file config"""
        self._file_config = value

    @property
    def theme(self):
        """Getter for theme"""
        return self._theme

    @theme.setter
    def theme(self, value):
        """Setter for theme"""
        self._theme = value

    def read_config(self):
        """Reads config from file"""
        with open(self._file_config, "r") as file:
            config = json.loads(file.read())
            self._theme = config["theme"]

    def set_theme(self):
        """Setter for theme"""
        with open(self._file_config, "w") as file:
            file.write(json.dumps({"theme":self._theme}, indent=4))
