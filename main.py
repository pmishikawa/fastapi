from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi.responses import JSONResponse
from schemas.auth import SuccessMsg, CsrfSettings
from routers import auth, users, job_primera, job_alegro_line
from fastapi.routing import APIRoute
from typing import Callable
import time
import datetime
from logging import getLogger, StreamHandler, DEBUG
import sys
import json

logger = getLogger(__name__)
handler = StreamHandler(sys.stdout)
handler.setLevel(DEBUG)
logger.addHandler(handler)
logger.setLevel(DEBUG)


class LoggingContextRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            """
            時間計測
            """
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = round(time.time() - before, 4)

            record = {}
            time_local = datetime.datetime.fromtimestamp(before)
            record["time_local"] = time_local.strftime("%Y/%m/%d %H:%M:%S%Z")
            if await request.body():
                record["request_body"] = (await request.body()).decode("utf-8")
            record["request_headers"] = {
                k.decode("utf-8"): v.decode("utf-8") for (k, v) in request.headers.raw
            }
            record["remote_addr"] = request.client.host
            record["request_uri"] = request.url.path
            record["request_method"] = request.method
            record["request_time"] = str(duration)
            record["status"] = response.status_code
            record["response_body"] = response.body.decode("utf-8")
            record["response_headers"] = {
                k.decode("utf-8"): v.decode("utf-8") for (k, v) in response.headers.raw
            }
            logger.info(json.dumps(record))
            return response

        return custom_route_handler


app = FastAPI(
    title="mm-jdf-editor API",
    description="プレスメディア学習用",
    version="0.1.0",
    contact={"name": "プレスメディア", "url": "https://pressmedia.co.jp/contents/contact/"},
)

app.router.route_class = LoggingContextRoute

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(job_primera.router)
app.include_router(job_alegro_line.router)
origins = ["http://localhost:3000", "http://localhost:5173"]
#origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get("/hello", response_model=SuccessMsg)
async def hello():
    print()
    return {"message": "hello world"}
