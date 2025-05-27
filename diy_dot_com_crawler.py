import urllib.parse

from crawlee import Request
from crawlee.crawlers import ParselCrawlingContext
from crawlee.router import Router
from crawlee.crawlers import ParselCrawler
from crawlee.http_clients import HttpxHttpClient

router = Router[ParselCrawlingContext]()
DIY_DOT_COM_URL = "https://www.diy.com"


@router.handler(label="Search products")
async def diy_dot_com_product_search_handler(context: ParselCrawlingContext) -> None:

    for product in context.selector.css('[data-testid=\'product\']'):
        await context.push_data({
            'title': product.css('[data-testid=\'product-name\']::text').get(),
            "price": product.css('[data-testid=\'product-price\']::text').get(),
            "url": product.css('[data-testid=\'product-link\']::attr(href)').get()
        })


@router.handler(label="Get product detail")
async def diy_dot_com_product_detail_handler(context: ParselCrawlingContext) -> None:

    await context.push_data({
        "title": context.selector.css('[data-testid=\'product-name\']::text').get(),
        "price": context.selector.css('[data-testid=\'product-price\']::text').get(),
        "detail": context.selector.css('#product-details').get(),
    })


async def product_search(keyword: str):
    query = urllib.parse.urlencode({"term": keyword})
    request = Request.from_url(f"{DIY_DOT_COM_URL}/search?{query}", label="Search products")
    crawler = ParselCrawler(
        configure_logging=False,
        request_handler=router,
        http_client=HttpxHttpClient(),
    )
    await crawler.run(
        [
            request
        ]
    )
    result = [item for item in (await crawler.get_data()).items]
    crawler.stop()
    return result

async def product_detail(product_path: str):
    request = Request.from_url(f"{DIY_DOT_COM_URL}{product_path}", label="Get product detail")
    crawler = ParselCrawler(
        configure_logging=False,
        request_handler=router,
        http_client=HttpxHttpClient(),
    )
    await crawler.run(
        [
            request
        ]
    )
    result = [item for item in (await crawler.get_data()).items]
    crawler.stop()
    return result[0]