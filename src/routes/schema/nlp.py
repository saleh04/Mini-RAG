from pydantic import BaseModel


class PushRequest(BaseModel):
    do_reset: bool| None = None

class SearchRequest(BaseModel):
    query: str
    limit: int | None = 5