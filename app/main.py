from fastapi import FastAPI


from app.core import utils


def get_application() -> None:
    app = FastAPI(
        title='Impact Room Book'
    )

    app.add_event_handler('startup', utils.start_up_handler(app))
    app.add_event_handler('shutdown', utils.shut_down_handler(app))