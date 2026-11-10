from sqlalchemy import select
from sqlalchemy.orm import Session
from .config import ADMIN_EMAIL, ADMIN_PASSWORD
from .models import User
from .security import hash_password
def ensure_admin(db: Session) -> None:
    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        return
    user = db.scalar(select(User).where(User.email == ADMIN_EMAIL))
    if user:
        if user.role != "admin":
            user.role = "admin"
            db.commit()
        return
    db.add(User(full_name="Library Administrator", email=ADMIN_EMAIL,
                password_hash=hash_password(ADMIN_PASSWORD), role="admin", is_active=True))
    db.commit()
