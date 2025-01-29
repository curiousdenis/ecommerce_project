from fastapi import FastAPI, Depends, HTTPException
from typing import Union, Annotated
from dataclasses import dataclass
from sqlmodel import Field, Session, SQLModel, create_engine

@dataclass
class Customer(SQLModel, table = True):
    email: Field()
    name: str = Field()
    surname: str = Field(default = '')
    alliace: Union[str, None] = Field(default = '')
    id: int = Field(default = 0, primary_key=True)
    _current_id = 0
    def __post_init__(self) -> None:
        if self.alliace is None:
            self.alliace = '{}, your new unique alliace is = {}_{}'.format(type(self).__name__, self.name, self.surname)
        self.id = Customer._current_id
        Customer._current_id += 1

    def __str__(self) -> str:
        return '{} with name = {} and surname = {}. Your id is {} and alliace that you can use otherwise is {}'.\
            format(type(self).__name__, self.name, self.surname,self.id,self.alliace)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)



def get_session():
    with Session(engine) as session:
        return session

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()

@app.on_event("startup")
def on_start_up():
    create_db_and_tables()

@app.get("/get_customer/{customer_id}")
def read_customer(customer_id: int, session:SessionDep) -> Customer:
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail='Such customer does not exist')
    else:
        return customer
@app.put("/create_customer/")
def create_customer(customer: Customer, session: SessionDep) -> Customer:
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer
