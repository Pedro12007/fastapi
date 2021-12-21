#Python
from enum import unique
from typing import Optional

#Pydantic
from pydantic import BaseModel

#SQLAlquemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

#FastAPI
from fastapi import FastAPI

app = FastAPI()

#Objeto para crear modelos
Base = declarative_base()

#Modelos
class Moneda(Base):
    _tablename_ = "monedas"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    valor_moneda_a_dolar = Column(Integer(), nullable=False, unique=True)
    valor_dolar_a_moneda = Column(Integer(), nullable=False, unique=True)
    simbolo = Column(String(), nullable=False, unique=True)
    