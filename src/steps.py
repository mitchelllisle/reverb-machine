import httpx
from src.config import PipelineConfig
from src.models import ReverbListings, ReverbListing
from typing import List, Dict
import pendulum
from src import logger
import jsonlines
from io import StringIO


async def do(page, date):
    listings = await get_reverb_listings(page)
    return listings


def yesterdays_listings(listing: ReverbListing, date: pendulum.Date):
    diff = date.diff(listing.created_at, abs=False)
    if diff.days == -1:
        return True
    else:
        return False


async def get_reverb_listings(page: int, category: str = "effects-and-pedals") -> List[ReverbListing]:
    logger.info(f"Fetching page {page} for {category}")
    querystring = {
        "product_type": category,
        "per_page": "40",
        "page": page,
        "sort": "published_at%7Cdesc"
    }

    headers = {
        'accept-version': "3.0",
        'content-type': "application/hal+json",
        'accept': "application/hal+json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PipelineConfig.REVERB.url}/listings/all", headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
    return ReverbListings(**data).listings


def listing_to_dict(listing: ReverbListing) -> Dict:
    element = listing.dict()
    element["created_at"] = str(listing.created_at)
    element["published_at"] = str(listing.published_at)
    return element


def write_to_jsonlines(elements: List[Dict]):
    buffer = StringIO()
    writer = jsonlines.Writer(buffer)
    writer.write_all(elements)
    return buffer.getvalue()


def upload_blob(data, destination_blob_name: str) -> str:
    blob = PipelineConfig.GOOGLE.bucket.blob(destination_blob_name)
    file_buffer = write_to_jsonlines(data)
    blob.upload_from_string(file_buffer)
    return destination_blob_name
