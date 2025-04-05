from aiogram import Router, F
from uuid import uuid4
from app.core.bot import bot
from app.core.elastic import es
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
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
                        {"term": {"title.keyword": {"value": query, "boost": 100}}},
                        {
                            "match_phrase_prefix": {
                                "title.prefix": {"query": query, "boost": 50}
                            }
                        },
                        {"match_phrase": {"title": {"query": query, "boost": 20}}},
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
        results.append(
            InlineQueryResultArticle(
                id=str(product["id"]),
                title=f'{product["title"]}',
                description=f'Рейтинг: {product["description"]}',
                input_message_content=InputTextMessageContent(
                    message_text=f'{product["title"]} ({product["price"]})\nРейтинг: {product["description"]}'
                ),
            )
        )

    await inline_query.answer(results, cache_time=1)
