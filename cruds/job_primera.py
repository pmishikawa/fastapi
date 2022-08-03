from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
import api.schemas.job_primera as job_primera_schema
import api.models.job_primera as job_primera_model


async def get_job_primera(db: AsyncSession, job_id: int):
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


async def get_user_by_email(db: AsyncSession, email: str):
    return (
        await db.query(job_primera_model.User)
        .filter(job_primera_model.User.email == email)
        .filter()
    )


async def get_job_primeras(db: AsyncSession, skip: int = 0, limit: int = 100):

    result: Result = await db.execute(
        select(job_primera_model.User).offset(skip).limit(limit).all()
    )

    return await result


async def create_job_primera(db: AsyncSession, user: job_primera_schema.JobPrimera):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = await job_primera_model.User(
        email=user.email, fake_hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
