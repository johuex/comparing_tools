from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route


async def test_root(request):
    return Response()


app = Starlette(debug=True, routes=[
    Route('/', test_root),
])

# uvicorn --workers=8 src.web.python.test_starlette:app
