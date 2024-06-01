from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

import os

psql_conn_url = os.getenv('PSQL_URL')
if psql_conn_url == None:
    psql_conn_url = 'postgresql://postgres:postgres@localhost:5432/fichi'


Base = declarative_base()
engine = create_engine(psql_conn_url)

class Feature(Base):
    __tablename__ = 'features'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    priority_id = Column(Integer, ForeignKey('priorities.id'), nullable=False)

    priorities = relationship("Priority", back_populates="feature")


class Priority(Base):
    __tablename__ = 'priorities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    coefficient = Column(Float)
    feature = relationship("Feature", back_populates="priorities")


def CreateTables():
    print("create tables")
    Base.metadata.create_all(engine)


def GetSession():
    Session = sessionmaker(bind=engine)
    return Session()


class DeleteError(Exception):
    pass


def AddPriority(name, coefficient):
    """
    Добавление приоритета
    """
    with GetSession() as session:
        new_priority = Priority(name=name, coefficient=coefficient)
        session.add(new_priority)
        session.commit()



def AddFeature(name, priority_id):
    """
    Добавление фичи
    """
    
    with GetSession() as session:
        new_feature = Feature(name=name, priority_id=priority_id)
        session.add(new_feature)
        session.commit()
        print("commited")
    
    


def GetFeatureByName(name):
    """
    Поиск фичи по её имени
    """
    with GetSession() as session:
        return session.query(Feature).filter(Feature.name == name).first()
    
    
    
         



def DelPriority(priority_id):
    """
    Удаление приоритета
    """
    with GetSession() as session:
        priority = session.query(Priority).filter(Priority.id == priority_id).first()
        if priority:
            try:
                session.delete(priority)
                session.commit()
            except IntegrityError:
                session.rollback()
                print("Ошибка: Невозможно удалить приоритет, на который есть ссылки.")
            finally:
                pass
        else:
            raise DeleteError("Ошибка. Приоритет не найден по этому id")



def DelFeature(feature_id):
    """
    Удаление фичи
    """
    with GetSession() as session:
        feature = session.query(Feature).filter(Feature.id == feature_id).first()
        if feature:
            session.delete(feature)
            session.commit()
        else:
            raise DeleteError("Ошибка. Фича не найдена по этому id")

def EditPriority(priority_id, name, coefficient):
    """
    Редактирование приоритета
    """
    with GetSession() as session:
        priority = session.query(Priority).filter(Priority.id == priority_id).first()
        if priority:
            priority.name = name
            priority.coefficient = coefficient
            session.commit()
        else:
            raise DeleteError("Ошибка. Приоритет не найден по этому id")

def EditFeature(feature_id, priority_id, name):
    """
    Редактирование фичи
    """
    with GetSession() as session:
        feature = session.query(Feature).filter(Feature.id == feature_id).first()
        if feature:
            feature.priority_id = priority_id
            feature.name = name
            session.commit()
        
        else:
            session.close()
            raise DeleteError("Ошибка. Фича не найдена по этому id")

def GetObjects():
    """
    Получение одного объекта в виде гибридного словаря
    """
    with GetSession() as session:
        features = session.query(Feature).all()

        features_dicts = []
        for feature in features:
            feature_dict = {
                "id": feature.id,
                "name": feature.name,
                "priority": {
                    "id": feature.priorities.id,
                    "name": feature.priorities.name,
                    "coefficient": feature.priorities.coefficient
                }
            }
            features_dicts.append(feature_dict)
    
        return features_dicts




    


def GetFeatureById(feature_id):
    with GetSession() as session:
        
        feature = session.query(Feature).filter(Feature.id == feature_id).first()
       
        feature_dict = {
            "id": feature.id,
            "name": feature.name,
            "priority": {
                "id": feature.priorities.id,
                "name": feature.priorities.name,
                "coefficient": feature.priorities.coefficient
            }
        }
        
        return feature_dict



CreateTables()

