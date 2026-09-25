import requests

def get_books(subject, page, limit):
    try:

        url = f"https://openlibrary.org/search.json?q={subject}&page={page}&limit={limit}&fields=title"
        data = requests.get(url, timeout = 10)
        return data.json()
    except Exception as e:
        print(f"Error fetching books: {e}")


print(get_books("python", 1, 10))