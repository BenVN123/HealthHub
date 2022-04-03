from flask import Flask, render_template, request, flash, redirect, url_for, session, g 
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


    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')

        if user_id is None:
            g.user = None
        else:
            g.user = get_db().execute(
                'SELECT * FROM user WHERE id = ?', (user_id,)   
            ).fetchone()


    def login_required(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for('login'))

            return view(**kwargs)

        return wrapped_view

    def save_picture(picture):
        fname = secrets.token_hex(20)
        _, f_ext = os.path.splitext(picture.filename)
        picture_fn = fname + f_ext
        picture_path = os.path.join(app.root_path, "static/images", picture_fn)

        i = Image.open(picture)
        i.save(picture_path)

        return picture_path

    @login_required
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

    @login_required
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

    @login_required
    @app.route("/symptoms")
    def symptoms():
        return render_template("symptoms.html")

    @login_required
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

    @login_required
    @app.route("/about")
    def about():
        return render_template("about.html")

    @login_required
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


    
    @app.route('/register', methods=('GET', 'POST'))
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            db = get_db()
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'

            if error is None:
                try:
                    db.execute(
                        "INSERT INTO user (username, password) VALUES (?, ?)",
                        (username, generate_password_hash(password)),
                    )
                    db.commit()
                except db.IntegrityError:
                    error = f"User {username} is already registered."
                else:
                    return redirect(url_for("login"))

            flash(error)

        return render_template('register.html')

    @app.route('/login', methods=('GET', 'POST'))
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            db = get_db()
            error = None
            user = db.execute(
                'SELECT * FROM user WHERE username = ?', (username,)
            ).fetchone()

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index'))

            flash(error)

        return render_template('login.html')


    

    @login_required
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))

        
        
    return app
