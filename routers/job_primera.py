from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api.database import get_db
import api.schemas.job_primera as job_primera_schema
import api.cruds.job_primera as job_primera_crud

router = APIRouter()


@router.post("/primera_jobs/", response_model=job_primera_schema.JobPrimera)
async def create_primera_job(
    user: job_primera_schema.JobPrimera, db: AsyncSession = Depends(get_db)
):
    db_user = await job_primera_crud.get_job_primera(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return job_primera_crud.create_user(db=db, user=user)


@router.get("/primera_jobs", response_model=list[job_primera_schema.JobPrimera])
async def read_primera_jobs(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    users = await job_primera_crud.get_job_primera(db, skip=skip, limit=limit)
    return users


@router.get("/primera_jobs/{job_id}", response_model=job_primera_schema.JobPrimera)
async def get_job_primera(job_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await job_primera_crud.get_job_primera(db, job_id=job_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
