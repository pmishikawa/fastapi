from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from fastapi.responses import JSONResponse
from schemas.auth import SuccessMsg, CsrfSettings
from routers import auth, users, job_primera, job_alegro_line

app = FastAPI(
    title="mm-jdf-editor API",
    description="プレスメディア学習用",
    version="0.1.0",
    contact={"name": "プレスメディア", "url": "https://pressmedia.co.jp/contents/contact/"},
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(job_primera.router)
app.include_router(job_alegro_line.router)
# origins = ["http://localhost:3000"]
origins = ["*"]
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
