from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={
        404: {
            'msg': 'Not Found'
        }
    }
)


class User(BaseModel):
    id: int
    name: str
    edad: int


users_list = [User(id=1, name='Leo', edad=20),
              User(id=2, name='Maru', edad=45)]


@router.get('/usersjson')
async def userjson():
    return [{'name': 'Ale', 'edad': 39},
            {'name': 'Alex', 'edad': 18}]


@router.get('/')
async def users():
    return users_list

# Path


@router.get('/{id}')
async def user(id: int):
    return search_user(id)

# Query


@router.get('/')
async def user(id: int):
    return search_user(id)


@router.post('/', response_model=User, status_code=201)
async def userAdd(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail='Usuario ya esta')

    users_list.routerend(user)
    return user


@router.put('/')
async def userAp(user: User):
    found = False

    for i, guardar in enumerate(users_list):
        if guardar.id == user.id:
            users_list[i] = user
            found = True

            return user
    if not found:
        return {'err': 'Usuario no esta'}


@router.delete('/{id}')
async def userDel(id: int):
    found = False
    for i, guardar in enumerate(users_list):
        if guardar.id == id:
            del users_list[i]
            found = True

    if not found:
        return {'err': 'Usuario no esta'}


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {'err': 'Usuario no esta'}
