from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITMO = 'HS256'
ACCESS_TOKEN_DURACION = 1
SECRET = '4e7d696bce894548dded72f6eeb04e8d625cc7f2afd08845824a4a8378b428d1'

router = APIRouter()

oauth = OAuth2PasswordBearer(tokenUrl='login')

cry = CryptContext(schemes=['bcrypt'])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


user_db = {
    'alef': {
        'username': 'alef',
        'full_name': 'aleFirma',
        'email': 'ale@mail.com',
        'disabled': False,
        'password': '$2a$12$7wiMhE1CGq27wUpkpaIBhuQANBPs4W1ZiowqPyIarYxVhkHb6t0aW'
    },
    'fiamC': {
        'username': 'fiamC',
        'full_name': 'fiamCon',
        'email': 'fiam@mail.com',
        'disabled': True,
        'password': '$2a$12$7wiMhE1CGq27wUpkpaIBhuQANBPs4W1ZiowqPyIarYxVhkHb6t0aW'
    },
}


def buscar(username: str):
    if username in user_db:
        return User(**user_db[username])


async def aut_user(token: str = Depends(oauth)):

    ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Usuario no Autorizado',
        headers={'WWW-Authenticate': 'Bearer'})

    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITMO).get('sub')
        if username is None:
            raise ex

    except JWTError:
        raise ex

    return buscar(username)


async def current_user(user: User = Depends(aut_user)):

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Usuario inactivo')

    return user


def buscar_db(username: str):
    if username in user_db:
        return UserDB(**user_db[username])


@router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_res = user_db.get(form.username)
    if not user_res:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Usuario no esta1')

    user = buscar_db(form.username)

    if not cry.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail='Usuario no esta2')

    access_token = {
        'sub': user.username,
        'exp': timedelta(minutes=ACCESS_TOKEN_DURACION)
    }

    return {'access_token': jwt.encode(access_token, SECRET, algorithm=ALGORITMO), 'token_type': 'bearer'}


@router.get('/users/yo')
async def yo(user: User = Depends(current_user)):
    return user
