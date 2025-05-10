from utils.DataParser import DocType


# TODO テキスト用ベクトル化処理実装予定

def text2vec(data: bytes) -> None:
    try:
        print(data)
    except Exception as e:
        raise RuntimeError(e)
