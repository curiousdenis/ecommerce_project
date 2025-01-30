from typing import Annotated
from .main import get_session
from sqlmodel import Session
from fastapi import Depends

SessionDep = Annotated[Session, Depends(get_session)]
