from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import require_admin
from ..models import BorrowRequest, User
from ..schemas import BorrowOut, BorrowStatusIn, UserOut
router = APIRouter(prefix="/admin", tags=["Administration"])
@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return db.scalars(select(User).order_by(User.id.desc())).all()
@router.get("/borrow-requests", response_model=list[BorrowOut])
def list_borrow_requests(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return db.scalars(select(BorrowRequest).order_by(BorrowRequest.requested_at.desc())).all()
@router.patch("/borrow-requests/{request_id}", response_model=BorrowOut)
def update_borrow_request(request_id: int, data: BorrowStatusIn, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    req = db.get(BorrowRequest, request_id)
    if not req: raise HTTPException(status_code=404, detail="Borrow request not found")
    req.status = data.status; db.commit(); db.refresh(req); return req
