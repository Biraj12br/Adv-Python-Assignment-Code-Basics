import requests
import asyncio
import time


BASE_URL = "https://openlibrary.org/search.json"

SUBJECTS = [
    "python",
    "machine learning",
    "data science",
    "artificial intelligence",
    "sql"
]


def fetch_count(subject):

    params = {
        "q": subject,
        "page": 1,
        "limit": 1,
        "fields": "title"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return subject, data["numFound"]

# SYNCHRONOUS VERSION

def sync_fetch():
    """Fetch subjects one at a time."""

    results = []

    for subject in SUBJECTS:

        result = fetch_count(subject)

        results.append(result)

    return results



# ASYNCHRONOUS VERSION

async def async_fetch():
    """Fetch all subjects concurrently."""

    tasks = [
        asyncio.to_thread(fetch_count, subject)
        for subject in SUBJECTS
    ]

    results = await asyncio.gather(*tasks)

    return results


# MAIN

def main():

    # SYNC
   
    start = time.perf_counter()
    sync_results = sync_fetch()
    sync_time = time.perf_counter() - start

    print("SYNC RESULTS")
    print("-" * 40)

    for subject, count in sync_results:
        print(f"{subject:<25} {count:,}")

    print(f"\nSync time: {sync_time:.2f} seconds")


   
    # ASYNC

    start = time.perf_counter()
    async_results = asyncio.run(async_fetch())
    async_time = time.perf_counter() - start

    print("\nASYNC RESULTS")
    print("-" * 40)

    for subject, count in async_results:
        print(f"{subject:<25} {count:,}")

    print(f"\nAsync time: {async_time:.2f} seconds")


    # COMPARISON
  
    print("\nPERFORMANCE COMPARISON")
    print("-" * 40)

    print(f"Sync  : {sync_time:.2f} seconds")
    print(f"Async : {async_time:.2f} seconds")

    if async_time < sync_time:

        speedup = sync_time / async_time

        print(
            f"Async is approximately "
            f"{speedup:.2f}x faster."
        )

    else:
        print(
            "Async was not faster in this run. "
            "Network conditions can affect timings."
        )


if __name__ == "__main__":
    main()