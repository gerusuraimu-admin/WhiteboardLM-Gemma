from typing import List
from itertools import chain
import magic
from google.cloud import storage, firestore
from utils.Payload import EmbedPayload
from utils.DataParser import DocType

db = firestore.Client()


def embed_process(payload: EmbedPayload) -> List[List[float]]:
    # data: bytes = read_file_from_gcs(payload.path, os.environ['BUCKET'])
    data: bytes = read_file_from_gcs(payload.path, 'whiteboardlm-v1.firebasestorage.app')
    mime: str = detect_mime(data)
    print(f'mimetpye: {mime}')
    doc_type: DocType = DocType.from_mime(mime)
    vectors: List[List[float]] = doc_type.handler(data)

    if not vectors:
        raise ValueError('Vectors cannot be empty')
    flat_vectors: List[float] = list(chain.from_iterable(vectors))

    save_embedding(payload, flat_vectors)
    return vectors


def save_embedding(payload: EmbedPayload, embedding: List[float]):
    try:
        doc_id = '_'.join(payload.path.split('/')[1:])
        doc_ref = db.collection('documents').document(doc_id)

        if not doc_ref.get().exists:
            raise FileNotFoundError(f'Document not found: {doc_id}')

        doc_ref.set({'embedding': embedding}, merge=True)
    except Exception as e:
        raise RuntimeError(f'Failed to save embedding: {e}')


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
