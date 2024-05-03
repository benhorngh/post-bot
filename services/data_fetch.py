"""https://data.gov.il/api/3/action/datastore_search?resource_id=b2c59e21-c345-4b02-b071-2890a3d431d6&limit=5"""

import dataclasses
import logging

import requests

RESOURCE_ID = "b2c59e21-c345-4b02-b071-2890a3d431d6"
FETCH_URL = "https://data.gov.il/api/3/action/datastore_search"


@dataclasses.dataclass
class CPCPatent:
    patent_id: str
    content: str

    def __init__(self, record: dict):
        self.patent_id = record.get("מספר בקשה")
        self.content = record.get("שם האמצאה בעברית")


PARAMS = {"resource_id": RESOURCE_ID, "limit": 5}


def get_patents():
    logging.info("Fetching patents data")
    res = requests.get(FETCH_URL, params=PARAMS)
    logging.info("Patent data successfully fetched")
    patents = [CPCPatent(p) for p in res.json()["result"]["records"]]
    patents.reverse()
    return patents
