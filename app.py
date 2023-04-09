from flask import Flask, render_template, request, redirect, url_for
from datetime import date, timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date

app = Flask(__name__)
tasks = []

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def index():
    check_and_update_tasks()

    today = date.today()
    tomorrow = today + timedelta(days=1)

    today_tasks = Task.query.filter_by(due_date=today).all()
    tomorrow_tasks = Task.query.filter_by(due_date=tomorrow).all()

    return render_template('index.html', today_tasks=today_tasks, tomorrow_tasks=tomorrow_tasks)


@app.route('/add-task', methods=['POST'])
def add_task():
    if request.form.get('task_today'):
        task = request.form.get('task_today')
        due_date = date.today()
    if request.form.get('task_tomorrow'):
        task = request.form.get('task_tomorrow')
        due_date = (date.today() + timedelta(days=1))

    if task and due_date:
        new_task = Task(task, due_date)
        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/toggle-task-completion/<int:task_id>', methods=['POST'])
def toggle_task_completion(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete-task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/move-task/<int:task_id>', methods=['POST'])
def move_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.due_date == date.today():
        task.due_date = date.today() + timedelta(days=1)
    else:
        task.due_date = date.today()
    db.session.commit()
    return redirect(url_for('index'))


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


def check_and_update_tasks():
    today = date.today()

    last_check_date = LastCheckDate.query.first()
    if last_check_date is None:
        new_date = LastCheckDate(today)
        db.session.add(new_date)
        db.session.commit()
        last_check_date = LastCheckDate.query.first()

    if last_check_date.check_date != today:


        # TODO Translate all comments
        # TODO separate module
        # TODO help
        # TODO Do css flexible
        # Delete all done tasks
        completed_tasks = Task.query.filter(Task.completed == True).all()
        for task in completed_tasks:
            db.session.delete(task)

        # all tasks move on today
        tasks_before_today = Task.query.filter(Task.due_date < today, Task.completed == False).all()
        for task in tasks_before_today:
            task.due_date = today
            db.session.add(task)

        # Refresh current date on database
        last_check_date.check_date = today
        db.session.add(last_check_date)
        db.session.commit()



if __name__ == '__main__':
    app.run(debug=True)
