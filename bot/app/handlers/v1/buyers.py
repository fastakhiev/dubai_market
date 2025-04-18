from aiogram import Router, F
from sqlalchemy.util import await_only

from app.core.elastic import es
from app.core import config
from app.core.bot import bot
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQueryResultPhoto,
    Message,
)

router = Router()


@router.inline_query()
async def inline_search(inline_query: InlineQuery):
    query = inline_query.query.strip()

    if not query:
        return

    response = await es.search(
        index="products",
        body={
            "query": {
                "bool": {
                    "should": [
                        {
                            "term": {"title.keyword": {"value": query, "boost": 100}}
                        },
                        {
                            "match": {"title": {"query": query, "boost": 50}}
                        },
                        {
                            "match_phrase": {"title": {"query": query, "boost": 20}}
                        },
                        {
                            "match": {
                                "title": {
                                    "query": query,
                                    "operator": "and",
                                    "fuzziness": "auto",
                                    "boost": 10,
                                }
                            }
                        },
                    ],
                    "minimum_should_match": 1,
                }
            },
            "sort": [{"_score": "desc"}, {"title.keyword": "asc"}],
        },
    )
    results = []
    for hit in response["hits"]["hits"]:
        product = hit["_source"]
        file_info  = await bot.get_file(product['thumbnail'])
        photo_url = f"https://api.telegram.org/file/bot{config.TELEGRAM_TOKEN}/{file_info.file_path}"
        results.append(
            InlineQueryResultArticle(
                id=str(product["id"]),
                title=f'{product["title"]}, {product["price"]} {product["currency"]}',
                description=product["description"],
                thumb_url="http://0.0.0.0:8000/get_image/AgACAgIAAxkBAAIIfmgB_vG9IE_4BI9aiEDzhrvwvO-fAALk8DEbdnQRSGZempbzn_mYAQADAgADeQADNgQ",  # тут можно оставить превью картинки
                input_message_content=InputTextMessageContent(
                    message_text=f"{product['title']}\nЦена: {product['price']} {product['currency']}\nОписание: {product['description']}"
                )
            )
        )

    await inline_query.answer(results, cache_time=1)
