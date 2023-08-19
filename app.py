from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, URL, NumberRange
from sqlalchemy.exc import SQLAlchemyError
from forms import EditPetForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'  # SQLite database file
db = SQLAlchemy(app)
toolbar = DebugToolbarExtension(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    photo_url = db.Column(db.String(200))
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Pet(id={self.id}, name={self.name}, species={self.species})"

class AddPetForm(FlaskForm):
    name = StringField('Pet name', validators=[InputRequired()])
    species = SelectField('Species', choices=[('cat', 'Cat'), ('dog', 'Dog'), ('porcupine', 'Porcupine')],
                          validators=[InputRequired()])
    photo_url = StringField('Photo URL', validators=[URL()])
    age = IntegerField('Age', validators=[NumberRange(min=0, max=30)])
    notes = TextAreaField('Notes')

class EditPetForm(FlaskForm):
    # Create fields for editing pet information
    name = StringField('Pet name', validators=[InputRequired()])
    species = SelectField('Species', choices=[('cat', 'Cat'), ('dog', 'Dog'), ('porcupine', 'Porcupine')],
                          validators=[InputRequired()])
    photo_url = StringField('Photo URL', validators=[URL()])
    age = IntegerField('Age', validators=[NumberRange(min=0, max=30)])
    notes = TextAreaField('Notes')

@app.route('/')
def homepage():
    pets = Pet.query.all()
    return render_template('index.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    form = AddPetForm()

    if form.validate_on_submit():
        try:
            pet = Pet(name=form.name.data, species=form.species.data,
                      photo_url=form.photo_url.data, age=form.age.data,
                      notes=form.notes.data)
            db.session.add(pet)
            db.session.commit()
            return redirect('/')
        except SQLAlchemyError as e:
            db.session.rollback()

    return render_template('add_pet.html', form=form)

@app.route('/<int:pet_id>/edit', methods=['GET', 'POST'])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        try:
            form.populate_obj(pet)
            db.session.commit()
            flash(f"{pet.name} updated.")
            return redirect(url_for('homepage'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("An error occurred while updating the pet. Please try again.", "error")

    return render_template('display_edit_pet.html', pet=pet, form=form)

@app.route('/<int:pet_id>/delete', methods=['GET', 'POST'])
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)

    if request.method == 'POST':
        try:
            db.session.delete(pet)
            db.session.commit()
            return redirect(url_for('homepage'))
        except SQLAlchemyError as e:
            db.session.rollback()
            # Log the error for debugging
            app.logger.error("Error deleting pet: %s", str(e))

    return render_template('delete_pet.html', pet=pet)


@app.route('/api/pets/<int:pet_id>', methods=['GET'])
def api_get_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age}

    return jsonify(info)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)