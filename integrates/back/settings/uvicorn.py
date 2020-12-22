# IntegratesWorker class overrides uvicorn base worker to inject custom params

from uvicorn.workers import UvicornWorker


class IntegratesWorker(UvicornWorker):  # type: ignore

    CONFIG_KWARGS = {'interface': 'asgi3'}
