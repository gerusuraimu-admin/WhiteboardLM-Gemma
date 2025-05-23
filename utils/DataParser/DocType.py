from enum import Enum
from typing import Callable
from utils.DataParser.TextParser import text2vec


class DocType(Enum):
    txt = ('text/plain', text2vec)

    def __init__(self, mime: str, handler: Callable) -> None:
        self.mime = mime
        self.handler = handler

    @classmethod
    def from_mime(cls, mime_type: str) -> 'DocType':
        for doc_type in cls:
            if doc_type.mime == mime_type:
                return doc_type

        raise TypeError('ファイルタイプが判定できませんでした')
