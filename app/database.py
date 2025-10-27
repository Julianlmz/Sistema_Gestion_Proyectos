from sqlmodel import Session, create_engine, SQLModel
from fastapi import Depends
from typing import Annotated

engine = create_engine('sqlite:///Proyectos.db')

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]