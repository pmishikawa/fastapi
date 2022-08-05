from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
import schemas.job_primera as job_primera_schema
import cruds.job_primera as job_primera_crud

router = APIRouter()


@router.get("/primera_jobs", response_model=list[job_primera_schema.JobPrimera])
async def get_jobs(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    jobs = await job_primera_crud.get_jobs(db, skip=skip, limit=limit)
    return jobs


@router.get("/primera_jobs/{job_id}", response_model=job_primera_schema.JobPrimera)
async def get_job_primera(job_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await job_primera_crud.get_job(db, job_id=job_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post(
    "/primera_jobs/", response_model=job_primera_schema.JobPrimeraCreateResponse
)
def create_primera_job(
    job_body: job_primera_schema.JobPrimeraCreate, db: AsyncSession = Depends(get_db)
):
    # print("=======================")
    # print(type(job_body))
    # print("=======================")
    # dir(job_body)
    # print("=======================")

    # result_id = await job_primera_crud.get_job(db, id=job_primera_schema.id)
    # if result_id:
    #    raise HTTPException(status_code=400, detail="Job already registered")
    print("=======================")
    return job_primera_crud.create_job(db=db, job=job_body)
