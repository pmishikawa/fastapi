from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from typing import Optional, Tuple
from datetime import datetime, timedelta, timezone
import schemas.job_alegro_line as job_alegro_line_schema
import models.job_alegro_line as job_alegro_line_model


JST = timezone(timedelta(hours=+9), "JST")


async def get_job(
    db: AsyncSession, job_id: int
) -> Optional[job_alegro_line_model.JobAlegroLine]:
    result: Result = await db.execute(
        select(job_alegro_line_model.JobAlegroLine).where(
            job_alegro_line_model.JobAlegroLine.id == job_id
        )
    )
    # for item in result:
    #    print(item.Item.id)
    # print(result.first())

    alegro_lineJob: Optional[
        Tuple[job_alegro_line_model.JobAlegroLine]
    ] = result.first()
    return alegro_lineJob[0] if alegro_lineJob is not None else None


async def get_jobs(db: AsyncSession, skip: int = 0, limit: int = 100):

    result: Result = await db.execute(
        select(
            job_alegro_line_model.JobAlegroLine.id,
            job_alegro_line_model.JobAlegroLine.date_job,
            job_alegro_line_model.JobAlegroLine.title,
            job_alegro_line_model.JobAlegroLine.copies,
            job_alegro_line_model.JobAlegroLine.speed,
            job_alegro_line_model.JobAlegroLine.finished_top_to_bottom,
            job_alegro_line_model.JobAlegroLine.finished_edge,
            job_alegro_line_model.JobAlegroLine.cover_cutting_top,
            job_alegro_line_model.JobAlegroLine.cover_edge,
            job_alegro_line_model.JobAlegroLine.cover_thickness,
            job_alegro_line_model.JobAlegroLine.signature_cutting_top,
            job_alegro_line_model.JobAlegroLine.signature_edge,
            job_alegro_line_model.JobAlegroLine.signature_thickness,
            job_alegro_line_model.JobAlegroLine.created_at,
            job_alegro_line_model.JobAlegroLine.updated_at,
        )
        .offset(skip)
        .limit(limit)
    )
    return result.all()


async def create_job(
    db: AsyncSession, job: job_alegro_line_schema.JobAlegroLine
) -> job_alegro_line_model.JobAlegroLine:

    db_job = job_alegro_line_model.JobAlegroLine(**job.dict())

    db.add(db_job)

    await db.commit()
    await db.refresh(db_job)

    return db_job


async def update_job(
    db: AsyncSession,
    job_create: job_alegro_line_schema.JobAlegroLine,
    original: job_alegro_line_model.JobAlegroLine,
) -> job_alegro_line_model.JobAlegroLine:

    original.date_job = job_create.date_job
    original.title = job_create.title
    original.copies = job_create.copies
    original.speed = job_create.speed
    original.finished_top_to_bottom = job_create.finished_top_to_bottom
    original.finished_edge = job_create.finished_edge
    original.cover_cutting_top = job_create.cover_cutting_top
    original.cover_edge = job_create.cover_edge
    original.cover_thickness = job_create.cover_thickness
    original.signature_cutting_top = job_create.signature_cutting_top
    original.signature_edge = job_create.signature_edge
    original.signature_thickness = job_create.signature_thickness
    original.updated_at = datetime.now(JST)
    original.created_at = job_create.created_at

    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def delete_job(
    db: AsyncSession, original: job_alegro_line_model.JobAlegroLine
) -> None:
    await db.delete(original)
    await db.commit()
