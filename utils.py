from datetime import date
from models import LastCheckDate, Task
from app import db


def check_and_update_tasks():
    today = date.today()

    # Make first row if needed
    last_check_date = LastCheckDate.query.first()
    if last_check_date is None:
        new_date = LastCheckDate(today)
        db.session.add(new_date)
        db.session.commit()
        last_check_date = LastCheckDate.query.first()

    if last_check_date.check_date != today:

        # Delete all done tasks
        completed_tasks = Task.query.filter(Task.completed).all()
        for task in completed_tasks:
            db.session.delete(task)

        # all tasks move on today
        tasks_before_today = Task.query.filter(Task.due_date < today, not Task.completed).all()
        for task in tasks_before_today:
            task.due_date = today
            db.session.add(task)

        # Refresh current date on database
        last_check_date.check_date = today
        db.session.add(last_check_date)
        db.session.commit()
