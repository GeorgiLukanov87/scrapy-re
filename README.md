# Shoes Scraper

This is a web scraping project built with Scrapy and Selenium to extract product details from an online shoe store.

## Features
- Scrapes product details such as name, price, color options, and reviews.
- Uses Selenium to handle JavaScript-rendered pages.
- Implements retry mechanisms and proxy rotation.
- Saves extracted data as structured `ProductItem` objects.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/shoes-scraper.git
   cd shoes-scraper
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

Run the spider using and save the data in json format:
```sh
scrapy crawl academy -o products.jsonl
```

## Project Structure
```
shoes-scraper/
│── shoes/
│   ├── spiders/
│   │   ├── shoes_spider.py  # Main spider
│   ├── middlewares.py  # Custom middlewares
│   ├── settings.py  # Project settings
│   ├── items.py  # Data structure for scraped items
│── README.md  # Documentation
│── requirements.txt  # Dependencies
```

## Configuration
The settings file (`settings.py`) includes configurations for:
- Selenium middleware
- Auto-throttling

## Dependencies
- Scrapy
- Scrapy-Selenium
- Selenium
- WebDriver Manager

## License
This project is licensed under the MIT License.

