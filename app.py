from flask import Flask, render_template, request, jsonify, url_for, send_file
from datetime import datetime
from db import get_messages, add_message, delete_message
from db import get_tasks, add_task, delete_task, change_checked_value
from rmbg import remove_background
from env import flask_port, flask_host

PORT = flask_port
HOST = flask_host
link_home = f'http://{HOST}:{PORT}/'
link_blog = f'http://{HOST}:{PORT}/blog'
link_todo = f'http://{HOST}:{PORT}/todo'

app = Flask(__name__)

def get_year():
    year = datetime.now().year
    return year

@app.route('/')
def home():    
    return render_template(
        'home.html', 
        year=get_year(),
        title='Home Page'
    )

@app.route('/blog')
def blog():    
    messages = get_messages()

    return render_template(
        'blog.html', 
        messages=messages, 
        year=get_year(), 
        title='Pascal Blog'
    )

@app.route('/todo')
def todo():    
    tasks = get_tasks()

    return render_template(
        'todo.html', 
        tasks=tasks,
        year=get_year(),
        title='Pascal TODO App'
    )

@app.post('/api/message')
def add_message_from_form():
    title = request.form.get('title')
    content = request.form.get('content')

    if (not(title and content)):
        return f'<h1>Didnt have title or content. Go back to <a href="{url_for('blog')}">Blog Page</a></h1>'

    message = dict(title=title, content=content)

    add_message(message)        

    return f'<h1>Message recieved. Go back to <a href="{url_for('blog')}">Blog Page</a></h1>', 201

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
        return f'<h1>Didnt have content in task. Go back to <a href="{url_for('todo')}">TODO App</a></h1>'

    task = dict(title=title, content=content, checked=checked)

    add_task(task)

    return f'<h1>Task recieved. Go back to <a href="{url_for('todo')}">TODO App</a></h1>', 201


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

@app.route('/rmbg', methods=['GET', 'POST'])
def rmbg():
    if request.method == 'POST':
        files = request.files
        if 'file' not in files:
            response = f'<h1>No file uploaded. <a href="{url_for('rmbg')}">Go back</a></h1>' 
            return response, 400
        
        file = files['file']

        if file.filename == '':
            response = f'<h1>No file selected. <a href="{url_for('rmbg')}">Go back</a></h1>'
            return response, 400
        
        if file.content_type != 'image/png':
            response = f'<h1>This file is not an image. <a href="{url_for('rmbg')}">Go back</a></h1>'
            return response, 400
        
        img_io = remove_background(file)

        return send_file(img_io, 
                         mimetype=file.mimetype, 
                         as_attachment=True, 
                         download_name='_rmbg.png')

    return render_template(
        'rmbg.html', 
        title='Remove Background App',
        year=get_year()
    )

if __name__=='__main__':
    app.run(debug=True, host=HOST, port=PORT)
    