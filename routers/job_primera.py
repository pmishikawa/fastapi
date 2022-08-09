from fastapi import APIRouter, HTTPException, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import schemas.job_primera as job_primera_schema
import cruds.job_primera as job_primera_crud
from fastapi_csrf_protect import CsrfProtect
from lib.auth_utils import AuthJwtCsrf

router = APIRouter(prefix="/primera_jobs", tags=["Primera"])
auth = AuthJwtCsrf()


@router.get("/", response_model=list[job_primera_schema.JobPrimera])
async def get_jobs(
    req: Request,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    auth.verify_jwt(req)
    jobs = await job_primera_crud.get_jobs(db, skip=skip, limit=limit)
    return jobs


@router.get("/{job_id}", response_model=job_primera_schema.JobPrimera)
async def get_job_primera(
    req: Request, res: Response, job_id: int, db: AsyncSession = Depends(get_db)
):
    new_token, _ = auth.verify_update_jwt(req)

    db_user = await job_primera_crud.get_job(db, job_id=job_id)

    res.set_cookie(
        key="access_token",
        value=f"bearer {new_token}",
        httponly=True,
        samesite="none",
        secure=True,
    )

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=job_primera_schema.JobPrimeraCreateResponse)
async def create_primera_job(
    req: Request,
    res: Response,
    job_body: job_primera_schema.JobPrimeraCreate,
    csrf_protect: CsrfProtect = Depends(),
    db: AsyncSession = Depends(get_db),
):
    new_token = auth.verify_csrf_update_jwt(req, csrf_protect, req.headers)

    result = await job_primera_crud.create_job(db, job_body)

    res.status_code = status.HTTP_201_CREATED
    res.set_cookie(
        key="access_token",
        value=f"bearer {new_token}",
        httponly=True,
        samesite="none",
        secure=True,
    )

    if result:
        return result
    raise HTTPException(status_code=404, detail="Create task failed")


@router.put("/{job_id}", response_model=job_primera_schema.JobPrimeraCreateResponse)
async def update_user(
    req: Request,
    res: Response,
    job_id: int,
    job_body: job_primera_schema.JobPrimeraCreate,
    csrf_protect: CsrfProtect = Depends(),
    db: AsyncSession = Depends(get_db),
):
    new_token = auth.verify_csrf_update_jwt(req, csrf_protect, req.headers)

    job = await job_primera_crud.get_job(db, job_id=job_id)

    res.set_cookie(
        key="access_token",
        value=f"bearer {new_token}",
        httponly=True,
        samesite="none",
        secure=True,
    )

    if job is None:
        raise HTTPException(status_code=404, detail="Primera job not found")

    return await job_primera_crud.update_job(db, job_body, original=job)


@router.delete("/{job_id}", response_model=None)
async def delete_user(
    req: Request,
    res: Response,
    job_id: int,
    csrf_protect: CsrfProtect = Depends(),
    db: AsyncSession = Depends(get_db),
):
    new_token = auth.verify_csrf_update_jwt(req, csrf_protect, req.headers)

    job = await job_primera_crud.get_job(db, job_id=job_id)

    res.set_cookie(
        key="access_token",
        value=f"bearer {new_token}",
        httponly=True,
        samesite="none",
        secure=True,
    )

    if job:
        return {"message": "Successfully deleted"}
    raise HTTPException(status_code=404, detail="Delete Pprimera job failed")

    return await job_primera_crud.delete_job(db, original=job)
