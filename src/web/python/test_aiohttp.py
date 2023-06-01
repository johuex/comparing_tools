from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response


routes = web.RouteTableDef()


@routes.get('/')
async def test_root(request) -> Response:
    return web.Response(status=200)


app = web.Application()
app.add_routes(routes)
#web.run_app(app)
# gunicorn src.web.python.aiohttp.test_aiohttp:app --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker --workers=8
