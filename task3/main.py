from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def main() -> None:

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 5)
    driver.maximize_window()

    url_blazers = "https://henderson.ru/catalog/blazers/"
    driver.get(url_blazers)

    data = []
    page = 1
    i = 0

    while True:
        try:
            element = wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "list-product"))
            )

            products = driver.find_elements(By.CLASS_NAME, "list-product__item")

            for product in products:
                title = product.get_attribute("data-product-name").strip()
                price = product.get_attribute("data-product-unitsaleprice")
                category = product.get_attribute("data-product-category")
                link = product.find_element(By.CSS_SELECTOR, ".card-product__name a").get_attribute("href")
                img_url = product.find_element(By.CSS_SELECTOR, ".card-product__wrap-img img").get_attribute("src")

                i +=1

                data.append({
                    "id_item": i,
                    "title": title,
                    "price": price,
                    "category": category,
                    "link": link,
                    "img_url": img_url
                })

        except TimeoutException as _ex:
            print(_ex)
            break

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "a.pagination-next")  # Находим ссылку "Следующая"
            next_page_url = next_button.get_attribute("href") 
            driver.get(next_page_url)
            page += 1
            time.sleep(5)

        except:
            print(f"Число страниц: {page}")
            break
        
    df = pd.DataFrame(data)
    df.to_csv('data.csv')

    driver.close()


if __name__ == "__main__":
    main()


