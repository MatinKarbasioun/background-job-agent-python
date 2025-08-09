from pathlib import Path
import json
import os


class AppSetting:
    APP_SETTINGS = None

    def __init__(self):
        self._appSetting = {}
        self._credentials = {}
        self.__directory = os.path.join(Path(__file__).resolve().parent.parent, "config")
        AppSetting.APP_SETTINGS = self._load_settings()


    def _load_settings(self):
        app_settings_name = os.getenv('APP_SETTING_NAME', 'app_settings')
        directory = os.path.join(self.__directory, app_settings_name + ".json")

        with open(directory) as json_file:
            self._appSetting = json.load(json_file)

        return self._appSetting
