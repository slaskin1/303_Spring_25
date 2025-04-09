import wikipedia
import time
import os
from concurrent.futures import ThreadPoolExecutor

search_query = "generative artificial intelligence"
topics = wikipedia.search(search_query)

if not topics:
    print("No topics found for the search query.")
else:
    print("Topics found:", topics)

# ------------------------
# PART A: Sequential Download
# ------------------------

print("\n--- Starting Part A: Sequential Download ---")
start_time_a = time.perf_counter()

for topic in topics:
    try:
        page = wikipedia.page(topic, auto_suggest=False)
        title = page.title
        references = page.references

        print(f"Found {len(references)} references for {title}")

        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()

        if references:
            with open(f"{safe_title}.txt", "w", encoding="utf-8") as file:
                for ref in references:
                    file.write(ref + "\n")
        else:
            print(f"No references found for {title}")

    except Exception as e:
        print(f"Skipping topic '{topic}' due to error: {e}")

end_time_a = time.perf_counter()
print(f"Part A completed in {end_time_a - start_time_a:.2f} seconds.")

# ------------------------
# PART B: Concurrent Download
# ------------------------

print("\n--- Starting Part B: Concurrent Download ---")

def wiki_dl_and_save(topic):
    try:
        page = wikipedia.page(topic, auto_suggest=False)
        title = page.title
        references = page.references

        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()

        if references:
            with open(f"{safe_title}.txt", "w", encoding="utf-8") as file:
                for ref in references:
                    file.write(ref + "\n")
        else:
            print(f"No references found for {title}")

    except Exception as e:
        print(f"Skipping topic '{topic}' due to error: {e}")

start_time_b = time.perf_counter()

with ThreadPoolExecutor() as executor:
    executor.map(wiki_dl_and_save, topics)

end_time_b = time.perf_counter()
print(f"Part B completed in {end_time_b - start_time_b:.2f} seconds.")
