from pathlib import Path
import json
import os


class AppSetting:
    APP_SETTINGS = None
    CREDENTIALS = None

    def __init__(self):
        self._appSetting = {}
        self._credentials = {}
        self.__directory = os.path.join(Path(__file__).resolve().parent.parent, "app")
        AppSetting.APP_SETTINGS = self._load_settings()
        AppSetting.CREDENTIALS = self._load_credentials()


    def _load_settings(self):
        app_settings_name = os.getenv('APP_SETTING_NAME', 'app_settings')
        directory = os.path.join(self.__directory, app_settings_name + ".json")

        with open(directory) as json_file:
            self._appSetting = json.load(json_file)

        return self._appSetting

    def _load_credentials(self):
        credentials_name = os.getenv('APP_SETTING_NAME', 'credentials')
        directory = os.path.join(self.__directory, credentials_name + ".json")

        with open(directory) as json_file:
            self._credentials = json.load(json_file)

        return self._credentials
