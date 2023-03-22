import os

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from settings import (AUTHORS_INDEX, CONCEPTS_INDEX, INSTITUTIONS_INDEX,
                      PUBLISHERS_INDEX, SOURCES_INDEX, WORKS_INDEX)

INDEXES = [
    AUTHORS_INDEX,
    CONCEPTS_INDEX,
    INSTITUTIONS_INDEX,
    PUBLISHERS_INDEX,
    SOURCES_INDEX,
    WORKS_INDEX,
]


def update_indexes():
    """Use this script to sync the test indexes with the production indexes."""
    # 1. Change the index names to match what is in settings.py
    # 2. Export the ES_PROD_URL_FOR_UPDATE environment variable
    # 3. Run this script with: python scripts/update_test_indexes.py
    for index in INDEXES:
        update_test_index(index)


def update_test_index(index):
    test_client = Elasticsearch("http://elastic:testpass@127.0.0.1:9200")
    prod_client = Elasticsearch(os.environ.get("ES_PROD_URL_FOR_UPDATE"))
    s = Search(using=test_client, index=index)
    s = s.extra(size=10000)
    response = s.execute()
    count = 0
    for r in response["hits"]["hits"]:
        updated_record = get_updated_record(r["_source"]["id"], prod_client, index)
        if updated_record:
            test_client.index(index=r["_index"], id=r["_id"], document=updated_record)
            count = count + 1
        else:
            print("No updated record found for", r["_source"]["id"])
        print(count)
    print(f"updated {count} records in {index}")


def get_updated_record(id, client, index):
    s = Search(using=client, index=index)
    s = s.filter("term", id=id)
    s = s.sort("-@timestamp")
    response = s.execute()
    for r in response:
        return r.to_dict()


if __name__ == "__main__":
    update_indexes()
