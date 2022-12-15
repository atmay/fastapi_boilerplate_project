import datetime as dt
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
import models
import schemas


def create_database():
    return Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    db_user = db.query(models.User).filter(models.User.email == email).first()
    return db_user


def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    return db_user


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hash_pwd = user.password  # TODO hash passwords!
    db_user = models.User(email=user.email, hashed_password=hash_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int, limit: int) -> list[models.User | None]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_post(db: Session, post: schemas.PostCreate, user_id: int):
    post = models.Post(**post.dict(), owner_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_posts(db: Session, skip: int, limit: int) -> list[models.Post | None]:
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_post(db: Session, post_id: int) -> models.Post | None:
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def delete_post(db: Session, post_id: int) -> None:
    db.query(models.Post).filter(models.Post.id == post_id).delete()
    db.commit()


def update_post(db: Session, post_id: int, post: schemas.PostCreate) -> models.Post:
    db_post = get_post(db=db, post_id=post_id)
    db_post.title = post.title
    db_post.content = post.content
    db_post.date_last_updated = dt.datetime.now()
    db.commit()
    db.refresh(db_post)
    return db_post
