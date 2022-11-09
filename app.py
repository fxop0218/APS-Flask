from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from database import db
from forms import PersonForm
from models import Person

app = Flask(__name__)

# DB configuration

USER_DB = "postgres"
PASS_DB = "admin"
URL_DB = "localhost"
NAME_DB = "aps_flask_db"
FULL_URL_DB = f"postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}"

app.config["SQLALCHEMY_DATABASE_URI"] = FULL_URL_DB
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# If separate the classes in other files need this
db.init_app(app)

# Configurate flask-migrate

migrate = Migrate()
migrate.init_app(app, db)

# Configuration of flask-wtf
app.config["SECRET_KEY"] = "SECRET_KEY"  # Change in production service


@app.route("/")
@app.route("/index")
def index():
    # Person list
    people = Person.query.all()
    total_people = Person.query.count()
    app.logger.debug(f"People list: {people}")
    app.logger.debug(f"Total people: {total_people}")
    return render_template("index.html", people=people, total_people=total_people)


@app.route("/show/<int:id>")
def show_info(id):
    person = Person.query.get_or_404(id)  # If fails return error 404
    app.logger.debug(f"People list: {person}")
    return render_template("show_info.html", person=person)


@app.route("/add_person", methods=["GET", "POST"])
def add_person():
    person = Person()
    person_form = PersonForm(obj=person)
    if request.method == "POST":
        if person_form.validate_on_submit():
            person_form.populate_obj(person)
            app.logger.debug(f"Person to insert: {person}")
            # Add to database
            db.session.add(person)
            # Commit
            db.session.commit()
            return redirect(url_for("index"))
    return render_template("add.html", person_form=person_form)
