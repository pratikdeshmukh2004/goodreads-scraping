# Goodreads Scraping with Flask

This project is a Python-based web scraper that extracts book details from Goodreads and presents them via a Flask web API. It uses Selenium to scrape book information such as prices, product links, and titles from Goodreads wishlists and Amazon product pages.

## Features

- **Scraping Goodreads Wishlists**: Extracts book details like titles and prices from Goodreads.
- **Concurrent Data Retrieval**: Uses multithreading to scrape book details in batches, improving performance for large wishlists.
- **Flask API**: Provides a RESTful interface to retrieve scraped book details from a given Goodreads wishlist URL.
- **Gift a Book Feature**: Provides functionality to simulate purchasing a book from Amazon by using credentials stored in environment variables.

## Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.x
- Required Python libraries (listed in `requirements.txt`)
- Chrome browser and [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
- Selenium WebDriver
- A Goodreads account for scraping book wishlists

### Required Libraries

Install the required Python libraries using the following command:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should include:
- `Flask`
- `selenium`
- `webdriver-manager`
- `python-dotenv`
- `concurrent.futures`

## Installation and Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/pratikdeshmukh2004/goodreads-scraping.git
   cd goodreads-scraping
   ```

2. **Install ChromeDriver (using WebDriver Manager):**
   The script will automatically install the appropriate version of ChromeDriver using WebDriver Manager.

3. **Create a `.env` File:**
   Create a `.env` file to store sensitive data like your Amazon account credentials:

   ```bash
   PHONE=<your_amazon_phone_or_email>
   PASSWORD=<your_amazon_password>
   ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Flask Application

1. **Run the Flask server:**

   ```bash
   python app.py
   ```

   The server will run on `http://127.0.0.1:5000` by default.

### API Endpoints

#### 1. Scrape Books from a Goodreads Wishlist

   **Endpoint:**

   ```http
   GET /books
   ```

   **Parameters:**

   - `wishlist`: The Goodreads wishlist URL.

   **Example Request:**

   ```http
   GET http://127.0.0.1:5000/books?wishlist=https://www.goodreads.com/review/list/1234567890?shelf=wishlist
   ```

   **Response:**

   ```json
   {
       "status": "success",
       "count": 10,
       "books": [
           {
               "title": "Book Title 1",
               "price": [
                   {"Hardcover": "$25.99"},
                   {"Kindle": "$9.99"}
               ],
               "product_link": "https://www.amazon.com/..."
           },
           {
               "title": "Book Title 2",
               "price": [
                   {"Paperback": "$14.99"},
                   {"Kindle": "$6.99"}
               ],
               "product_link": "https://www.amazon.com/..."
           }
       ]
   }
   ```

#### 2. Simulate Gifting a Book

   **Endpoint:**

   ```http
   GET /gift_book
   ```

   **Parameters:**

   - `url`: Amazon product URL for the book to be gifted.

   **Example Request:**

   ```http
   GET http://127.0.0.1:5000/gift_book?url=https://www.amazon.com/...
   ```

   **Response:**

   ```json
   {
       "status": "success",
       "message": "Gift process initiated"
   }
   ```

### Selenium Scraper

The main scraping logic is located in the `scrap_data.py` file and performs the following tasks:
- Loads all pages from a Goodreads wishlist.
- Extracts book IDs and retrieves price details from Amazon.
- Automates the gift purchasing process by logging into Amazon.

### Multithreading

The application uses Python's `concurrent.futures.ThreadPoolExecutor` to scrape books in batches for better performance.

## Limitations

- **Goodreads Terms of Service**: Ensure that you comply with Goodreads' policies when scraping their site.
- **Amazon CAPTCHA**: If you automate too many requests in a short time, Amazon might trigger CAPTCHA challenges.
- **Session Management**: Keep in mind that long scraping sessions might require handling timeouts or session expirations for both Goodreads and Amazon.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
