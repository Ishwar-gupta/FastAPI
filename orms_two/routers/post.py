from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,oauth2
from sqlalchemy.orm import Session
from .. database import get_db
from typing import List,Optional

router=APIRouter(
    prefix="/posts",  # we don't need to declare "/posts" in every decorators simply
    tags=['Posts']   # it differentiate the Posts and User documentation in Swagger UI
)

@router.get("/",response_model=List[schemas.Post])
# def get_posts(db: Session= Depends(get_db),current_user:schemas.TokenData=Depends(oauth2.get_current_user)):
# if we want only speicfic posts or skip the posts then ->
def get_posts(db:Session=Depends(get_db),current_user:schemas.TokenData=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    ''' checking in url ->
{{{URL}}}posts  => gives default 10 posts from top because it specified in funx.
{{{URL}}}posts?limit=3 => gives top 3 posts
{{{URL}}}posts?limit=5&skip=2 => skip top 2 posts & return remaining top 5 posts
{{URL}}posts?limit=5&skip=0&search=Random 
{{URL}}posts?search=Random   && {{URL}}posts?search=Random%20Post4
for spaces :->   %20  i.e {{URL}}posts?limit=5&skip=0&search=Random%20Post1
    '''
    # posts=db.query(models.Post).limit(limit).all()  # for limit method
    # posts=db.query(models.Post).limit(limit).offset(skip).all()  # for skipping the post
    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  # this is for searching by title

    # to get all posts at a time josukai owner hos then
    # posts=db.query(models.Post).all()
    return posts
'''But if wa want to get such posts who actuall owns that posts then syntax is:  '''
    # posts=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()

# # searching posts with id

@router.get("/{id}", response_model=schemas.Post)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found."
        )
    return post

''' if we want to get post only owner_user then it's syntax:   '''
    # if post.owner_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to get this post."
    #     )



 
# creating post using orms model
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:schemas.TokenData=Depends(oauth2.get_current_user)):
    new_post=models.Post(owner_id=current_user.id ,**post.model_dump())
    # print(current_user.email)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # returning back
    return new_post

# deleting posts
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int , db:Session=Depends(get_db),current_user:schemas.TokenData=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==id)
    post=post.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} doesn't exists.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )

    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# # updating post
# @router.put("/{id}",response_model=schemas.Post)
# def update_post(id:int,updated_post:schemas.PostCreate, db:Session=Depends(get_db),current_user:schemas.TokenData=Depends(oauth2.get_current_user)):
#     post_query=db.query(models.Post).filter(models.Post.id==id)
#     post=post_query.first()

#     if post == None: # if post doesn't exists
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} doesn't exists.")
    
#     post_query.update(updated_post.model_dump(),synchronize_session=False)
#     db.commit()

#     return post_query.first()



# UPDATE POST (Only owner)
@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user)
):
    post = db.query(models.Post).filter(
        models.Post.id == id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )

    for key, value in updated_post.model_dump().items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return post

