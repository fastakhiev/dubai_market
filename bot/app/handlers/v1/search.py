from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from app.core.elastic import es
from app.models.orders import Order
from app.models.questions import Question
from app.handlers.v1.sign_up import cmd_start
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

    if "filter" not in data:
        await inline_query.answer(
            results=[],
            switch_pm_text="Ошибка: фильтр не установлен",
            switch_pm_parameter="set_filter",
            cache_time=1
        )
        return

    if "orders" in data["filter"]:
        if data["message"]["type"] == "seller":
            orders = await Order.objects.select_related('product_id__seller_id').filter(product_id__seller_id__telegram_id=data["filter"]["orders"]).all()
            results = []
            for i in orders:
                results.append(
                    InlineQueryResultArticle(
                        id=str(i.id),
                        title=i.product_id.title,
                        thumb_url=f"https://dubaimarketbot.ru/get_image/{i.product_id.thumbnail}",
                        description=f"{i.destination}; {'Подтвержден' if i.is_approve else 'Не подтвержден'}",
                        input_message_content=InputTextMessageContent(
                            message_text=f"order_{str(i.id)}:{data['message']['type']}"
                        )
                    )
                )
            await inline_query.answer(results, cache_time=1)
            return
        elif data["message"]["type"] == "buyer":
            orders = await Order.objects.select_related("product_id").select_related("buyer_id").filter(buyer_id__telegram_id=data["filter"]["orders"]).all()
            results = []
            for i in orders:
                results.append(
                    InlineQueryResultArticle(
                        id=str(i.id),
                        title=i.product_id.title,
                        thumb_url=f"https://dubaimarketbot.ru/get_image/{i.product_id.thumbnail}",
                        description=f"{i.destination}; {'Подтвержден' if i.is_approve else 'Не подтвержден'}",
                        input_message_content=InputTextMessageContent(
                            message_text=f"order_{str(i.id)}:{data['message']['type']}"
                        )
                    )
                )
            await inline_query.answer(results, cache_time=1)
            return

    if "questions" in data["filter"]:
        if data["message"]["type"] == "seller":
            questions = await Question.objects.select_related('product_id__seller_id').filter(product_id__seller_id__telegram_id=data["filter"]["questions"]).all()
            results = []
            for i in questions:
                results.append(
                    InlineQueryResultArticle(
                        id=str(i.id),
                        title=i.question,
                        thumb_url=f"https://dubaimarketbot.ru/get_image/{i.product_id.thumbnail}",
                        description=f"{i.answer if i.answer else 'Нет ответа'}",
                        input_message_content=InputTextMessageContent(
                            message_text=f"question_{str(i.id)}:{data['message']['type']}"
                        )
                    )
                )
            await inline_query.answer(results, cache_time=1)
            return
        elif data["message"]["type"] == "buyer":
            questions = await Question.objects.select_related('buyer_id').select_related("product_id").filter(buyer_id__telegram_id=data["filter"]["questions"]).all()
            results = []
            for i in questions:
                results.append(
                    InlineQueryResultArticle(
                        id=str(i.id),
                        title=i.question,
                        thumb_url=f"https://dubaimarketbot.ru/get_image/{i.product_id.thumbnail}",
                        description=f"{i.answer if i.answer else 'Нет ответа'}",
                        input_message_content=InputTextMessageContent(
                            message_text=f"question_{str(i.id)}:{data['message']['type']}"
                        )
                    )
                )
            await inline_query.answer(results, cache_time=1)
            return

    filter_dict = data["filter"]
    must_conditions = []

    for key, value in filter_dict.items():
        must_conditions.append({
            "term": {key: value}
        })
    if data["message"]["type"] == "buyer":
        must_conditions.append({
            "term": {"is_active": "true"}
        })

    if query:
        es_query = {
            "query": {
                "bool": {
                    "must": must_conditions,
                    "should": [
                        {"term": {"title.keyword": {"value": query, "boost": 100}}},
                        {"match": {"title": {"query": query, "boost": 50}}},
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
                    "minimum_should_match": 1
                }
            },
            "sort": [{"_score": "desc"}, {"title.keyword": "asc"}]
        }
    else:
        es_query = {
            "query": {
                "bool": {
                    "must": must_conditions
                }
            },
            "size": 10,
            "sort": [{"title.keyword": "asc"}]
        }


    response = await es.search(index="products", body=es_query)


    results = []
    for hit in response["hits"]["hits"]:
        product = hit["_source"]
        results.append(
            InlineQueryResultArticle(
                id=str(product["id"]),
                title=f'{product["title"]}, {product["price"]} {product["currency"]}',
                description=f"{product['description']}, Статус: {'активен' if product['is_active'] else 'забанен' if data['message']['type'] == 'seller' and product['is_moderation'] is False else 'На проверке'}",
                thumb_url=f"https://dubaimarketbot.ru/get_image/{product['thumbnail']}",
                input_message_content=InputTextMessageContent(
                    message_text=f"product_{product['id']}:{data['message']['type']}"
                ),
            )
        )

    await inline_query.answer(results, cache_time=1)