from functools import lru_cache
from typing import Dict, Type

from app.core.setting import AppSettings, AppEnvTypes

environments: Dict[AppEnvTypes, Type[AppEnvTypes]] = {
    AppEnvTypes.dev: AppSettings,
    AppEnvTypes.prod: AppSettings,
    AppEnvTypes.test: AppSettings
}

@lru_cache
def get_app_setting() -> AppSettings:
    # app_env = AppSettings.app_env
    # config = environments[app_env]
    return AppSettings()