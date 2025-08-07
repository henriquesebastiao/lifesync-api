from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from lifesync.core.settings import get_settings
from lifesync.routes import token, user
from lifesync.routes.finance import accounts, quote


def custom_generate_unique_id(route: APIRoute):
    return f'{route.tags[0]}-{route.name}'


settings = get_settings()

app = FastAPI(
    docs_url='/',
    generate_unique_id_function=custom_generate_unique_id,
    title='LifeSync API',
    version=settings.VERSION,
    terms_of_service='https://github.com/henriquesebastiao/lifesync-api/blob/main/LICENSE',
    contact={
        'name': 'LifeSync',
        'url': 'https://github.com/henriquesebastiao/lifesync-api',
        'email': 'contato@henriquesebastiao.com',
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(user.router)
app.include_router(quote.router)
app.include_router(accounts.router)
app.include_router(token.router)
