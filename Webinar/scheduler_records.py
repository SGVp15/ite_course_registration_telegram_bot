import asyncio

from Utils.log import log
from Webinar import WebinarApi
from Webinar.config import WEBINAR_TOKENS


async def scheduler_converter_records():
    log.warning('scheduler_record_to_conversions run')
    record_id_list = []
    while True:
        for token in WEBINAR_TOKENS:
            webinar_api = WebinarApi(token)
            records: [dict] = webinar_api.get_records_list()
            if records:
                for r in records:
                    record_id = r.get('id')
                    if record_id and record_id not in record_id_list:
                        code, response = webinar_api.post_record_to_conversions(record_id)
                        record_id_list.append(record_id)
                        if code == 200:
                            log.info(f'[Records] {record_id} to converter = {response}')
                        else:
                            log.error(response)
        await asyncio.sleep(10 * 60)
