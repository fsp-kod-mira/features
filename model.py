from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import IntegrityError

import os

psql_conn_url = os.getenv('PSQL_URL')
if psql_conn_url == None:
    psql_conn_url = 'postgresql://nlclover:rootNodeJS1243@localhost:5432/fichi'


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
    session = GetSession()
    new_priority = Priority(name=name, coefficient=coefficient)
    session.add(new_priority)
    session.commit()
    session.close()


def AddFeature(name, priority_id):
    """
    Добавление фичи
    """
    session = GetSession()
    new_feature = Feature(name=name, priority_id=priority_id)
    session.add(new_feature)
    session.commit()
    session.close()

def DelPriority(priority_id):
    """
    Удаление приоритета
    """
    session = GetSession()
    priority = session.query(Priority).filter(Priority.id == priority_id).first()
    if priority:
        try:
            session.delete(priority)
            session.commit()
        except IntegrityError:
            session.rollback()
            print("Ошибка: Невозможно удалить приоритет, на который есть ссылки.")
        finally:
            session.close()
    else:
        session.close()
        raise DeleteError("Ошибка. Приоритет не найден по этому id")

def DelFeature(feature_id):
    """
    Удаление фичи
    """
    session = GetSession()
    feature = session.query(Feature).filter(Feature.id == feature_id).first()
    if feature:
        session.delete(feature)
        session.commit()
        session.close()
    else:
        session.close()
        raise DeleteError("Ошибка. Фича не найдена по этому id")

def EditPriority(priority_id, name, coefficient):
    """
    Редактирование приоритета
    """
    session = GetSession()
    priority = session.query(Priority).filter(Priority.id == priority_id).first()
    if priority:
        priority.name = name
        priority.coefficient = coefficient
        session.commit()
        session.close()
    else:
        session.close()
        raise DeleteError("Ошибка. Приоритет не найден по этому id")

def EditFeature(feature_id, priority_id, name):
    """
    Редактирование фичи
    """
    session = GetSession()
    feature = session.query(Feature).filter(Feature.id == feature_id).first()
    if feature:
        feature.priority_id = priority_id
        feature.name = name
        session.commit()
        session.close()
    else:
        session.close()
        raise DeleteError("Ошибка. Фича не найдена по этому id")

def GetObjects():
    """
    Получение одного объекта в виде гибридного словаря
    """
    session = GetSession()
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
    
    session.close()
    return features_dicts

CreateTables()




    


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

