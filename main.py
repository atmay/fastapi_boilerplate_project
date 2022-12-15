import fastapi
import fastapi as _fastapi
import sqlalchemy.orm as _orm

import services
import schemas

app = _fastapi.FastAPI()
services.create_database()


@app.post("/users/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, db: _orm.Session = _fastapi.Depends(services.get_db)
):
    db_user = services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail=f"The user with email {user.email} already exists!"
        )
    return services.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(
    skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(services.get_db)
):
    return services.get_users(skip=skip, limit=limit, db=db)


@app.get("/users/{user_id}/", response_model=schemas.User)
def read_user(user_id: int, db: _orm.Session = _fastapi.Depends(services.get_db)):
    db_user = services.get_user_by_id(user_id=user_id, db=db)
    if not db_user:
        raise fastapi.HTTPException(
            status_code=404, detail=f"User with id {user_id} does not exist"
        )
    return db_user


@app.post("/users/{user_id}/posts/", response_model=schemas.Post)
def create_post(
    user_id: int,
    post: schemas.PostCreate,
    db: _orm.Session = _fastapi.Depends(services.get_db),
):
    db_user = services.get_user_by_id(user_id=user_id, db=db)
    if not db_user:
        raise fastapi.HTTPException(
            status_code=404, detail=f"User with id {user_id} does not exist"
        )
    return services.create_post(user_id=user_id, db=db, post=post)


@app.get("/posts/", response_model=list[schemas.Post])
def read_posts(
    skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(services.get_db)
):
    return services.get_posts(skip=skip, limit=limit, db=db)


@app.get("/posts/{post_id}/", response_model=schemas.Post)
def read_post(post_id: int, db: _orm.Session = _fastapi.Depends(services.get_db)):
    db_post = services.get_post(db=db, post_id=post_id)
    if not db_post:
        raise fastapi.HTTPException(
            status_code=404, detail=f"Post with id {post_id} does not exist"
        )
    return db_post


@app.delete("/posts/{post_id}/")
def delete_post(post_id: int, db: _orm.Session = _fastapi.Depends(services.get_db)):
    services.delete_post(db=db, post_id=post_id)
    return {"message": f"Successfully deleted post with id {post_id}"}


@app.put("/posts/{post_id", response_model=schemas.Post)
def update_post(
    post_id: int,
    post: schemas.PostCreate,
    db: _orm.Session = _fastapi.Depends(services.get_db),
):
    return services.update_post(post_id=post_id, db=db, post=post)
