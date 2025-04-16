import time

import pandas as pd
from fastapi import FastAPI
from fastapi import Query
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from sqlalchemy import create_engine, text
from sqlalchemy import inspect

app = FastAPI()

#Settings of Data Base
db_name = "user"
db_user = "user"
db_password = "parol"
db_host = "localhost"
db_port = "5432"

engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

with engine.connect() as conn:
    print("Connected successfuly")


create_table_query = """
CREATE  TABLE IF NOT EXISTS items (
    id_item SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    price NUMERIC,
    category TEXT,
    link TEXT,
    img_url TEXT
);
"""

with engine.connect() as conn:
    inspector = inspect(conn)

    if 'items' in inspector.get_table_names():
        print("Table already exists")
    else:
        conn.execute(text(create_table_query))
        conn.commit()   
        print("Table was created")

    
@app.get("/")
def home():
    return {"message": "API is working!"}

@app.get("/parse")
def parse(url: str = Query(..., description="URL of page for parse")):

    try:
        with engine.connect() as conn:
            truncate_query = text("TRUNCATE TABLE items RESTART IDENTITY;")
            conn.execute(truncate_query)
            conn.commit()
            
    except Exception as _ex:
        print(_ex)
        
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 15)
    driver.maximize_window()

    driver.get(url)

    data = []
    item_id = 0

    try:
        while True:
            try:
            
                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "list-product")))
                products = driver.find_elements(By.CLASS_NAME, "list-product__item")

                for product in products:
                    title = product.get_dom_attribute("data-product-name").strip()
                    price = product.get_attribute("data-product-unitsaleprice")
                    category = product.get_attribute("data-product-category")
                    link = product.find_element(By.CSS_SELECTOR, ".card-product__name a").get_attribute("href")
                    img_url = product.find_element(By.CSS_SELECTOR, ".card-product__wrap-img img").get_attribute("src")

                    item_id += 1

                    data.append({
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
                next_button = driver.find_element(By.CSS_SELECTOR, "a.pagination-next")  
                next_page_url = next_button.get_attribute("href") 
                driver.get(next_page_url)
                time.sleep(5)

            except:
                break

        with engine.begin() as conn:
            for item in data:
                query = text("""
                    INSERT INTO items (title, price, category, link, img_url)
                    VALUES (:title, :price, :category, :link, :img_url)
                """)
                conn.execute(query, item)


    except Exception as e:
        return {"error": str(e)}
    finally:
        driver.quit()
    
    return {"message": f"Data parsing completed. {item_id} items were parsed."}

@app.get("/data")
def get_data():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM items")).fetchall()

    data = [
        {
            "id_item": row[0],
            "title": row[1],
            "price": row[2],
            "category": row[3],
            "link": row[4],
            "img_url": row[5]
        }
        for row in result
    ]

    return {"items": data}
    
