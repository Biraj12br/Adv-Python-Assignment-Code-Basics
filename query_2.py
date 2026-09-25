import requests


BASE = "https://openlibrary.org/search.json"

SUBJECT = "python"
PAGE_SIZE = 10


def get_page(page, limit=PAGE_SIZE):
    """Ask the Open Library API for ONE page."""

    params = {
        "q": SUBJECT,
        "page": page,
        "limit": limit,
        "fields": "title,first_publish_year,key"
    }

    response = requests.get(
        BASE,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def full_load():

    books = []
    page_number = 1

    while page_number < 10:

        data = get_page(page_number)

        page = data["docs"]

        if not page:
            break

        books.extend(page)

        print(
            f"  ... pulled page={page_number}, "
            f"running total={len(books)}"
        )

        # Open Library tells us the total number of results
        total = data["numFound"]

        if len(books) >= total:
            break

        page_number += 1

    return books


def incremental_load(books, watermark):
    """
    Pull only books newer than the watermark.

    Here we are using first_publish_year as the watermark.
    """

    new_books = []

    for book in books:

        publish_year = book.get("first_publish_year")

        if publish_year is not None and publish_year > watermark:
            new_books.append(book)

    return new_books


def main():

    print("OPEN LIBRARY INGESTION\n")

    try:

        # FULL LOAD
        
        books = full_load()

        print(
            f"\nFULL LOAD: pulled "
            f"{len(books)} books from the API"
        )

    except Exception as error:

        print(f"API error: {error}")
        return

    # Show a few records

    print("\nSample of what arrived:")

    for book in books[:5]:

        print(
            f"  - {book.get('title')} "
            f"({book.get('first_publish_year', 'Unknown')})"
        )

    
    # WATERMARK

    years = [
        book["first_publish_year"]
        for book in books
        if book.get("first_publish_year") is not None
    ]

    watermark = max(years) - 5

    
    # INCREMENTAL LOAD
   

    todays_new = incremental_load(
        books,
        watermark
    )

    print(
        f"\nINCREMENTAL NEXT RUN: "
        f"watermark = year {watermark}"
    )

    print(
        f"  only {len(todays_new)} new books "
        f"would be pulled, not all {len(books)}"
    )

    print("\nNew books:")

    for book in todays_new[:5]:

        print(
            f"  - {book.get('title')} "
            f"({book.get('first_publish_year')})"
        )

    print("\nFull load once, incremental every run after.")


if __name__ == "__main__":
    main()