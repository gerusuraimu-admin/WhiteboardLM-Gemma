# テスト用import
from random import choice

from typing import Optional
from utils import QueryPayload


def query_process(payload: QueryPayload):
    return test_query(payload)


# テスト実行用関数
def test_query(_) -> Optional[bool]:
    _list = [True, None]
    return choice(_list)
