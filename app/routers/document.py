from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import time

router = APIRouter(prefix="/documents", tags=["Documents"])


class SearchRequest(BaseModel):
    keyword: str
    doc_id: int


class AnswerResponse(BaseModel):
    answer: str
    confidence: float

def search_document(search_body:SearchRequest):
    print("Starting search for ", search_body.keyword)
    time.sleep(5)
    print("Search compelete")
    

@router.post("/search", response_model=AnswerResponse)
def search(search_body: SearchRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(search_document, search_body)
    answer = AnswerResponse(
        answer=f"This is serach router for {search_body.keyword}", 
        confidence=0.9)
    return answer


@router.get("/")
def get_documents():
    answer = AnswerResponse(
        answer="This is document router", 
        confidence=1.0)
    return answer