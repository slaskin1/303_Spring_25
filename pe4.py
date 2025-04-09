import wikipedia
import time
import os

search_query = "generative artificial intelligence"
topics = wikipedia.search(search_query)

if not topics:
    print("No topics found for the search query.")
else:
    print("Topics found:", topics)

start_time = time.perf_counter()

for topic in topics:
    try:
        page = wikipedia.page(topic, auto_suggest=False)
        title = page.title
        references = page.references

        print(f"Found {len(references)} references for {title}")

        print("References:", references)

        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()

        if references:
            with open(f"{safe_title}.txt", "w", encoding="utf-8") as file:
                for ref in references:
                    file.write(ref + "\n")
        else:
            print(f"No references found for {title}")

    except Exception as e:
        print(f"Skipping topic '{topic}' due to error: {e}")

end_time = time.perf_counter()
print(f"Execution completed in {end_time - start_time:.2f} seconds.")