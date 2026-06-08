
from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import os

from database import engine, AsyncSessionLocal
from models import Base, Task


app = FastAPI()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )


@app.get("/tasks")
async def get_tasks(
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Task)
    )

    tasks = result.scalars().all()

    return tasks

@app.post("/upload")
async def upload_file(
        file: UploadFile = File(...)
):
    os.makedirs("uploads", exist_ok=True)

    content = await file.read()

    with open(
        f"uploads/{file.filename}",
        "wb"
    ) as f:
        f.write(content)

    return {
        "message": "File uploaded",
        "filename": file.filename,
        "size": len(content)
    }


@app.post("/upload-multiple")
async def upload_multiple(
        files: List[UploadFile] = File(...)
):

    uploaded = []

    for file in files:

        contents = await file.read()

        uploaded.append(
            {
                "filename": file.filename,
                "size": len(contents)
            }
        )

    return uploaded


@app.post("/upload-image")
async def upload_image(
        file: UploadFile = File(...)
):

    if not file.content_type.startswith(
        "image/"
    ):
        return {
            "error": "Only images allowed"
        }

    return {
        "filename": file.filename
    }

