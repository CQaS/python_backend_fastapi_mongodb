from fastapi import APIRouter

router = APIRouter(
    prefix='/products',
    tags=['products'],
    responses={
        404: {
            'msg': 'Not Found'
        }
    }
)

product_list = ['Producto1', 'Producto2', 'Producto3', 'Producto4', ]


@router.get('/')
async def root():
    return product_list


@router.get('/{id}')
async def root(id: int):
    return product_list[id]
