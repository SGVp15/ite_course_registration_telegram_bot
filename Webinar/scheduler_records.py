import asyncio

from Utils.log import log
from Webinar import WebinarApi
from Webinar.config import WEBINAR_TOKENS


async def scheduler_converter_records():
    log.info('scheduler_record_to_conversions run')
    while True:
        for token in WEBINAR_TOKENS:
            webinar_api = WebinarApi(token)
            records: [dict] = webinar_api.get_records_list()
            if records:
                for r in records:
                    record_id = r.get('id')
                    if record_id:
                        log.info(f'Record {record_id} to converter = {webinar_api.post_record_to_conversions(record_id)}')
        await asyncio.sleep(10 * 60)
