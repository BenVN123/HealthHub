from flask import Flask, render_template, request, flash, redirect, url_for
import os
import secrets
from PIL import Image
from HealthHub.deeplearning.classification import predict


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="uPqECIPsjfu7qQ93MwHiyDr73QyhyjUphSnehNAt",
        DATABASE=os.path.join(app.instance_path, "HealthHub.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    db.init_app(app)

    from HealthHub.db import get_db

    def save_picture(picture):
        fname = secrets.token_hex(20)
        _, f_ext = os.path.splitext(picture.filename)
        picture_fn = fname + f_ext
        picture_path = os.path.join(app.root_path, "static/images", picture_fn)

        i = Image.open(picture)
        i.save(picture_path)

        return picture_path

    @app.route("/", methods=("GET", "POST"))
    def index():
        if request.method == "POST":
            img = request.files["uploaded_img"]
            img = save_picture(img)
            pred = predict(app, img)
            os.remove(img)
            if pred == 0:
                lol = "You don't have a tumor!"
            else:
                lol = "You have a tumor!"
            return render_template("index.html", output=lol)
        return render_template("index.html")

    @app.route("/questions", methods=("GET", "POST"))
    def questions():
        db = get_db()
        questions = db.execute("SELECT * FROM question").fetchall()
        if request.method == "POST":
            q = request.form["q"]
            error = None

            if len(q) > 255:
                error = "Question should not exceed 255 characters."

            if error is None:
                db.execute("INSERT INTO question (body) VALUES (?)", (q,))
                db.commit()

                return redirect(url_for("questions"))

            flash(error)

        return render_template("questions.html", questions=questions)

    @app.route("/symptoms")
    def symptoms():
        return render_template("symptoms.html")

    @app.route("/doctors", methods=("GET", "POST"))
    def doctors():
        if request.method == "POST":
            zipcode = request.form["zipcode"]

            if len(zipcode) < 5:
                error = "Please enter a valid American zip code."
                flash(error)
            else:
                return redirect(
                    f"https://www.vitals.com/search?query=Brain%20Tumor&city_state={zipcode}"
                )

        return render_template("doctors.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/<int:id>", methods=("GET", "POST"))
    def answer(id):
        db = get_db()
        answers = db.execute(
            "SELECT * FROM answer WHERE question_id = ?", (id,)
        ).fetchall()
        if request.method == "POST":
            a = request.form["body"]
            error = None

            if len(a) > 255:
                error = "Max length: 255"

            if error is None:
                db.execute(
                    "INSERT INTO answer (question_id, body) VALUES (?,?)", (id, a)
                )
                db.commit()
                return redirect(url_for("answer", id=id))

            flash(error)

        return render_template("answer.html", id=id, answers=answers)

    return app
