from app.models.products import Product

ITEMS_PER_PAGE = 3


async def get_user_products(telegram_id: str, page: int = 0):
    products = await Product.objects.select_related("seller_id").order_by("-created_at").all(seller_id__telegram_id=telegram_id)
    total_pages = (len(products) - 1) // ITEMS_PER_PAGE + 1
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    products_on_page = products[start:end]

    return products_on_page, total_pages