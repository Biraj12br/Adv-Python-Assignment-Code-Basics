import requests
import time
import os
from concurrent.futures import ProcessPoolExecutor


BASE_URL = "https://openlibrary.org/search.json"

GENRES = [
    "python",
    "science",
    "history",
    "fantasy",
    "technology",
    "romance",
    "mathematics",
    "business"
]

BOOKS_PER_GENRE = 100


# FETCH DATA

def fetch_books(genre):
    """Fetch books for one genre from Open Library."""

    params = {
        "q": genre,
        "page": 1,
        "limit": BOOKS_PER_GENRE,
        "fields": "title,first_publish_year"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    return genre, data["docs"]


# CPU-HEAVY SCORING

def calculate_score(args):
   

    genre, books = args

    total_score = 0

    for book in books:

        title = book.get("title", "")

        year = book.get("first_publish_year") or 0

        # CPU-heavy calculation
        score = 0

        for i in range(500_000):

            score += (i * i + len(title) * 31 + year) % 97

        total_score += score

    return genre, total_score


# SERIAL VERSION

def serial_processing(data):
    """Process every genre one after another."""

    results = []

    for item in data:

        result = calculate_score(item)

        results.append(result)

    return results


# PARALLEL VERSION

def parallel_processing(data):
    """Process genres across CPU cores."""

    with ProcessPoolExecutor() as pool:

        results = list(
            pool.map(calculate_score, data)
        )

    return results


# MAIN

def main():

    print("OPEN LIBRARY CPU PROCESSING")
    print("=" * 50)

    # MACHINE INFORMATION

    cores = os.cpu_count()

    print(f"CPU cores available: {cores}")
    print(f"Genres: {len(GENRES)}")
    print()

    # FETCH DATA

    print("Fetching data from Open Library...")

    data = []

    for genre in GENRES:

        genre_name, books = fetch_books(genre)

        print(
            f"  {genre_name:<20} "
            f"{len(books)} books"
        )

        data.append((genre_name, books))

    print()

    # SERIAL

    print("Running SERIAL processing...")

    start = time.perf_counter()

    serial_results = serial_processing(data)

    serial_time = time.perf_counter() - start

    print(
        f"Serial time: "
        f"{serial_time:.2f} seconds"
    )

    # PARALLEL

    print("\nRunning PARALLEL processing...")

    start = time.perf_counter()

    parallel_results = parallel_processing(data)

    parallel_time = time.perf_counter() - start

    print(
        f"Parallel time: "
        f"{parallel_time:.2f} seconds"
    )

    # VERIFY RESULTS

    print("\nRESULT VERIFICATION")
    print("-" * 50)

    # pool.map preserves the order of the input,
    # so the lists can be compared directly.

    results_match = serial_results == parallel_results

    print(f"Results identical: {results_match}")

    if not results_match:
        print("ERROR: Results do not match!")

    # PERFORMANCE
  

    print("\nPERFORMANCE")
    print("-" * 50)

    print(f"CPU cores       : {cores}")
    print(f"Serial time     : {serial_time:.2f} sec")
    print(f"Parallel time   : {parallel_time:.2f} sec")

    if parallel_time < serial_time:

        speedup = serial_time / parallel_time

        print(
            f"Speedup         : "
            f"{speedup:.2f}x"
        )

        print("Parallel processing is faster.")

    else:

        print(
            "Parallel processing was not faster "
            "in this run."
        )


if __name__ == "__main__":
    main()