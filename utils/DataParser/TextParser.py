# TODO テキスト用ベクトル化処理実装予定
from typing import List
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

def text2vec(data: bytes) -> List[List[float]]:
    try:
        text = data.decode('utf-8', errors='ignore')
        if not text:
            raise ValueError('テキスト抽出に失敗しました')

        return embedding(text)

    except Exception as e:
        raise RuntimeError(f'テキスト抽出エラー: {e}')

# Embedding処理
# TODO チャンク処理未実装
def embedding(text: str) -> List[List[float]]:
    dimensionality = 256
    task = 'RETRIEVAL_DOCUMENT'

    model = TextEmbeddingModel.from_pretrained('textembedding-gecko')
    inputs = [TextEmbeddingInput(text, task)]
    kwargs = dict(output_dimensionality=dimensionality) if dimensionality else {}
    embeddings = model.get_embeddings(inputs, **kwargs)

    return [embeddings.values for embeddings in embeddings]
