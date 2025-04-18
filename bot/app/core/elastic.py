from elasticsearch import AsyncElasticsearch
from app.core import config

es = AsyncElasticsearch(
    hosts=f"http://{config.ELASTIC_HOST}:{config.ELASTIC_PORT}", verify_certs=False
)
