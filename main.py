"""
ファイルアップロード時のベクトル化とLLM関連の中継エンドポイント
"""

from typing import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from utils import get_logger
from utils import EmbedPayload, QueryPayload
from utils import embed_process, query_process

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    APIサーバーの起動時、終了時の動作を実装。
    yieldの上が起動時に実行する処理、
    yieldの下が終了時に実行する処理。

    :param app: FastAPI
    :return: AsyncGenerator[None, None]
    """

    logger.info('===== API server start =====')
    logger.info('API App: %s', app)
    yield
    logger.info('===== API server stop =====')


server = FastAPI(lifespan=lifespan)
server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@server.post('/embed')
async def embed(payload: EmbedPayload) -> JSONResponse:
    """
    ドキュメントをベクトル化してDBに保存する機能を提供するエンドポイント。
    payloadにFirebaseStorageのパスとUserIDを格納している。

    payload.path ... FirebaseStorageの保存先
    payload.uid  ... UserID

    :param payload: EmbedPayload
    :return: JSONResponse
    """

    try:
        logger.info('Embed request received: %s', payload.model_dump())

        # TODO Embed処理実装
        result = embed_process(payload)
        if result is None:
            raise RuntimeError('Query failed')

        logger.info('Embed successfully: %s', result)
        return JSONResponse(
            status_code=200,
            content={'message': 'Embed successfully'}
        )
    except Exception as e:
        logger.error('Embed failed')
        logger.exception(e)
        return JSONResponse(
            status_code=500,
            content={'message': 'Internal Server Error', 'details': str(e)}
        )


@server.post('/query')
async def query(payload: QueryPayload) -> JSONResponse:
    """
    チャットボット経由でメッセージをLLMに投げ、返答内容を返すエンドポイント。
    payloadにメッセージとUserIDを格納している。

    payload.message ... ユーザーがBotに与えたメッセージ
    payload.uid     ... UserID

    :param payload: QueryPayload
    :return: JSONResponse
    """

    try:
        logger.info('Query request received: %s', payload.model_dump())
        logger.info(payload)

        # TODO Query処理実装
        result = query_process(payload)
        if result is None:
            raise RuntimeError('Query failed')

        logger.info('Query successfully: %s', result)
        return JSONResponse(
            status_code=200,
            content={'message': 'Query successfully'}
        )
    except Exception as e:
        logger.error('Query failed')
        logger.exception(e)
        return JSONResponse(
            status_code=500,
            content={'message': 'Internal Server Error', 'details': str(e)}
        )
