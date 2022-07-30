from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from settiings import DATABASE_URL

ENGINE = create_engine(DATABASE_URL)


if not database_exists(ENGINE.url):
    create_database(ENGINE.url)


DeclarativeBase = declarative_base()


class Supply(DeclarativeBase):
    __tablename__ = 'supply'

    id = Column(Integer, primary_key=True)
    order_number = Column(Integer)
    price_in_valute = Column(Integer)
    price_in_rub = Column(Integer)
    date = Column(DateTime)

    def __repr__(self):
        return f'Supply dict: {self.__dict__}'


DeclarativeBase.metadata.create_all(ENGINE)


class SuppliesManager():
    """Uses for working with Supply objects in database."""

    def __init__(self):
        self.engine = ENGINE
        self.Session = sessionmaker(self.engine)

    def get_all_supplies(self) -> List[Supply]:
        with self.Session() as session:
            supplies = session.query(Supply).all()
            return supplies

    def get_supply_by_id(self, identifier: int) -> Supply:
        with self.Session() as session:
            supply = session.query(Supply).filter(Supply.id == identifier).first()
            return supply

    def get_supply_by_order_number(self, order_number: int) -> Supply:
        with self.Session() as session:
            supply = session.query(Supply).filter(Supply.order_number == order_number).first()
            return supply

    def add_supply(self, order_number: int, price_in_valute: int, price_in_rub: int, date: datetime) -> Supply:
        with self.Session() as session:
            supply = Supply(order_number=order_number, price_in_valute=price_in_valute,
                            price_in_rub=price_in_rub, date=date)
            session.add(supply)
            session.commit()
            return supply

    def update_supply(self, identifier: int, order_number: int, price_in_valute: int, price_in_rub: int, date: datetime) -> Supply:
        with self.Session() as session:
            supply = session.query(Supply).filter(Supply.id == identifier).first()
            supply.order_number = order_number
            supply.price_in_valute = price_in_valute
            supply.price_in_rub = price_in_rub
            supply.date = date
            session.commit()
            return supply

    def add_multiple_supplies(self, supplies: List[Supply]) -> List[Supply]:
        with self.Session() as session:
            for supply in supplies:
                session.add(supply)
            session.commit()
            return supplies

    def update_multiple_supplies(self, supplies: List[Supply]) -> List[Supply]:
        with self.Session() as session:
            for supply in supplies:
                supply_from_db = session.query(Supply).filter(
                    Supply.order_number == supply.order_number).first()
                supply_from_db.order_number = supply.order_number
                supply_from_db.price_in_valute = supply.price_in_valute
                supply_from_db.price_in_rub = supply.price_in_rub
                supply_from_db.date = supply.date
            session.commit()

    def delete_all_supplies(self) -> None:
        with self.Session() as session:
            session.query(Supply).delete()
            session.commit()
