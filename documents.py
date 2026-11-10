from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user, require_admin
from ..models import BorrowRequest, Document, User
from ..schemas import DocumentIn, DocumentOut, BorrowOut
router = APIRouter(tags=["Library documents"])
@router.get("/documents", response_model=list[DocumentOut])
def list_documents(search: str = "", category: str = "", db: Session = Depends(get_db)):
    stmt = select(Document).order_by(Document.title.asc())
    if search.strip():
        term = f"%{search.strip()}%"
        stmt = stmt.where(Document.title.ilike(term) | Document.author.ilike(term))
    if category.strip():
        stmt = stmt.where(Document.category.ilike(category.strip()))
    return db.scalars(stmt).all()
@router.get("/documents/{document_id}", response_model=DocumentOut)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc: raise HTTPException(status_code=404, detail="Document not found")
    return doc
@router.post("/documents", response_model=DocumentOut, status_code=201)
def add_document(data: DocumentIn, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    doc = Document(**data.model_dump()); db.add(doc); db.commit(); db.refresh(doc)
    return doc
@router.put("/documents/{document_id}", response_model=DocumentOut)
def update_document(document_id: int, data: DocumentIn, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    doc = db.get(Document, document_id)
    if not doc: raise HTTPException(status_code=404, detail="Document not found")
    for key, value in data.model_dump().items(): setattr(doc, key, value)
    db.commit(); db.refresh(doc); return doc
@router.delete("/documents/{document_id}", status_code=204)
def delete_document(document_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    doc = db.get(Document, document_id)
    if not doc: raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc); db.commit()
@router.post("/documents/{document_id}/borrow", response_model=BorrowOut, status_code=201)
def request_borrow(document_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    doc = db.get(Document, document_id)
    if not doc: raise HTTPException(status_code=404, detail="Document not found")
    if doc.available_copies < 1: raise HTTPException(status_code=409, detail="No copies are available")
    active = db.scalar(select(BorrowRequest).where(BorrowRequest.user_id == user.id,
        BorrowRequest.document_id == document_id, BorrowRequest.status.in_(["pending", "approved"])))
    if active: raise HTTPException(status_code=409, detail="You already have an active request")
    req = BorrowRequest(user_id=user.id, document_id=document_id)
    db.add(req); db.commit(); db.refresh(req); return req
@router.get("/my-requests", response_model=list[BorrowOut])
def my_requests(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.scalars(select(BorrowRequest).where(BorrowRequest.user_id == user.id)
                      .order_by(BorrowRequest.requested_at.desc())).all()
