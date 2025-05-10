# WhiteboardLM-Gemma

## 概要
WhiteboardLM-Gemmaは、ドキュメントのベクトル化とLLM（大規模言語モデル）を活用したチャットボット機能を提供するAPIサーバーです。

## 環境

### 開発環境
- macOS Sequoia 15.4.1
- Python3.12

### 動作環境
- Cloud Run
- python:3.12-slim

### 依存関係
- fastapi
- pydantic
- uvicorn[standard]
- python-magic
- google
- google-cloud-storage
- google-cloud-firestore
- firebase-admin

## main.py
main.pyは、FastAPIを使用したAPIサーバーの実装です。  
以下の機能を提供しています。

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
- 成功時: `{"message": "Embed successfully"}` (status code: 200)
- 失敗時:
  - FileNotFound: `{"message": "Embed failed", "details": "エラー詳細"}` (status code: 404)
  - その他のエラー: `{"message": "Internal Server Error", "details": "エラー詳細"}` (status code: 500)

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
- 成功時: `{"message": "Query successfully"}` (status code: 200)
- 失敗時: `{"message": "Internal Server Error", "details": "エラー詳細"}` (status code: 500)

### サーバー起動方法
```bash
uvicorn main:server --log-level critical --host 0.0.0.0 --port 8080
```

## 環境変数
- BUCKET: `${BucketName}.firebasestorage.app`

## 開発状況
- `embed_process`: Google Cloud Storageからファイルを読み込み、MIMEタイプを検出する基本実装が完了しています。ベクトル化とデータベース保存の機能は今後実装予定です。
- `query_process`: 現在はテスト用の実装のみで、ランダムに成功または失敗を返します。LLMとの連携機能は今後実装予定です。
