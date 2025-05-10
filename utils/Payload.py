from pydantic import BaseModel


class EmbedPayload(BaseModel):
    path: str
    uid: str


class QueryPayload(BaseModel):
    message: str
    uid: str
