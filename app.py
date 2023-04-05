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



class Task(db.Model):
    id = Column(Integer, primary_key=True)
    task = Column(String(255), nullable=False)
    due_date = Column(Date, nullable=False)

    def __init__(self, task, due_date):
        self.task = task
        self.due_date = due_date


if __name__ == '__main__':
    app.run(debug=True)
