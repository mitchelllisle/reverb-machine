import logging
from src.steps import upload_blob, yesterdays_listings, listing_to_dict, do
from src.models import Request
import pendulum
import funcy as fn
from src.config import PipelineConfig
import asyncio
import json


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def main(date: pendulum.Date):
    listings = await asyncio.gather(*[do(page) for page in range(1, PipelineConfig.REVERB.max_pages)])
    flattened = fn.lflatten(listings)

    new_listings = fn.filter(
        lambda x: yesterdays_listings(x, date), flattened
    )

    serialised = fn.lmap(listing_to_dict, new_listings)
    logger.info(f"Found {len(serialised)} listings to be saved")
    upload_blob(serialised, f"data/pedals/{date.strftime('%Y/%m/%d')}/data.jsonl")


def SaveReverbListingsToGCS(request):
    try:
        req = Request()
        logger.info(f"Fetching listings for date: {req.date}")
        asyncio.run(main(req.date))
    except Exception as err:
        logger.error(err)
        raise


if __name__ == "__main__":
    SaveReverbListingsToGCS(None)
