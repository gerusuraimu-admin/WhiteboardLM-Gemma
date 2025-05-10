# WhiteboardLM-Gemma

## 概要
WhiteboardLM-Gemmaは、ドキュメントのベクトル化とLLM（大規模言語モデル）を活用したチャットボット機能を提供するAPIサーバーです。

## main.py
main.pyは、FastAPIを使用したAPIサーバーの実装です。以下の機能を提供しています。

### エンドポイント

#### `/embed` (POST)
ドキュメントをベクトル化してデータベースに保存するエンドポイント。

**リクエスト形式**:
```json
{
  "path": "FirebaseStorageのパス",
  "uid": "ユーザーID"
}
```

**レスポンス**:
- 成功時: `{"message": "Embed successfully"}`
- 失敗時: `{"message": "Internal Server Error", "details": "エラー詳細"}`  
※失敗時のレスポンスは暫定的。

#### `/query` (POST)
ユーザーのメッセージをLLMに送信し、応答を返すエンドポイント。

**リクエスト形式**:
```json
{
  "message": "ユーザーのメッセージ",
  "uid": "ユーザーID"
}
```

**レスポンス**:
- 成功時: `{"message": "Query successfully"}`
- 失敗時: `{"message": "Internal Server Error", "details": "エラー詳細"}`  
※失敗時のレスポンスは暫定的。

### サーバー起動方法
```bash
uvicorn main:server --reload
```

## 依存関係
- fastapi
- pydantic
- uvicorn[standard]
- python-magic

## 開発状況
現在、`embed_process`と`query_process`の実装は開発中です。テスト用の実装が含まれています。
