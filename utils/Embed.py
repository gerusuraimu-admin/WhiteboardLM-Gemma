import os
from typing import Tuple
import magic
from google.cloud import storage
from utils.Payload import EmbedPayload
from utils.DataParser import DocType


def embed_process(payload: EmbedPayload) -> Tuple[str, bytes]:
    data: bytes = read_file_from_gcs(payload.path, os.environ['BUCKET'])
    mime: str = detect_mime(data)
    doc_type: DocType = DocType.from_mime(mime)
    doc_type.handler(data)
    return mime, data


def read_file_from_gcs(path: str, bucket_name: str) -> bytes:
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(path)

        if not blob.exists():
            raise FileNotFoundError('GCSファイルが見つかりません')

        return blob.download_as_bytes()
    except Exception as e:
        raise RuntimeError(f"GCSファイル読み込み失敗: {e}")


def detect_mime(data: bytes) -> str:
    return magic.from_buffer(data, mime=True)
