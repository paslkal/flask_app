from flask import Flask, render_template, request, jsonify
from datetime import datetime
from db import get_messages, add_message, delete_message
from db import get_tasks, add_task, delete_task, change_checked_value

PORT = 5500
HOST = '127.0.0.1'
link_home = f'http://{HOST}:{PORT}/'
link_blog = f'http://{HOST}:{PORT}/blog'
link_todo = f'http://{HOST}:{PORT}/todo'

app = Flask(__name__)

@app.route('/')
def index():
    year = datetime.now().year
    
    return render_template(
        'home.html', 
        link_blog=link_blog, 
        link_todo=link_todo,
        link_home=link_home,
        year=year
    )

@app.route('/blog')
def blog():    

    year = datetime.now().year

    messages = get_messages()

    return render_template(
        'blog.html', 
        messages=messages, 
        year=year, 
        link_blog=link_blog, 
        link_todo=link_todo,
        link_home=link_home
    )

@app.route('/todo')
def todo():
    
    year = datetime.now().year

    tasks = get_tasks()

    return render_template(
        'todo.html', 
        tasks=tasks,
        link_blog=link_blog, 
        link_todo=link_todo,
        link_home=link_home,
        year=year
    )

@app.post('/api/message')
def add_message_from_form():
    title = request.form.get('title')
    content = request.form.get('content')

    if (not(title and content)):
        return f'<h1>Didnt have title or content. Go back to <a href="{link_blog}">Home</a></h1>'

    message = dict(title=title, content=content)

    add_message(message)        

    return f'<h1>Message recieved. Go back to <a href="{link_blog}">Home</a></h1>'

@app.delete('/api/message/<int:message_id>')
def delete_message_from_page(message_id):
    delete_message(message_id)    

    messages = get_messages()

    return jsonify(messages)

# TODO: dont hard coding content and cheked variables
@app.post('/api/task')
def add_task_from_form():
    title = request.form.get('title')
    content = None
    checked = False
    if not title:
        return f'<h1>Didnt have content in task. Go back to <a href="{link_blog}">Home</a></h1>'

    task = dict(title=title, content=content, checked=checked)

    add_task(task)

    return f'<h1>Task recieved. Go back <a href="{link_todo}">TODO App</a></h1>'


@app.delete('/api/task/<int:task_id>')
def delete_task_from_page(task_id):
    delete_task(task_id)
    tasks = get_tasks()

    return jsonify(tasks)


@app.put('/api/task/checkbox')
def change_checkbox():
    data = request.get_json()

    task_id = data['id']
    checked = data['checked']

    change_checked_value(task_id, checked)

    return get_tasks()

if __name__=='__main__':
    app.run(debug=True, host=HOST, port=PORT)
    