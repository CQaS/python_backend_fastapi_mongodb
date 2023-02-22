from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.cliente import db_cliente
from db.schemas.user import user_schema, users_schema
from bson import ObjectId


router = APIRouter(
    prefix='/userdb',
    tags=['userdb'],
    responses={
        status.HTTP_404_NOT_FOUND: {
            'msg': 'Not Found'
        }
    }
)


@router.get('/', response_model=list[User])
async def users():
    return users_schema(db_cliente.users.find())


@router.get('/{id}')
async def user(id: str):
    return search_user('_id', ObjectId(id))


@router.get('/')
async def user(id: str):
    return search_user('_id', ObjectId(id))


@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def userAdd(user: User):
    if type(search_user('mail', user.mail)) == User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Usuario ya esta')

    user_dic = dict(user)
    del user_dic['id']

    id = db_cliente.users.insert_one(user_dic).inserted_id
    new_user = user_schema(db_cliente.users.find_one({'_id': id}))

    return User(**new_user)


@router.put('/', response_model=User)
async def userAp(user: User):

    user_dic = dict(user)
    del user_dic['id']

    try:
        db_cliente.users.find_one_and_replace(
            {'_id': ObjectId(user.id)}, user_dic)
    except:
        return {'err': 'Usuario no actualizado'}

    return search_user('_id', ObjectId(user.id))


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def userDel(id: str):

    found = db_cliente.users.find_one_and_delete({'_id': ObjectId(id)})

    if not found:
        return {'err': 'Usuario no esta'}


def search_user(field: str, key):

    try:
        u = db_cliente.users.find_one({field: key})
        return User(**user_schema(u))
    except:
        return {'err': 'Usuario no esta'}
