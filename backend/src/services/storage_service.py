from io import BytesIO
from gridfs import AsyncGridFSBucket
from bson import ObjectId
from src.database.database import db

bucket = AsyncGridFSBucket(db)


async def upload_file(filename: str, content: bytes, content_type: str):
    file_id = await bucket.upload_from_stream(
        filename,
        BytesIO(content),
        metadata={
            "content_type": content_type
        }
    )

    return file_id


async def download_file(file_id: str):
    stream = BytesIO()

    await bucket.download_to_stream(
        ObjectId(file_id),
        stream
    )

    return stream.getvalue()


async def delete_file(file_id: str):
    await bucket.delete(ObjectId(file_id))
