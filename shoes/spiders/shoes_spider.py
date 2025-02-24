from scrapy_selenium import SeleniumRequest
import scrapy
import re
import logging
from ..items import ProductItem

logging.basicConfig(
    filename='spider.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class AcademySpider(scrapy.Spider):
    name = "academy"
    start_urls = ["https://www.academy.com/p/nike-womens-court-legacy-next-nature-shoes"]

    def start_requests(self):
        """Use SeleniumRequest to render JavaScript."""
        yield SeleniumRequest(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        """Main parsing function for extracting product data."""
        if not self._handle_request_errors(response):
            return

        script_data = response.css('script').extract()
        if not script_data:
            self.logger.warning("No JSON-LD script found! CAPTCHA may be blocking access.")
            logging.warning("No JSON-LD script found! CAPTCHA may be blocking access.")
            return

        str_json = ",".join([str(el) for el in script_data])
        yield self._extract_product_data(str_json)

    def _handle_request_errors(self, response):
        """Retry mechanism for handling failed requests."""
        max_retries = 5
        retry_count = response.meta.get('retry_count', 0)

        if response.status != 200:
            if retry_count < max_retries:
                self.logger.warning(
                    f"Retrying {response.url} ({retry_count + 1}/{max_retries}) due to status {response.status}"
                )
                yield SeleniumRequest(
                    url=response.url,
                    callback=self.parse,
                    dont_filter=True,
                    meta={'retry_count': retry_count + 1}
                )
            return False
        return True

    def _extract_product_data(self, str_json):
        """Extracts product details using regex."""
        try:
            product_names = re.findall(r'"Product","name":"([^"]+)"', str_json)
            name = product_names[0].split("Shoes")[0] + "Shoes" if product_names else "No name"

            # Extract all prices
            prices = re.search(r'"priceCurrency":"USD","price":([\d.]+)', str_json)
            price = prices.group(1) if prices else 0.0

            # Extract all colors
            colors = [str(c).split(name)[1].strip() for c in product_names]
            main_color = colors[0] if colors else "Unknown color"
            available_colors = colors[1:]

            # Extract review count
            review_count_match = re.search(r'"reviewCount":"(\d+)"', str_json)
            reviews_count = review_count_match.group(1) if review_count_match else 0

            # Extract review_score
            review_score_match = re.search(r'"ratingValue":\s*([\d]+\.[\d]+)', str_json)
            review_score = review_score_match.group(1) if review_score_match else 0.0

            return ProductItem(
                name=name,
                price=price,
                color=main_color,
                available_colors=available_colors,
                review_count=reviews_count,
                reviews_score=review_score,
            )

        except Exception as e:
            self.logger.error(f"Error extracting product data: {e}")
            logging.error(f"Error extracting product data: {e}")
            return None
