from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from typing import Optional
from datetime import datetime, timedelta, timezone
from fastapi.encoders import jsonable_encoder
import schemas.job_primera as job_primera_schema
import models.job_primera as job_primera_model


JST = timezone(timedelta(hours=+9), "JST")


async def get_job(
    db: AsyncSession, job_id: int
) -> Optional[job_primera_model.JobPrimera]:
    result: Result = await db.execute(
        select(
            job_primera_model.JobPrimera.id,
            job_primera_model.JobPrimera.data_job,
            job_primera_model.JobPrimera.title,
            job_primera_model.JobPrimera.copies,
            job_primera_model.JobPrimera.finished_top_to_bottom,
            job_primera_model.JobPrimera.finished_edge,
            job_primera_model.JobPrimera.has_cut,
            job_primera_model.JobPrimera.cutting_top,
            job_primera_model.JobPrimera.stitches,
            job_primera_model.JobPrimera.stacks,
            job_primera_model.JobPrimera.batches,
            job_primera_model.JobPrimera.cover_cutting_top,
            job_primera_model.JobPrimera.cover_edge,
            job_primera_model.JobPrimera.cover_thickness,
            job_primera_model.JobPrimera.signature_pages,
            job_primera_model.JobPrimera.signature_top_to_bottom,
            job_primera_model.JobPrimera.signature_cutting_top,
            job_primera_model.JobPrimera.signature_cutting_bottom,
            job_primera_model.JobPrimera.signature_edge,
            job_primera_model.JobPrimera.signature_thickness,
            job_primera_model.JobPrimera.created_at,
            job_primera_model.JobPrimera.updated_at,
        ).where(job_primera_model.JobPrimera.id == job_id)
    )
    # for item in result:
    #    print(item.Item.id)
    # print(result.first())
    # print("=============================")

    return result.first()


async def get_jobs(db: AsyncSession, skip: int = 0, limit: int = 100):

    result: Result = await db.execute(
        select(
            job_primera_model.JobPrimera.id,
            job_primera_model.JobPrimera.data_job,
            job_primera_model.JobPrimera.title,
            job_primera_model.JobPrimera.copies,
            job_primera_model.JobPrimera.finished_top_to_bottom,
            job_primera_model.JobPrimera.finished_edge,
            job_primera_model.JobPrimera.has_cut,
            job_primera_model.JobPrimera.cutting_top,
            job_primera_model.JobPrimera.stitches,
            job_primera_model.JobPrimera.stacks,
            job_primera_model.JobPrimera.batches,
            job_primera_model.JobPrimera.cover_cutting_top,
            job_primera_model.JobPrimera.cover_edge,
            job_primera_model.JobPrimera.cover_thickness,
            job_primera_model.JobPrimera.signature_pages,
            job_primera_model.JobPrimera.signature_top_to_bottom,
            job_primera_model.JobPrimera.signature_cutting_top,
            job_primera_model.JobPrimera.signature_cutting_bottom,
            job_primera_model.JobPrimera.signature_edge,
            job_primera_model.JobPrimera.signature_thickness,
            job_primera_model.JobPrimera.created_at,
            job_primera_model.JobPrimera.updated_at,
        )
        .offset(skip)
        .limit(limit)
    )
    return result.all()


async def create_job(
    db: AsyncSession, job: job_primera_schema.JobPrimeraCreate
) -> job_primera_model.JobPrimera:
    print("------------------------===1")

    job_data1 = jsonable_encoder(job)
    print(type(job_data1))
    print(job_data1)
    db_job = job_primera_model.JobPrimera(**job_data1)
    print(db_job)
    print("------------------------===2")
    job_data2 = job_primera_model.JobPrimera(**job.dict())
    print(type(job_data2))
    print(job_data2)

    print("------------------------===3")
    print(type(job))
    print(job)

    db.add(job_data2)
    print("------------------------===4")
    await db.commit()
    await db.refresh(job_data2)
    print("------------------------===5")
    return job_data2


async def update_job(
    db: AsyncSession,
    job_create: job_primera_schema.JobPrimeraCreate,
    original: job_primera_model.JobPrimera,
) -> job_primera_model.JobPrimera:
    original.data_job = job_create.data_job
    original.title = job_create.title
    original.copies = job_create.copies
    original.finished_top_to_bottom = job_create.finished_top_to_bottom
    original.finished_edge = job_create.finished_edge
    original.has_cut = job_create.has_cut
    original.cutting_top = job_create.cutting_top
    original.stitches = job_create.stitches
    original.batches = job_create.batches
    original.cover_cutting_top = job_create.cover_cutting_top
    original.cover_edge = job_create.cover_edge
    original.cover_thickness = job_create.cover_thickness
    original.signature_pages = job_create.signature_pages
    original.signature_top_to_bottom = job_create.signature_top_to_bottom
    original.signature_cutting_top = job_create.signature_cutting_top
    original.signature_cutting_bottom = job_create.signature_cutting_bottom
    original.signature_edge = job_create.signature_edge
    original.signature_thickness = job_create.signature_thickness
    original.updated_at = datetime.now(JST)

    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def delete_user(db: AsyncSession, original: job_primera_model.JobPrimera) -> None:
    await db.delete(original)
    await db.commit()
