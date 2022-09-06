# FastAPI Application Documentation

This is an API application developed in Python's FastAPI. It used postgresql as database.

This application has below functionalities-

1. Create/update/delete/view a post.
2. View all posts from all users.
3. View single post from any user.
4. Create/get user.
5. Login and authentication using bcrypt and JWT (oauth).
6. Health check endpoint.
7. Validate the request and response paylaods to get only required fields and in declared format only. Otherwise error response will be sent.

## Healthcheck

```none
Endpoint    : GET /api/health
Description : Check if an API is online or not
Returns     : "OK"
```

## Connecting to the database

We are using SQLAlchemy for dealing with databases. We create a session to do database operations. For every API call we give this session object to the process as dependency and close the session as process closes.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASS}@{HOST}/{DATABASE}"

# Set up database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()


def connect_to_postgres_db():
    """
    Create postgres session

    Yields:
        sqlalchemy.orm.session.Session: Postgres Session Object
    """
    database = session_local()
    try:
        yield database

    except Exception as error:
        print("Error occured ==>", error)

    finally:
        database.close()
```

```python
# Using database dependency for API calls and its operations

from fastapi import  Depends

@router.get("/{user_id}", response_model=users_model.UserResponse)
def get_user(user_id: int, database: Session = Depends(connect_to_postgres_db)):
    user = users_model.get_user(user_id, database)
    return user
```

## Users

### User Schemas

```python
# Postgresql "Users" Model
*id
email
password
created_at
updated_at


# Data Validators (pydantic)
# 1. Create user request
    email: EmailStr
    password: str

# 2. User GET request response
    id: int
    email: EmailStr
    created_at: datetime

```

#### Create a New User

```none
Endpoint    : POST /api/users
Description : Create a new user.
Body        :
{
    "email": "new.user@email.com",
    "password": "secretPassword"
}

Returns     : [201 Created]
{
    "id": 3,
    "email": "new.user@email.com",
    "created_at": "2022-08-28T00:36:38.804486+05:30"
}

Error Resp  : [409 Conflict]
{
    "detail": "User already exists!"
}
```

Hash The Password

```python
from passlib.context import CryptContext

# Default hashing algorithm to use
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
return pwd_context.hash(password)
```

#### Get a user

```none
Endpoint    : GET /api/users/<id>
Description : Get a user by id. [*testing functionality]

Returns     : [200 OK]
{
    "id": 3,
    "email": "new.user@email.com",
    "created_at": "2022-08-28T00:36:38.804486+05:30"
}

Error Resp  : [404 Not Found]
{
    "detail": "User not found!"
}
```

## Authentication

### Login User

```none
Endpoint    : POST /api/login/
Description : Login User

Form Fields :
username => new.user@email.com
password => secretPassword

Returns     : [200 OK]
{
    "access_token": "really_long_token",
    "token_type": "bearer"
}

Error Resp  : [403 Forbidden]
{
    "detail": "Invalid Credentials"
}
```

Verify Password

```python
pwd_context.verify(plain_pass, hashed_pass)
```

Generating JWT Token

```python
from fastapi.security.oauth2 import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

data = {"user_id": user.id}
expire = datetime.utcnow() + timedelta(minutes=constants.ACCESS_TOKEN_EXPIRE_MINUTES)
to_encode.update({"exp": expire})

return jwt.encode(
    to_encode, constants.JWT_SECRET_KEY, algorithm=constants.JWT_ALOGORITHM
)
```

Verify JWT Token, parse it and return user_id from it

```python

credentials_exceptions = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(
            token, constants.JWT_SECRET_KEY, algorithms=constants.JWT_ALOGORITHM
        )

        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exceptions

        token_data = users_model.TokenData(id=user_id)
        return database.query(users_model.User).filter(users_model.User.id == token.id).first()

    except JWTError as error:
        print("JWT error!", error)
        raise credentials_exceptions from error
```

## Posts

### Post Schemas

```python
# Postgresql "Posts" Model
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

*id
title
content
published
created_at
updated_at
owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
owner = relationship("User")


# Data Validators (pydantic)
# 1. Create and update posts request
    title: str
    content: str
    published: bool = True

# 2. Post GET request response
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime | None
    owner: UserResponse

    class Config:
        """Configuration for the pydantic schema"""

        orm_mode = True  # This takes a SQLAlchemy response instead of dict[default]
```

Using JWT to verify logged in user's authentication as dependency.

```python
from app.Utils import oauth2

@router.get("/", response_model=list[posts_model.PostResponse])
def get_posts(
    database: Session = Depends(connect_to_postgres_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    posts = posts_model.get_all_posts(database)
    return posts
```

#### Create a post

```none
Endpoint    : POST /api/posts/
Description : Create a Post
Bearer Auth : JWT_token
Body        :
{
    "title": "New post this is new post",
    "content": "new posts after another! Its still coming!",
    "published": false
}

Returns     : [200 OK]
{
    "title": "New post this is new post",
    "content": "new posts after another! Its still coming!",
    "published": false,
    "id": 6,
    "owner_id": 1,
    "created_at": "2022-08-28T10:57:30.594404+05:30",
    "updated_at": null,
    "owner": {
        "id": 1,
        "email": "piyush123.user@email.com",
        "created_at": "2022-08-17T23:09:01.482465+05:30"
    }
}

Error Resp  : [401 Unauthorized]
{
    "detail": "Not authenticated"
}
```

#### Update a post

```none
Endpoint    : PUT /api/posts/<id>
Description : Update a Post
Bearer Auth : JWT_token
Body        :
{
    "title": "Updated this post as well",
    "content": "This is my first post. Its amazing!"
}

Returns     : [200 OK]
{
    "title": "Updated this post as well",
    "content": "This is my first post. Its amazing!",
    "published": true,
    "id": 7,
    "owner_id": 1,
    "created_at": "2022-08-28T11:07:17.219483+05:30",
    "updated_at": "2022-08-28T11:11:34.686644+05:30",
    "owner": {
        "id": 1,
        "email": "piyush123.user@email.com",
        "created_at": "2022-08-17T23:09:01.482465+05:30"
    }
}

Error Resp  : [401 Unauthorized]
{
    "detail": "Not authenticated"
}

Error Resp  : [404 Not Found]
{
    "detail": "Post not found!"
}
```

#### Delete a post

```none
Endpoint    : DELETE /api/posts/<id>
Description : Delete a Post
Bearer Auth : JWT_token
Returns     : [204 No Content]

Error Resp  : [401 Unauthorized]
{
    "detail": "Not authenticated"
}

Error Resp  : [404 Not Found]
{
    "detail": "Post not found!"
}
```

#### Get a post

```none
Endpoint    : GET /api/posts/<id>
Description : Get a Post
Returns     : [200 OK]
{
    "title": "New post",
    "content": "new posts after another! Its still coming!",
    "published": false,
    "id": 2,
    "owner_id": 1,
    "created_at": "2022-08-17T23:10:46.129324+05:30",
    "updated_at": null,
    "owner": {
        "id": 1,
        "email": "piyush123.user@email.com",
        "created_at": "2022-08-17T23:09:01.482465+05:30"
    }
}

Error Resp  : [404 Not Found]
{
    "detail": "Post not found!"
}
```

#### Get all post

```none
Endpoint    : GET /api/posts/
Description : Get all Post
Returns     : [200 OK]
[
    {
        "title": "New post",
        "content": "new posts after another! Its still coming!",
        "published": false,
        "id": 2,
        "owner_id": 1,
        "created_at": "2022-08-17T23:10:46.129324+05:30",
        "updated_at": null,
        "owner": {
            "id": 1,
            "email": "piyush123.user@email.com",
            "created_at": "2022-08-17T23:09:01.482465+05:30"
        }
    },
    {
        "title": "New post",
        "content": "new posts after another! Its still coming!",
        "published": false,
        "id": 3,
        "owner_id": 1,
        "created_at": "2022-08-17T23:12:13.297153+05:30",
        "updated_at": null,
        "owner": {
            "id": 1,
            "email": "piyush123.user@email.com",
            "created_at": "2022-08-17T23:09:01.482465+05:30"
        }
    }
]

Error Resp  : [404 Not Found]
{
    "detail": "Post not found!"
}
```


#### Pagination and string based searching

Query params
1. limit: Number of results to return.
2. skip: Number of results to skip.
3. search: Search for given string in the records.

```none
Endpoint    : GET /api/posts/?limit=10&size=2?search="beach"
```

## NOT Found

Response

```none
Resp  : [404 Not Found]
{
    "detail": "Not Found"
}
```


## Votes

### Vote Schemas

```python
# Postgresql "Posts" Model
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

*post_id: ForeignKey("posts.id", ondelete="CASCADE")
*user_id: ForeignKey("users.id", ondelete="CASCADE")
liked_at


# Data Validators (pydantic)
# 1. Vote Request
    post_id: int
    dir: int

    @validator("dir")
    def validate_vote_type(cls, val):
        """ Validate vote type """
        if val not in [0, 1]:
            raise ValueError("Vote type should be either 0 or 1!")
        return val
```
#### Add/remove a vote

```none
Endpoint    : GET /api/vote/
Description : Add/remove a vote on a post
Bearer Auth : JWT_token
Body        :
{
    "psot_id": 19,
    "dir": 0|1
}

# User_id is extracted from the JWT_TOKEN

Returns     : [200 OK]
{
    "title": "Updated this post as well",
    "content": "This is my first post. Its amazing!",
    "published": true,
    "id": 7,
    "owner_id": 1,
    "created_at": "2022-08-28T11:07:17.219483+05:30",
    "updated_at": "2022-08-28T11:11:34.686644+05:30",
    "owner": {
        "id": 1,
        "email": "piyush123.user@email.com",
        "created_at": "2022-08-17T23:09:01.482465+05:30"
    }
}

Error Resp  : [401 Unauthorized]
{
    "detail": "Not authenticated"
}

Error Resp  :
[404 Not Found] : { "detail": "Post does not exists!" }
[409 conflict]  : { "detail": "Cannot vote already voted post!" }
[409 conflict]  : { "detail": "Cannot down-vote a not voted this post!" }
```
