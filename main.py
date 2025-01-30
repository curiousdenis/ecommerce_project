from fastapi import FastAPI
from typing import Generator
from sqlmodel import Session, SQLModel, create_engine
import routers

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

app = FastAPI()
app.include_router(routers.customer.router)

@app.on_event("startup")
def on_start_up() -> None:
    create_db_and_tables()

