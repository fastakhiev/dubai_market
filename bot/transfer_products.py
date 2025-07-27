import psycopg2
from elasticsearch import helpers
from app.core import config
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=[f"http://{config.ELASTIC_HOST}:{config.ELASTIC_PORT}"])

pg_conn = psycopg2.connect(
    dbname=config.POSTGRES_DB,
    user=config.POSTGRES_USER,
    password=config.POSTGRES_PASSWORD,
    host=config.POSTGRES_HOST,
    port=config.POSTGRES_PORT,
)
pg_cursor = pg_conn.cursor()

INDEX_NAME = "products"
BATCH_SIZE = 1


def create_index_if_not_exists(index_name):
    if not es.indices.exists(index=index_name):
        index_settings = {
            "settings": {
                "analysis": {
                    "tokenizer": {
                        "edge_ngram_tokenizer": {
                            "type": "edge_ngram",
                            "min_gram": 1,
                            "max_gram": 20,
                            "token_chars": ["letter", "digit"],
                        }
                    },
                    "analyzer": {
                        "edge_ngram_analyzer": {
                            "type": "custom",
                            "tokenizer": "edge_ngram_tokenizer",
                            "filter": ["lowercase"],
                        },
                        "whitespace_analyzer": {
                            "type": "custom",
                            "tokenizer": "whitespace",
                            "filter": ["lowercase"],
                        },
                    },
                }
            },
            "mappings": {
    "properties": {
        "title": {
            "type": "text",
            "analyzer": "edge_ngram_analyzer",
            "search_analyzer": "whitespace_analyzer",
            "fields": {
                "keyword": {"type": "keyword"},
            },
        },
        "category": {
            "type": "keyword"
        },
        "currency": {
            "type": "keyword"
        },
        "seller_id": {
            "type": "keyword"
        },

        "is_active": {
            "type": "keyword"
        }

    }
},
        }

        es.indices.create(index=index_name, body=index_settings)
        print("ok")
    else:
        print("not ok")


def fetch_pg_data(batch_size=BATCH_SIZE):
    offset = 0
    while True:
        query = f"""
        SELECT id, title, description, price, currency, seller_id, thumbnail, category, is_active, is_moderation
        FROM products
        LIMIT {batch_size} OFFSET {offset};
        """
        pg_cursor.execute(query)
        columns = [desc[0] for desc in pg_cursor.description]
        rows = pg_cursor.fetchall()
        if not rows:
            break
        for row in rows:
            yield {
                **{columns[i]: row[i] for i in range(len(columns))},
            }
        offset += batch_size


def load_data_to_es(data, index_name):
    actions = [
        {
            "_index": index_name,
            "_id": str(record["id"]),
            "_source": record,
        }
        for record in data
    ]

    if actions:
        success, errors = helpers.bulk(es, actions, raise_on_error=False)

        if errors:
            print(f"Ошибки при загрузке в Elasticsearch: {errors}")
    else:
        print("Нет данных для загрузки")


def main():
    print("Начало выгрузки данных...")
    pg_data = fetch_pg_data()
    create_index_if_not_exists(INDEX_NAME)
    batch = []
    counter = 0

    for record in pg_data:
        batch.append(record)
        if len(batch) >= BATCH_SIZE:
            load_data_to_es(batch, INDEX_NAME)
            counter += len(batch)
            print(f"Загружено записей: {counter}")
            batch = []

    if batch:
        load_data_to_es(batch, INDEX_NAME)
        counter += len(batch)
        print(f"Загружено записей: {counter}")

    print("Выгрузка данных завершена.")


if __name__ == "__main__":
    main()
