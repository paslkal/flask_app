from flask import Flask, render_template, request, jsonify
from datetime import datetime

PORT = 5500
HOST = '127.0.0.1'
link_home = f'http://{HOST}:{PORT}/'
link_blog = f'http://{HOST}:{PORT}/blog'
link_todo = f'http://{HOST}:{PORT}/todo'

app = Flask(__name__)


messages = [
        {
            "id": 1,
            "title": 'HI',
            "content": 'Hi',
        },
        {
            "id": 2,
            "title": 'HELLO',
            "content": 'Hello',
        }
    ]

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

    return render_template(
        'blog.html', 
        messages=messages, 
        year=year, 
        link_blog=link_blog, 
        link_todo=link_todo,
        link_home=link_home
    )

tasks = [
    {
        "id":1,
        "content": 'Make dinner',
        "checked": True
    },
    {
        "id":2,
        "content": 'Make HomeWork',
        "checked": False
    },
    {
        "id":3,
        "content": 'Learn Python',
        "cheked": True
    },
]

@app.route('/todo')
def todo():
    
    year = datetime.now().year

    return render_template(
        'todo.html', 
        tasks=tasks,
        link_blog=link_blog, 
        link_todo=link_todo,
        link_home=link_home,
        year=year
    )

@app.post('/api/message')
def add_message():
    last_id = messages[-1]["id"]
    message_id = last_id + 1
    # time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    title = request.form.get('title')
    content = request.form.get('content')

    if (not content) or (not title):
        return f'<h1>Didnt have title or content</h1>Go back to <a href="{link_blog}">Home</a>'

    message = dict(
        id=message_id, 
        title=title, 
        content=content,
    )

    messages.append(message)

    return f'<h1>Message recieved. Go back to <a href="{link_blog}">Home</a></h1>'

@app.delete('/api/message')
def delete_message():
    data = request.get_json()
    message_id = int(data['id'])

    for message in messages:
        if message['id'] == message_id:
            messages.remove(message)

    return jsonify(messages)

@app.post('/api/task')
def add_task():
    last_id = messages[-1]["id"]
    task_id = last_id + 1
    content = request.form.get('content')
    if not content:
        return f'<h1>Didnt have content in task. Go back to <a href="{link_blog}">Home</a></h1>'
    task = dict(id=task_id, content=content, checked=False)


    tasks.append(task)

    return f'<h1>Task recieved. Go back <a href="{link_todo}">TODO App</a></h1>'

app.run(debug=True, host=HOST, port=PORT)