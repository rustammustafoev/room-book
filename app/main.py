from fastapi import FastAPI


from app.core import utils
from app.api import api
from app.core.middlewares import middleware


def get_application() -> FastAPI:
    app = FastAPI(
        title='Impact Room Book',
        middleware=middleware
    )

    app.add_event_handler('startup', utils.start_up_handler(app))
    app.add_event_handler('shutdown', utils.shut_down_handler(app))
    app.include_router(api.api_router, prefix='/api/v1')

    return app


app = get_application()
