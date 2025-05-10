# テスト用import
from random import choice

from typing import Optional
from utils.Payload import EmbedPayload


def embed_process(payload: EmbedPayload):
    return test_embed(payload)


# テスト実行用関数
def test_embed(_) -> Optional[bool]:
    _list = [True, None]
    return choice(_list)
