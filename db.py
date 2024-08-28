from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from env import port, host, database, user, password

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    content = Column(Text)
    checked = Column(Boolean, nullable=False)

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def create_tables():
    session = SessionLocal()
    try:
        message1 = Message(title='Breakfast', content='Eggs, bread, milk')
        message2 = Message(title='Sport', content='Football, basketball, formula 1')
        task1 = Task(title='Make breakfast', checked=True)
        task2 = Task(title='Play football', checked=False)

        session.add_all([message1, message2, task1, task2])
        session.commit()

        messages = get_messages()
        tasks = get_tasks()

        print(f'{messages=}\n')
        print(f'{tasks=}\n')
    finally:
        session.close()

def get_messages():
    session = SessionLocal()
    try:
        messages = session.query(Message).all()
        dict_messages = [message.__dict__ for message in messages]
        real_messages = [
            {
                'id': message['id'],
                'title': message['title'],
                'content': message['content']
            }

            for message in dict_messages
        ]

        return real_messages
    finally:
        session.close()

def add_message(message):
    session = SessionLocal()
    try:
        new_message = Message(title=message['title'], content=message['content'])
        session.add(new_message)
        session.commit()
        return get_messages()
    finally:
        session.close()

def delete_message(message_id):
    session = SessionLocal()
    try:
        message = session.query(Message).filter(Message.id == message_id).first()
        if message:
            session.delete(message)
            session.commit()
        return get_messages()
    finally:
        session.close()

def get_tasks():
    session = SessionLocal()
    try:
        tasks = session.query(Task).all()
        sorted_tasks = sorted(tasks, key=lambda task: task.__dict__['id'])
        dict_tasks = [task.__dict__ for task in sorted_tasks]
        real_tasks = [
            dict(
                id=task['id'],
                title=task['title'],
                content=task['content'],
                checked=task['checked']
            ) for task in dict_tasks
        ]
        return real_tasks
    finally:
        session.close()

def add_task(task):
    session = SessionLocal()
    try:
        new_task = Task(
            title=task['title'], 
            content=task.get('content', ''), 
            checked=task['checked']
        )
        session.add(new_task)
        session.commit()
        return get_tasks()
    finally:
        session.close()

def delete_task(task_id):
    session = SessionLocal()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            session.delete(task)
            session.commit()
        return get_tasks()
    finally:
        session.close()

def change_checked_value(task_id, checked):
    session = SessionLocal()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            task.checked = checked
            session.commit()
        return get_tasks()
    finally:
        session.close()

if __name__ == '__main__':
    create_tables()
