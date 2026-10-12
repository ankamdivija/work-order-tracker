import time
from typing import Annotated, Optional
from fastapi import Depends, FastAPI, Request
from app.exceptions.handlers import register_exception_handlers
from app.routers.work_order import router as workorder_router

from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Work Order Tracker",
    version="1.0.0",
    )


register_exception_handlers(app)

app.include_router(workorder_router)

# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     start_time = time.time()

#     response = await call_next(request)

#     process_time = time.time() - start_time

#     print(
#         f"{request.method} "
#         f"{request.url.path} "
#         f"took {process_time:.4f} seconds"
#     )

#     return response


@app.get("/")
def home():
    return {"message": "AI Career Quest API is running!"}


@app.get("/health")
def health():
    return {"status": "healthy"}

# 1. Define your dependency function
def query_extractor(q: Optional[str] = None, skip: int = 0, limit: int = 10):
    return {"q": q, "skip": skip, "limit": limit}

# 2. Create a reusable type alias for cleaner route signatures
CommonsDep = Annotated[dict, Depends(query_extractor)]

@app.get("/items/")
async def read_items(commons: CommonsDep):
    # 'commons' is automatically populated with the dict returned by query_extractor
    return commons