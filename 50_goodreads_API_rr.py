import requests
from bs4 import BeautifulSoup
import json

# Function to scrape books by genre across multiple pages
def scrape_all_books_by_genre(genre):
    base_url = f"https://www.goodreads.com/shelf/show/{genre}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    books = []
    page = 1
    while True:
        # Construct the URL for each page
        url = f"{base_url}?page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            break
        
        # Parse the HTML response
        soup = BeautifulSoup(response.text, "html.parser")
        book_elements = soup.select(".bookTitle")
        
        if not book_elements:
            # Break the loop if no more books are found
            break
        
        for book in book_elements:
            title = book.get_text(strip=True)
            link = "https://www.goodreads.com" + book[href]
            books.append({"title": title, "link": link})
        
        print(f"Scraped page {page} with {len(book_elements)} books.")
        page += 1
    
    return books

# Save all books by genre to JSON
def save_all_books_by_genre(genre, output_file="all_genre_books.json"):
    books = scrape_all_books_by_genre(genre)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(books)} books to {output_file}")

# Example usage
genre = "fantasy"  # Change this to your desired genre
save_all_books_by_genre(genre, output_file=f"{genre}_all_books.json")
