from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

import uuid


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# initialization
#app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://zhongche:swjt111@10.180.162.1/zhongche'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# extensions
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'
    #id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String(32), index=True)
    #password_hash = db.Column(db.String(64))
    id = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(64))
    author = db.Column(db.String(64))
    read = db.Column(db.Boolean, default=False)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)



BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

books = [Book(id=uuid.uuid4().hex, title = 'On the Road', author = 'Jack Kerouac', read=True),
        Book(id=uuid.uuid4().hex, title = 'Harry Potter and the Philosopher\'s Stone', author = 'J. K. Rowling', read=False),
        Book(id=uuid.uuid4().hex, title = 'Green Eggs and Ham', author = 'Dr. Seuss', read=True)
        ]

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        book = Book(
            id = uuid.uuid4().hex,
            title = post_data.get('title'),
            author = post_data.get('author'),
            read = True if (post_data.get('read') in ['true', 'True']) else False
        )
        db.session.add(book)
        db.session.commit()
        response_object['message'] = 'Book added!'
    else:
        data = Book.query.all()
        result = [d.__dict__ for d in data]
        new_result = [{key:val for key, val in r.items() if key != '_sa_instance_state'} for r in result]

        response_object['books'] = new_result
    return jsonify(response_object)

@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)

if __name__ == '__main__':
    # create tables
    db.create_all()

    # add the 3 testing items to the books table if they are not added yet
    if (len(Book.query.all()) == 0):
        db.session.add_all(books)
        db.session.commit()
    
    app.run(use_reloader=False)