from fastapi import FastAPI, Response
import uvicorn


app = FastAPI()

@app.get("/")
def test_root():
    return Response()

# uvicorn --workers=8 src.web.python.test_fastapi:app
