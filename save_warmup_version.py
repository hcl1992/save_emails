""" 
create a virtualenv email 
downgrade python to 2.7.9 to avoid incompatable issue with anaconda and virtualenv:conda install python=2.7.9
this file is a modification from the tutorial by Miguel as a warmup for the exercise, it does not connect to database
but instore in memory instead

after running this file, open another console to do modification such as get, put, delete, update

GET:
curl -i http://localhost:5000/jublia_test/v1.0/save_emails
POST:
curl -i -H "Content-Type: application/json" -X POST -d '{"email_subject":"Read a book"}' http://localhost:5000/jublia_test/v1.0/save_emails
UPDATE:
curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/jublia_test/v1.0/save_emails/2

after adding authentication: only username == ‘Chunlin’ and password== ‘python’ can visit  
curl -u Chunlin:python -i http://localhost:5000/jublia_test/v1.0/save_emails

"""
#!email/bin/python
from flask import Flask,jsonify

app = Flask(__name__)

save_emails = [
    {
        'event_id': 1,
        'email_subject': u'conference 1',
        'email_content': u'see you in the meeting',
        'done': False
    },
    {
        'event_id': 2,
        'email_subject': u'Learn Python',
        'email_content': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/')
def welcome():
    return "Welcome to email management system!"

from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'Chunlin':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.route('/jublia_test/v1.0/save_emails',methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'save_emails': save_emails})

from flask import abort

@app.route('/jublia_test/v1.0/save_emails/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['event_id'] == task_id, save_emails)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

from flask import make_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

from flask import request

@app.route('/jublia_test/v1.0/save_emails', methods=['POST'])
def create_task():
    if not request.json or not 'email_subject' in request.json:
        abort(400)
    task = {
        'event_id': save_emails[-1]['event_id'] + 1,
        'email_subject': request.json['email_subject'],
        'email_content': request.json.get('email_content', ""),
        'done': False
    }
    save_emails.append(task)
    return jsonify({'task': task}), 201

@app.route('/jublia_test/v1.0/save_emails/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = filter(lambda t: t['event_id'] == task_id, save_emails)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'email_subject' in request.json and type(request.json['email_subject']) != unicode:
        abort(400)
    if 'email_content' in request.json and type(request.json['email_content']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['email_subject'] = request.json.get('email_subject', task[0]['email_subject'])
    task[0]['email_content'] = request.json.get('email_content', task[0]['email_content'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/jublia_test/v1.0/save_emails/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = filter(lambda t: t['event_id'] == task_id, save_emails)
    if len(task) == 0:
        abort(404)
    save_emails.remove(task[0])
    return jsonify({'result': True})

from flask import url_for

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'event_id':
            new_task['uri'] = url_for('get_task', task_id=task['event_id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


if __name__ == '__main__':
    app.run(debug=True)
