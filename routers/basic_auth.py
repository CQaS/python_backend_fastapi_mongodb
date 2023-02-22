from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth = OAuth2PasswordBearer(tokenUrl='login')


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
        'password': '123456'
    },
    'fiamC': {
        'username': 'fiamC',
        'full_name': 'fiamCon',
        'email': 'fiam@mail.com',
        'disabled': True,
        'password': '123456'
    },
}


def buscar_db(username: str):
    if username in user_db:
        return UserDB(**user_db[username])


def buscar(username: str):
    if username in user_db:
        return User(**user_db[username])


async def current_user(token: str = Depends(oauth)):
    user = buscar(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuario no Autorizado',
            headers={'WWW-Authenticate': 'Bearer'})

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Usuario inactivo')

    return user


@router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_res = user_db.get(form.username)
    if not user_res:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Usuario no esta1')

    user = buscar_db(form.username)

    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail='Usuario no esta2')

    return {'access_token': user.username, 'token_type': 'bearer'}


@router.get('/users/yo')
async def yo(user: User = Depends(current_user)):
    return user
