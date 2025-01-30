from typing import Annotated
from sqlmodel import Session
from fastapi import Depends
from sql_engine import get_session

SessionDep = Annotated[Session, Depends(get_session)]
