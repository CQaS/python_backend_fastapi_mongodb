from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import products, users, basic_auth, jwt_auth, users_db

app = FastAPI()

# routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth.router)
app.include_router(jwt_auth.router)
app.include_router(users_db.router)

app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/')
async def root():
    return 'Hola'


@app.get('/url')
async def root():
    return [{'url': 'HTTP'},
            {'url': 'HTTP'}, ]
