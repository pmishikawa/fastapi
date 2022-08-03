from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import items, users, job_primera

app = FastAPI()


app.include_router(items.router)
app.include_router(users.router)
app.include_router(job_primera.router)

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.include_router(token.router)
# app.include_router(tasks.router)
# app.include_router(done.router)
# app.include_router(users.router)
# origins = ["http://localhost:3000", "https://fastapi-1436a.web.app"]
# app.add_middleware(
#    CORSMiddleware,
#    allow_origins=origins,
#    allow_credentials=True,
#    allow_methods=["*"],
#    allow_headers=["*"],
# )


@app.get("/hello")
async def hello():
    print()
    return {"message": "hello world"}
