from fastapi import FastAPI
from routers.customer import router as customer_router
import sql_engine

app = FastAPI()
app.include_router(customer_router)

@app.on_event("startup")
def on_start_up() -> None:
    sql_engine.create_db_and_tables()

