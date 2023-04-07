from flask import render_template, request, redirect, url_for
from datetime import date, timedelta
from __init__ import app, db
from utils import check_and_update_tasks
from models import Task


@app.route('/help')
def help_page():
    return render_template('help.html')


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
