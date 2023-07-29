from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# create an instance of the Flask class
app = Flask(__name__)

# add configurations and database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.secret_key = 'yoursecretkeyhere'


# initialize the database instance
db = SQLAlchemy(app)

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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
