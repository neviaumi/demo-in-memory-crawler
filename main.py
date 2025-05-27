import diy_dot_com_crawler
from crawlee import service_locator
from crawlee.storage_clients import MemoryStorageClient

service_locator.set_storage_client(MemoryStorageClient(
    storage_dir="",
    default_request_queue_id="",
    default_key_value_store_id="",
    default_dataset_id="",
    write_metadata=False,
    persist_storage=False))

async def main() -> None:
    products = await diy_dot_com_crawler.product_search(
        'Tomato'
    )
    product = await diy_dot_com_crawler.product_detail(products[0]['url'])
    print(product)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())