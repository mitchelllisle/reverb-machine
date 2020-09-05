from pydantic import BaseSettings, Field
from google.cloud import storage


class GoogleConfig(BaseSettings):
    BUCKET_NAME: str = Field(default="reverb-data", env="BUCKET_NAME")

    @property
    def bucket(self):
        client = storage.Client()
        return client.bucket(self.BUCKET_NAME)


class ReverbConfig(BaseSettings):
    url: str = Field(env="REVERB_URL", default="https://api.reverb.com/api")
    max_pages: int = Field(env="MAX_PAGES", default=100)


class PipelineConfig:
    REVERB = ReverbConfig()
    GOOGLE = GoogleConfig()
