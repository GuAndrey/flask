from datetime import date
from sqlalchemy import (Column, Integer, String, Boolean, Text, Date, 
                        ForeignKey, create_engine)
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

engine = create_engine('sqlite:///app.db', echo=True)
Base = declarative_base(bind=engine)


class AccountExists(Exception):
    '''
    Authentification pair already in db
    '''

class AccountNotFound(Exception):
    '''
    Authentification pair not found in db
    '''

class Abstract:
    id = Column(Integer, primary_key=True)
    created_on = Column(Date, default=date.today())


class User(Abstract, Base):
    __tablename__ = 'users'
    username = Column(String(20), nullable=False, unique=True)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(60), nullable=False)

    tasks = relationship("Task", cascade="all, delete-orphan")

    def __str__(self):
        return ' | '.join([self.id, self.username, self.email, self.password])


class Task(Abstract, Base):
    __tablename__ = 'tasks'
    title = Column(String(20), nullable=False, unique=True)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    details = Column(Text)
    deadline = Column(Date)
    status = Column(Boolean, default=0)

    author = relationship(User)

    def __str__(self):
        return ' | '.join([self.id, self.title, self.status])

# Base.metadata.create_all()

def add_user(name, email, password):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = User(username=name, email=email, password=password)
    try:
        session.add(user)
        session.commit()
    except IntegrityError:
        raise AccountExists
    finally:
        session.close()


def check_user(email, password):
    
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(email=email, 
                                         password=password).first()
    
    session.close()

    if not user:
        raise AccountNotFound

    return user.username


def get_user_tasks(name):
    
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(username=name).first()
    user_tasks = user.tasks
    session.close()

    return user_tasks


def create_user_task(name, title, details='', deadline=None):
    engine = create_engine('sqlite:///app.db', echo=True)
    session = Session(bind=engine)
    user = session.query(User).filter_by(username=name).first()
    user_tasks = user.tasks
    new_task = Task(title=title, details=details, deadline=deadline)
    user_tasks.append(new_task)
    session.commit()
    session.close()
