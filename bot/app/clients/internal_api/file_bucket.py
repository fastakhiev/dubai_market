from app.clients.base import BaseAPI
from app.core import config


class FileBucketApi(BaseAPI):
    base_url = config.FILES_BUCKET_URL

    @classmethod
    async def upload_image(
            self,
            file_id: str
    ):
        try:
            http_code, response_data = await self._request(
                method="post",
                path="/upload_preview",
                json_data={
                    "file_id": file_id
                }
            )
            return http_code, response_data
        except Exception as e:
            print(e)