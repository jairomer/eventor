from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

@lru_cache
def get_settings():
    """
        This will create only one instance of a class 
        and return the same object in the next requests.
    """
    return AppSettings()

class AppSettings(BaseSettings):
    app_name: str = "Flyer Generator Rest API"
    MAX_IN_MEMORY: int = 3000
    STABLE_DIFUSSION_INSTANCE: str = ""
    METRO_PATH: str = ""
    TEST_END_TO_END: bool = True  # Do not query the SD server in tests.

    model_config = SettingsConfigDict(env_file=".env")
