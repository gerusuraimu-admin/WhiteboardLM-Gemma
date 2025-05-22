from typing import List
import magic
from google.cloud import storage, firestore
from utils.Payload import EmbedPayload
from utils.DataParser import DocType

db = firestore.Client()


def embed_process(payload: EmbedPayload) -> List[List[float]]:
    # data: bytes = read_file_from_gcs(payload.path, os.environ['BUCKET'])
    data: bytes = read_file_from_gcs(payload.path, 'whiteboardlm-v1')
    mime: str = detect_mime(data)
    doc_type: DocType = DocType.from_mime(mime)
    vectors: List[List[float]] = doc_type.handler(data)

    if not vectors:
        raise ValueError('Vectors cannot be empty')

    save_embedding(payload, vectors)
    return vectors


def save_embedding(payload: EmbedPayload, embedding: List[List[float]]):
    try:
        doc_id = '_'.join(payload.path.split('/')[1:])
        print(doc_id)  # doc_idが正常なフォーマットか確認したい。
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
