from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import schemas.job_alegro_line as job_alegro_line_schema
import cruds.job_alegro_line as job_alegro_line_crud

router = APIRouter()


@router.get(
    "/alegro_line_jobs", response_model=list[job_alegro_line_schema.JobAlegroLine]
)
async def get_jobs(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    jobs = await job_alegro_line_crud.get_jobs(db, skip=skip, limit=limit)
    return jobs


@router.get(
    "/alegro_line_jobs/{job_id}", response_model=job_alegro_line_schema.JobAlegroLine
)
async def get_job_alegro_line(job_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await job_alegro_line_crud.get_job(db, job_id=job_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Alegro line not found")
    return db_user


@router.post(
    "/alegro_line_jobs/",
    response_model=job_alegro_line_schema.JobAlegroLineCreateResponse,
)
async def create_alegro_line_job(
    job_body: job_alegro_line_schema.JobAlegroLineCreate,
    db: AsyncSession = Depends(get_db),
):
    return await job_alegro_line_crud.create_job(db, job_body)


@router.put(
    "/alegro_line_jobs/{job_id}",
    response_model=job_alegro_line_schema.JobAlegroLineCreateResponse,
)
async def update_user(
    job_id: int,
    job_body: job_alegro_line_schema.JobAlegroLineCreate,
    db: AsyncSession = Depends(get_db),
):
    job = await job_alegro_line_crud.get_job(db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="alegro_line job not found")

    return await job_alegro_line_crud.update_job(db, job_body, original=job)


@router.delete("/alegro_line_jobs/{job_id}", response_model=None)
async def delete_user(job_id: int, db: AsyncSession = Depends(get_db)):
    job = await job_alegro_line_crud.get_job(db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Alegro line job not found")

    return await job_alegro_line_crud.delete_job(db, original=job)
