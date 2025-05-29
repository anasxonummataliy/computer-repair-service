from pydantic import BaseModel


class VisitorStats(BaseModel):
    date: str
    count: int


class LocationStats(BaseModel):
    source: str
    count: int


class RequestStats(BaseModel):
    total_requests: int
    pending_requests: int
    in_progress_requests: int
    completed_requests: int

