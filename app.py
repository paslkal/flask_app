from flask import Flask, render_template, request, jsonify
from datetime import datetime
from db import get_messages, add_message, delete_message, get_tasks

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
        return f'<h1>Didnt have title or content</h1>Go back to <a href="{link_blog}">Home</a>'

    message = dict(title=title, content=content)

    add_message(message)        

    return f'<h1>Message recieved. Go back to <a href="{link_blog}">Home</a></h1>'

@app.delete('/api/message')
def delete_message_from_page():
    data = request.get_json()
    message_id = data['id']

    delete_message(message_id)    

    messages = get_messages()

    return jsonify(messages)

@app.post('/api/task')
def add_task():
    last_id = tasks[-1]["id"]
    task_id = last_id + 1
    content = request.form.get('content')
    if not content:
        return f'<h1>Didnt have content in task. Go back to <a href="{link_blog}">Home</a></h1>'
    task = dict(id=task_id, content=content, checked=False)

    tasks.append(task)

    return f'<h1>Task recieved. Go back <a href="{link_todo}">TODO App</a></h1>'

@app.delete('/api/task')
def delete_task():
    data = request.get_json()
    task_id = data['id']

    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
    
    return jsonify(tasks)

if __name__=='__main__':
    app.run(debug=True, host=HOST, port=PORT)
    