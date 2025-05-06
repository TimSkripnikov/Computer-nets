from fastapi import FastAPI, Query
from sqlalchemy import create_engine, text
from sqlalchemy import inspect

app = FastAPI()

db_name = "mydb"
db_user = "artem"
db_password = "12345678"
db_host = "my_postgres"  
db_port = "5432"

engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

with engine.connect() as conn:
    print("Connected successfully")

create_table_query = """
CREATE TABLE IF NOT EXISTS urls (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL
);
"""

with engine.connect() as conn:
    inspector = inspect(conn)

    if 'urls' in inspector.get_table_names():
        print("Table already exists")
    else:
        conn.execute(text(create_table_query))
        conn.commit()
        print("Table is created")

@app.get("/")
def home():
    return {"message": "API is working!"}

@app.get("/add_url")
def add_url(url: str = Query(..., description="URL to add to the database")):
    try:
        with engine.connect() as conn:
            query = text("INSERT INTO urls (url) VALUES (:url)")
            conn.execute(query, {"url": url})
            conn.commit()
        return {"message": "URL added successfully!"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/get_urls")
def get_urls():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM urls")).fetchall()
        
        data = [
            {
                "id": row[0],
                "url": row[1]
            }
            for row in result
        ]
        
        return {"urls": data}
    except Exception as e:
        return {"error": str(e)}