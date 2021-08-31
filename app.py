from flask import Flask, request, render_template, redirect, flash, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "canilive"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def list_pets():
    """Adoption home page"""
    pets = Pet.query.all()
    return render_template("home.html", pets=pets)

@app.route('/add', methods=["GET", "POST"])
def add_pet():
    form = AddPetForm()

    if form.validate_on_submit():
        new_pet = Pet(name = form.name.data, 
                      age = form.age.data,
                      species = form.species.data,
                      notes = form.notes.data,
                      photo_url = form.photo_url.data)
        db.session.add(new_pet)
        db.session.commit()
        flash(f"{new_pet.name} added.")
        return redirect(url_for('list_pets'))

    else:
        return render_template("add_pet_form.html", form=form)

@app.route("/<int:id>", methods=["GET", "POST"])
def edit_pet(id):
    pet = Pet.query.get_or_404(id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect(url_for('list_pets'))

    else:
        return render_template("edit_pet_form.html", form=form, pet=pet)

@app.route("/api/pets/<int:id>", methods=["GET"])
def api_get_pet(id):

    pet = Pet.query.get_or_404(id)
    info = {"name": pet.name, "age": pet.age}

    return jsonify(info)