from functools import lru_cache
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

@lru_cache
def get_settings():
    """
    This will create only one instance of a class and return the same object in the next requests.
    """
    return AppSettings()

class AppSettings(BaseSettings):
    app_name: str = "Flyer Generator Rest API"
    MAX_BATCH_SIZE: int = 5
    MAX_IN_MEMORY: int = 3000
    STABLE_DIFFUSION_INSTANCE: str = ""
    METRO_PATH: str = ""
    # Do not query the SD server in tests.
    TEST_END_TO_END: bool = True  
    # This service has a single API key, which provides basic access control
    # for endpoint request but is meaningless if the master key is compromised. 
    #
    # This is a secure default to avoid insecure deployments.
    #
    # A future alternative to this would be to require user authentication 
    # in order to access the endpoint.
    API_MASTER_KEY: SecretStr = SecretStr(str(hash(os.urandom(32)))) 

    model_config = SettingsConfigDict(env_file=".env")

    def is_api_key(self, received: str) -> bool:
        return self.API_MASTER_KEY.get_secret_value() == received

