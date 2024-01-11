import dataclasses
import logging
from datetime import datetime
from enum import Enum
import tempfile

import firebase_admin
from firebase_admin import firestore, credentials

from services.settings import settings


class FirestoreCollections(str, Enum):
    patent = "patent"


class StoredFieldName(str, Enum):
    uploaded_at = "uploaded_at"
    patent_id = "patent_id"
    content = "content"
    post_id = "post_id"


@dataclasses.dataclass
class UploadedRecord:
    uploaded_at: datetime
    patent_id: str
    content: str
    post_id: str

    def to_dict(self):
        return {
            StoredFieldName.uploaded_at: self.uploaded_at.isoformat(),
            StoredFieldName.patent_id: self.patent_id,
            StoredFieldName.content: self.content,
            StoredFieldName.post_id: self.post_id,
        }


class FirebaseClient:
    _client = None

    @classmethod
    def start(cls, credentials_json: str = None):
        credentials_json = credentials_json or settings.config.GCP__CREDENTIALS_JSON
        if FirebaseClient._client is None:
            tmp = tempfile.NamedTemporaryFile(mode="w", delete=False)

            with open(tmp.name, "w") as f:
                f.write(credentials_json)
            cred = credentials.Certificate(tmp.name)
            firebase_admin.initialize_app(cred)
            FirebaseClient._client = firestore.client()

    @property
    def client(self):
        if FirebaseClient._client is None:
            raise Exception("Collection not started yet")
        return FirebaseClient._client


def get_collection(client):
    return client.collection(FirestoreCollections.patent)


firebase_client = FirebaseClient()


def save(record: UploadedRecord):
    logging.info("Saving a new record in firestore")
    get_collection(firebase_client.client).add(record.to_dict())
    logging.info("New records successfully saved")


def get_records() -> list[UploadedRecord]:
    logging.info("Getting records data from firestore")
    query = (
        get_collection(firebase_client.client)
        .order_by(StoredFieldName.uploaded_at, direction=firestore.Query.DESCENDING)
        .limit(5)
    )
    patents = query.stream()
    logging.info("Records successfully fetched")
    return [UploadedRecord(**p.to_dict()) for p in patents]
