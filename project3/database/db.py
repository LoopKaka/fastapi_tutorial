from contextlib import contextmanager
from typing import Annotated
from dotenv import load_dotenv
import os
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session

load_dotenv()

USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')

DB_URL=f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@localhost:3306/fastapi_tutorial"

# For docker use below
# DB_URL=f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@host.docker.internal:3306/fastapi_tutorial"

engine = create_engine(DB_URL, echo=True)

def create_table():
    SQLModel.metadata.create_all(engine)

@contextmanager
def get_session_context():
    session = Session(engine)

    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()

def get_session():
    with get_session_context() as session:
        yield session

SessionDependency = Annotated[Session, Depends(get_session)]