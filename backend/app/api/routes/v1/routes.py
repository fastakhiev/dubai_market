from exceptiongroup import catch
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.upload import UploadImage
import asyncio
from app.core.http_client import get_http_session
from app.core import config
import os
import mimetypes
from app.models.photos import Photo
from app.core.minio_client import minio_client
import io

router = APIRouter()

DOWNLOAD_SEMAPHORE = asyncio.Semaphore(10)


@router.post("/upload_preview")
async def upload_image(
        upload_data: UploadImage
):
    async with DOWNLOAD_SEMAPHORE:
        file_info_url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/getFile?file_id={upload_data.file_id}"
        session = await get_http_session()
        async with session.get(file_info_url) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=resp.status, detail="Failed to get file info from Telegram")
            data = await resp.json()
            file_path = data.get("result", {}).get("file_path")
            if not file_path:
                raise HTTPException(status_code=400, detail="file_path not found in response")

        file_url = f"https://api.telegram.org/file/bot{config.TELEGRAM_TOKEN}/{file_path}"
        async with session.get(file_url) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=resp.status, detail="Failed to download file from Telegram")
            content = await resp.read()

        filename = os.path.basename(file_path)
        minio_client.put_object(
            config.MINIO_BUCKET_PREVIEW,
            filename,
            data=io.BytesIO(content),
            length=len(content),
        )
        try:
            await Photo.objects.create(
                file_id=upload_data.file_id,
                file_name=filename
            )
            return {"status": "ok", "filename": filename}
        except:
            return {"status": "ok", "filename": filename}



@router.get("/get_image/{file_id}")
async def get_image_by_id(
        file_id: str
):
    file_info = await Photo.objects.get(file_id=file_id)
    response = minio_client.get_object(
        config.MINIO_BUCKET_PREVIEW,
        file_info.file_name,
    )
    mime_type, _ = mimetypes.guess_type(file_info.file_name)
    mime_type = mime_type or "application/octet-stream"
    return StreamingResponse(
        content=response,  # это stream
        media_type=mime_type  # или image/jpeg — зависит от файла!
    )