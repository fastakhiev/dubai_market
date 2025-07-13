from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from app.core.elastic import es
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQueryResultPhoto,
    Message,
)

router = Router()

@router.inline_query()
async def inline_search(inline_query: InlineQuery, state: FSMContext):
    query = inline_query.query.strip()
    data = await state.get_data()
    search_key = {
        "shops": "name",
        "products": "title"
    }

    if "filter" not in data:
        await inline_query.answer(
            results=[],
            switch_pm_text="Ошибка: фильтр не установлен",
            switch_pm_parameter="set_filter",
            cache_time=1
        )
        return

    filter_dict = data["filter"]
    must_conditions = []

    for key, value in filter_dict.items():
        must_conditions.append({
            "term": {key: value}
        })

    if query:
        es_query = {
            "query": {
                "bool": {
                    "must": must_conditions,
                    "should": [
                        {"term": {f"{search_key[data['type']]}.keyword": {"value": query, "boost": 100}}},
                        {"match": {f"{search_key[data['type']]}": {"query": query, "boost": 50}}},
                        {"match_phrase": {f"{search_key[data['type']]}": {"query": query, "boost": 20}}},
                        {
                            "match": {
                                f"{search_key[data['type']]}": {
                                    "query": query,
                                    "operator": "and",
                                    "fuzziness": "auto",
                                    "boost": 10,
                                }
                            }
                        },
                    ],
                    "minimum_should_match": 1
                }
            },
            "sort": [{"_score": "desc"}, {f"{search_key[data['type']]}.keyword": "asc"}]
        }
    else:
        es_query = {
            "query": {
                "bool": {
                    "must": must_conditions
                }
            },
            "size": 10,
            "sort": [{f"{search_key[data['type']]}.keyword": "asc"}]
        }
    response = await es.search(index=data['type'], body=es_query)
    results = []
    if data['type'] == "shops":
        for hit in response["hits"]["hits"]:
            shop = hit["_source"]
            results.append(
                InlineQueryResultArticle(
                    id=str(shop["id"]),
                    title=f'{shop["name"]}',
                    description=f"{shop['social_networks']}, Статус: {'активен' if shop['is_active'] else 'забанен'}",
                    thumb_url=f"https://dubaimarketbot.ru/get_image/{shop['photo']}",
                    input_message_content=InputTextMessageContent(
                        message_text=f"shop_{shop['id']}"
                    ),
                )
            )
    else:
        for hit in response["hits"]["hits"]:
            product = hit["_source"]
            results.append(
                InlineQueryResultArticle(
                    id=str(product["id"]),
                    title=f'{product["title"]}, {product["price"]} {product["currency"]}',
                    description=f"{product['description']}, Статус: {'активен' if product['is_active'] else 'забанен'}",
                    thumb_url=f"https://dubaimarketbot.ru/get_image/{product['thumbnail']}",
                    input_message_content=InputTextMessageContent(
                        message_text=f"product_{product['id']}"
                    ),
                )
            )

    await inline_query.answer(results, cache_time=1)