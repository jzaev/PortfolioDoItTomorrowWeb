from sqlalchemy import Column, Integer, String, Date
from app import db


class Task(db.Model):
    id = Column(Integer, primary_key=True)
    task = Column(String(255), nullable=False)
    due_date = Column(Date, nullable=False)
    completed = Column(db.Boolean, default=False, nullable=False)

    def __init__(self, task, due_date):
        self.task = task
        self.due_date = due_date
        self.completed = False


class LastCheckDate(db.Model):
    id = Column(Integer, primary_key=True)
    check_date = Column(Date, nullable=False)

    def __init__(self, check_date):
        self.check_date = check_date
