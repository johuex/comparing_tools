from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response


routes = web.RouteTableDef()


@routes.get('/')
async def test_root(request) -> Response:
    return web.Response(status=200)


app = web.Application()
app.add_routes(routes)
# choose one of them
# web.run_app(app)  # 1 thread
# gunicorn src.web.python.test_aiohttp:app --bind localhost:8000 --worker-class aiohttp.GunicornWebWorker --workers=8  # 8 process
