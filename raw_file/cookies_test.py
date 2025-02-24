import re
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# from selenium_stealth import stealth

URL = "https://www.academy.com/p/nike-womens-court-legacy-next-nature-shoes"
CHROME_DRIVER_PATH = "../chromedriver.exe"
MAX_RETRIES = 5


def press_captcha_button(driver):
    wait = WebDriverWait(driver, 10)
    captcha_button = wait.until(EC.presence_of_element_located((By.ID, "px-captcha")))

    actions = ActionChains(driver)
    actions.click_and_hold(captcha_button).perform()
    time.sleep(10)
    actions.release().perform()

    print("The CAPTCHA button was successfully pressed and held.")


def extract_page_info(driver, retry_count):
    time.sleep(5)
    str_json = driver.page_source

    # Check for access denial
    if "Access to this page has been denied." in str_json:
        print(f"Access denied. Retry {retry_count}/{MAX_RETRIES}")
        return False

    try:

        # def extract_value(pattern, text, default=0):
        #     match = re.search(pattern, text)
        #     return match.group(1) if match else default
        #
        # price1 = extract_value(r'"priceCurrency":"USD","price":([\d.]+)', str_json, "0.0")
        # reviews_count2 = extract_value(r'"reviewCount":"(\d+)"', str_json, "0")
        # review_score3 = extract_value(r'"ratingValue":\s*([\d]+\.[\d]+)', str_json, "0.0")
        #
        # print(price1)
        # print(reviews_count2)
        # print(review_score3)

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

        product_item = {
            "name": name,
            "price": price,
            "main_color": main_color,
            "available_colors": available_colors,
            "reviews_count": reviews_count,
            "review_score": review_score,
        }

        print(product_item)
        return True

    except Exception as e:
        print(f'Error {str(e)}')
        return None


def main():
    retry_count = 0
    while retry_count < MAX_RETRIES:
        options = webdriver.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/110.0.0.0"
            "Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)
        # stealth(driver,
        #         languages=["en-US", "en"],
        #         vendor="Google Inc.",
        #         platform="Win32",
        #         webgl_vendor="Intel Inc.",
        #         renderer="Intel Iris OpenGL Engine",
        #         fix_hairline=True,
        #         )
        driver.get(URL)

        cookies = driver.get_cookies()
        with open("cookies.pkl", "wb") as f:
            pickle.dump(cookies, f)
        print("Cookies saved.")

        driver.refresh()
        with open("cookies.pkl", "rb") as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()

        press_captcha_button(driver)

        if extract_page_info(driver, retry_count + 1):
            driver.quit()
            return

        driver.quit()
        retry_count += 1
        print("Restarting...")

    print("Maximum retries reached. Exiting...")


if __name__ == "__main__":
    main()