from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated, Optional, Generator
from sqlmodel import Field, Session, SQLModel, create_engine

class CustomerBase(SQLModel):
    login: str = Field(index=True)
    name: Optional[str] = Field(default = None)
    surname: Optional[str] = Field(default = None, index = True)

class Customer(CustomerBase, table = True):
    """It will be returned to user"""
    id: Optional[int] = Field(default = None, primary_key=True)

    def __str__(self) -> str:
        return '{} with name = {} and surname = {}. Your id is {}'.\
            format(type(self).__name__, self.name, self.surname,self.id)

class CustomerCreate(CustomerBase):
    """It is a model to show user what they should provide to create customer"""
    pass

class CustomerUpdate(CustomerBase):
    login: Optional[str]
    name: Optional[str]
    surname: Optional[str]



sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()

@app.on_event("startup")
def on_start_up() -> None:
    create_db_and_tables()

@app.get("/get_customer/{customer_id}", status_code=status.HTTP_200_OK, response_model=Customer)
def read_customer(customer_id: int, session:SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail='Such customer does not exist')
    else:
        return customer
@app.post("/create_customer/", status_code=status.HTTP_201_CREATED, response_model=Customer)
def create_customer(customer_input: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_input) #here we validate user input (which is itself CustomerCreate) against Customer
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.patch("/update_customer/{customer_id}", status_code=status.HTTP_200_OK, response_model=Customer)
def update_customer(customer_id: int, customer_input: CustomerUpdate, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail='Such customer does not exist')
    else:
        for key, value in customer_input.dict(exclude_unset = True).items():
            setattr(customer, key, value)
    session.commit()
    session.refresh(customer)
    return customer

@app.delete("/delete_customer/{customer_id}", status_code=status.HTTP_200_OK, response_model=Customer)
def delete_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail='Such customer does not exist')
    session.delete(customer)
    session.commit()
    return customer
