from search_engine.advanced_search import search

results = search(
    '"sqlite3"'
)

for item in results:

    print(item)