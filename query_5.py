import pandas as pd
import os


SALES_CSV = "sales.csv"
CHUNK_SIZE = 50_000


def main():

    print("SALES CSV PROCESSING\n")

    
    # 1. STREAM THE FILE AND CALCULATE REVENUE BY GENRE
    

    rows_seen = 0
    revenue_by_genre = {}

    for chunk in pd.read_csv(SALES_CSV, chunksize=CHUNK_SIZE):

        rows_seen += len(chunk)

        # Calculate revenue for this chunk
        chunk["revenue"] = chunk["price"] * chunk["quantity"]

        # Calculate revenue by genre for this chunk
        genre_revenue = (
            chunk.groupby("genre")["revenue"]
            .sum()
        )

        # Add this chunk's revenue to the running total
        for genre, revenue in genre_revenue.items():

            revenue_by_genre[genre] = (
                revenue_by_genre.get(genre, 0) + revenue
            )

    print("CHUNKED REVENUE")
    print("-" * 40)

    print(f"Rows processed: {rows_seen:,}")
    print(f"Chunk size: {CHUNK_SIZE:,}")

    for genre, revenue in sorted(revenue_by_genre.items()):
        print(f"{genre:<20} ₹{revenue:,.2f}")

    print("\nThe complete CSV was never loaded into memory at once.")



    # 2. MEMORY OPTIMIZATION


    # Read only ONE chunk for the memory comparison
    chunk = pd.read_csv(
        SALES_CSV,
        chunksize=CHUNK_SIZE
    ).get_chunk()

    # Memory BEFORE optimization
    memory_before = (
        chunk.memory_usage(deep=True).sum()
    )

    print("\nMEMORY OPTIMIZATION")
    print("-" * 40)

    print(
        f"Memory before optimization: "
        f"{memory_before / 1024**2:.2f} MB"
    )


    # Convert price and rating to float32
    chunk["price"] = chunk["price"].astype("float32")
    chunk["rating"] = chunk["rating"].astype("float32")

    # Convert repeated string columns to category
    chunk["genre"] = chunk["genre"].astype("category")
    chunk["city"] = chunk["city"].astype("category")
    chunk["payment_type"] = (
        chunk["payment_type"].astype("category")
    )


    # Memory AFTER optimization

    memory_after = (
        chunk.memory_usage(deep=True).sum()
    )

    reduction = (
        (memory_before - memory_after)
        / memory_before
        * 100
    )

    print(
        f"Memory after optimization : "
        f"{memory_after / 1024**2:.2f} MB"
    )

    print(
        f"Memory reduction          : "
        f"{reduction:.2f}%"
    )


if __name__ == "__main__":
    main()