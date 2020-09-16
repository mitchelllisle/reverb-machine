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
    max_retries: int = Field(env="MAX_RETRIES", default=3)


class AnomalyDetectionConfig(BaseSettings):
    model: str = Field(env="ANOMALY_MODEL_PATH", default="gs://reverb-data/models/anomaly.model")


class PipelineConfig:
    REVERB = ReverbConfig()
    GOOGLE = GoogleConfig()
    ANOMALY = AnomalyDetectionConfig()
