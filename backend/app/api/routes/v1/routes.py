from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.schemas.upload import UploadImage
import asyncio
from app.core.http_client import get_http_session
from app.core import config
import os
import aiofiles
from app.models.photos import Photo

router = APIRouter()

DOWNLOAD_SEMAPHORE = asyncio.Semaphore(10)


@router.post("/upload_image")
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

        os.makedirs("app/images/", exist_ok=True)
        filename = os.path.basename(file_path)
        full_path = os.path.join("app/images/", filename)

        async with aiofiles.open(full_path, "wb") as f:
            await f.write(content)

        await Photo.objects.create(
            file_id=upload_data.file_id,
            file_path=full_path
        )

        return {"status": "ok", "filename": filename, "path": full_path}


@router.get("/get_image/{file_id}")
async def get_image_by_id(
        file_id: str
):
    file_info = await Photo.objects.get(file_id=file_id)
    if os.path.exists(file_info.file_path):
        return FileResponse(file_info.file_path)
    else:
        raise HTTPException(status_code=404)