import logging
from src.steps import upload_blob, yesterdays_listings, listing_to_dict, do
from src.models import Request
import pendulum
import funcy as fn
from src.config import PipelineConfig
import asyncio


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def main(date: pendulum.Date):
    listings = await asyncio.gather(*[do(page, date) for page in range(1, PipelineConfig.REVERB.max_pages)])
    flattened = fn.lflatten(listings)

    new_listings = fn.lfilter(
        lambda x: yesterdays_listings(x, date), flattened
    )

    serialised = fn.lmap(listing_to_dict, new_listings)
    upload_blob(serialised, f"data/pedals/{date.strftime('%Y/%m/%d')}/data.jsonl")


def SaveReverbListingsToGCS(event, context):
    try:
        payload = Request()
        asyncio.run(main(payload.date))
    except Exception as err:
        logger.error(err)
        raise
