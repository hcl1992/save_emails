"""
configure user information to connect to database
"""

from flask import Flask
from flask import request
from flask import jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import config

databaseurl = 'mysql://%s:%s@%s:%s/%s' % (config.MYSQL_USER, config.MYSQL_PASS, config.MYSQL_HOST, config.MYSQL_PORT, config.MYSQL_DB)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = databaseurl
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

class email(db.Model):
    __tablename__ = 'email'
    event_id = db.Column(db.Integer, primary_key=True, nullable=False)
    email_subject = db.Column(db.String(50), nullable=False)
    email_content = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime)

    def __init__(self, event_id, email_subject, email_content,timestamp):
        self.event_id = event_id
        self.email_subject = email_subject
        self.email_content = email_content
        self.timestamp = timestamp

    def __repr__(self):
        return '<Id %r User %r>' % (self.event_id, self.email_subject)

db.create_all()

@app.route('/', methods=['POST'])
def hello():
    if not request.json:
        return "failed!", 400
    email = {
        'event_id': request.json['event_id'],
        'email_subject': request.json['email_subject'],
        'email_content': request.json['email_content']
        #'timestamp': request.json['timestamp']
    }
    # initialize email
    em = mytable(int(email['event_id']), email['email_subject'], email['email_content']) #,email['timestamp'])
    #haven't figured out how to address the timestamp issue
    
    # insert new items into database
    db.session.add(em)
    #submit change
    db.session.commit()
    return "Hello World!"

@app.route('/', methods=['GET'])
def get_one():
    if not request.args['event_id']:
        abort(400)
    get_id = request.args['event_id']
    # obtain all data in the table
    ids = mytable.query.all()
    # obtain filter item
    get = mytable.query.filter_by(event_id = get_id).first()
    # obtain member property
    ret = 'event_id=%d,email_subject=%s,timestamp=%s' % (get.event_id, get.email_subject, get.timestamp)
    return ret

app.run(debug = True)
