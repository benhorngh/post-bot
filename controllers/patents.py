import logging
from datetime import datetime
from typing import Optional

from services import data_fetch
from services import firebase_client
from services import twitter_client
from services.post_builder import patent_post


def start():
    firebase_client.firebase_client.start()
    twitter_client.twitter_client.start()
    upload_new_patents()


def upload_new_patents():
    logging.info("Start upload new patent")
    patents = data_fetch.get_patents()
    new_patent = _find_new_patent(patents)
    if new_patent:
        _handle_new_patent(new_patent)
        logging.info("Patent posted!")
    else:
        logging.info("No new patents")
    logging.info("Done")


def _handle_new_patent(new_patent: data_fetch.CPCPatent):
    content = patent_post.build_post(new_patent)
    post_id = twitter_client.post_tweet(content)
    new_record = firebase_client.UploadedRecord(
        patent_id=new_patent.patent_id,
        content=content,
        uploaded_at=datetime.utcnow(),
        post_id=post_id,
    )
    firebase_client.save(new_record)


def _find_new_patent(
        patents: list[data_fetch.CPCPatent]) -> Optional[data_fetch.CPCPatent]:
    for patent in patents:
        stored_patent = firebase_client.get_record(patent.patent_id)
        if not stored_patent:
            return patent
