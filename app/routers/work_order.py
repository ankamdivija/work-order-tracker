from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel
from requests import Session

from app.exceptions.handlers import WorkOrderNotFoundError
from app.database import get_db
from app.models.work_order import WorkOrder
from app.schemas.work_order import WorkOrderCreate, WorkOrderResponse, WorkOrderStatusUpdate

router = APIRouter(prefix="/work-orders", tags=["Work Orders"])


@router.get(
    "/",
    response_model=list[WorkOrderResponse],
)
def list_work_orders(
    db: Session = Depends(get_db),
):
    work_orders = db.query(WorkOrder).order_by(WorkOrder.id).all()
    
    return work_orders

@router.post(
    "/",
    response_model=WorkOrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_work_order(
    work_order: WorkOrderCreate,
    db: Session = Depends(get_db),
):
    db_work_order = WorkOrder(
        title=work_order.title,
        description=work_order.description,
    )

    db.add(db_work_order)
    db.commit()
    db.refresh(db_work_order)

    return db_work_order



@router.get(
    "/{work_order_id}",
    response_model=WorkOrderResponse,
)
def get_work_order(
    work_order_id: int,
    db: Session = Depends(get_db),
):
    work_order = db.get(WorkOrder, work_order_id)
    if work_order is None:
        raise WorkOrderNotFoundError(work_order_id)

    return work_order


@router.patch(
    "/{work_order_id}/status",
    response_model=WorkOrderResponse,
)
def update_work_order_status(
    work_order_id: int,
    request: WorkOrderStatusUpdate,
    db: Session = Depends(get_db),
):
    work_order = db.get(WorkOrder, work_order_id)

    if work_order is None:
        raise WorkOrderNotFoundError(work_order_id)

    work_order.status = request.status.value

    db.commit()
    db.refresh(work_order)

    return work_order