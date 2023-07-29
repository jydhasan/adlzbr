from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import random
import sqlite3

# create an instance of the Flask class
app = Flask(__name__)

# add configurations and database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.secret_key = 'yoursecretkeyhere'


# initialize the database instance
db = SQLAlchemy(app)

# create a model for questions


# create students model
class QuestionList(db.Model):
    __tablename__ = 'QuestionList'
    id = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    minutes = db.Column(db.String(100), nullable=False)
    tablename = db.Column(db.String(100), nullable=False)
    resulttable = db.Column(db.String(100), nullable=False)
    qstart = db.Column(db.String(100), nullable=False)
    qend = db.Column(db.String(100), nullable=False)
    # Add more fields as needed

    def __init__(self, fid, title, minutes, tablename, resulttable, qstart, qend):
        self.fid = fid
        self.title = title
        self.minutes = minutes
        self.tablename = tablename
        self.resulttable = resulttable
        self.qstart = qstart
        self.qend = qend


# Assuming you have imported the required modules and set up the app and db instances.

# Define the model class following the Python naming convention


class CreateCategory(db.Model):
    __tablename__ = 'catagory_table'
    id = db.Column(db.Integer, primary_key=True)
    catagory = db.Column(db.String(100))
    catagoryLavel = db.Column(db.String(200))
    catagorySubject = db.Column(db.String(200))

    # Add a composite unique constraint for catagoryLavel and catagorySubject
    __table_args__ = (
        db.UniqueConstraint('catagoryLavel', 'catagorySubject'),
    )

    def __init__(self, catagory, catagoryLavel, catagorySubject):
        self.catagory = catagory
        self.catagoryLavel = catagoryLavel
        self.catagorySubject = catagorySubject

# Create a route to add a category


@app.route('/create_catagory', methods=['GET', 'POST'])
def create_catagory():
    if request.method == 'POST':
        def to_camel_case(input_string):
            # Split the string into words (removing any leading/trailing spaces)
            words = input_string.strip().split()

            # Remove any non-alphabetic characters from the beginning of the first word
            first_word = words[0]
            first_word = ''.join(filter(str.isalpha, first_word))

            # Capitalize the first letter of the first word
            first_word = first_word.capitalize()

            # Capitalize the first letter of each subsequent word
            camel_case_string = first_word + \
                ''.join(word.capitalize() for word in words[1:])

            return camel_case_string

        # Get the data from the form
        catagory_lavel = request.form['catagoryLavel']
        catagory_subject = request.form['catagorySubject']
        catagory = request.form['catagory_name']

        # Convert the catagoryLavel and catagorySubject to camel case
        catagory = to_camel_case(catagory)
        catagory_lavel = to_camel_case(catagory_lavel)
        catagory_subject = to_camel_case(catagory_subject)

        # Check if the combination of catagoryLavel and catagorySubject already exists
        check_subject = CreateCategory.query.filter_by(
            catagoryLavel=catagory_lavel, catagorySubject=catagory_subject).first()

        if check_subject:
            flash('This subject already exists within this category level.')
            return redirect(url_for('create_catagory'))
        else:
            catagory = CreateCategory(
                catagory=catagory,
                catagoryLavel=catagory_lavel,
                catagorySubject=catagory_subject
            )
            db.session.add(catagory)
            db.session.commit()
            flash('Record was successfully added')
    return render_template('create_catagory.html')


# Create a new route to show the data by alphabetical order
@app.route('/show_catagory', methods=['GET'])
def show_categories():
    categories = CreateCategory.query.order_by(
        CreateCategory.catagory, CreateCategory.catagoryLavel).all()
    return render_template('show_catagory.html', categories=categories)


# # show catagorySubject by catagoryLavel
@app.route('/show_catagory/<catagoryLavel>', methods=['GET'])
def show_catagory(catagoryLavel):
    categories = CreateCategory.query.filter(
        (CreateCategory.catagoryLavel == catagoryLavel) | (
            CreateCategory.catagory == catagoryLavel)
    ).order_by(CreateCategory.catagorySubject).all()

    return render_template('show_catagory_level.html', categories=categories)


# show catagorySubject by catagoryLavel
@app.route('/<id>')
def get_subject(id):
    subject = CreateCategory.query.filter_by(id=id).first()
    showQuestions = QuestionList.query.filter_by(fid=id).all()
    return render_template('subject.html', subject=subject, showQuestions=showQuestions)


# create a dynameic table
def create_dynamic_table(entry_id):
    table_name = f"new_table_{entry_id}"

    class DynamicTable(db.Model):
        __tablename__ = table_name
        id = db.Column(db.Integer, primary_key=True)
    return DynamicTable


def create_result_table(entry_id):
    result_table = f"result_table_{entry_id}"

    class DynamicTableResult(db.Model):
        __tablename__ = result_table
        id = db.Column(db.Integer, primary_key=True)
        sname = db.Column(db.String(100))
        sscore = db.Column(db.Integer)
    return DynamicTableResult


# create excel quiz for catagorysubject


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # save excel data to database
    if request.method == 'POST':
        id = request.form['id']

        # another data for questionlist
        fid = request.form['id']
        title = request.form['title']
        minutes = request.form['minutes']

        entry_id = random.randrange(1, 9999999)
        DynamicTable = create_dynamic_table(entry_id)
        DynamicTableResult = create_result_table(entry_id)
        DynamicTableResult.__table__.create(db.engine)
        # Create the table in the database
        DynamicTable.__table__.create(db.engine)
        file = request.files['inputFile']
        # file.save(file.filename)
        df = pd.read_excel(file.filename)
        df.to_sql(DynamicTable.__tablename__, con=db.engine,
                  if_exists='replace', index=False)  # Fix here

        student = QuestionList(fid=fid, title=title,
                               minutes=minutes, tablename=DynamicTable.__tablename__, resulttable=DynamicTableResult.__tablename__, qstart='1', qend='2')
        db.session.add(student)
        db.session.commit()

        flash('Record was successfully added')
        return redirect(url_for('get_subject', id=id))
    else:
        return redirect(url_for('get_subject'))


# fetch data from questionlist table
@app.route('/get_data/<string:entry_id>', methods=['GET'])
def get_data(entry_id):
    # use sqlite to get data from database
    conn = sqlite3.connect('instance/db.sqlite')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {entry_id}")
    data = cursor.fetchall()
    # return data
    return render_template('show_quiz.html', data=data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
