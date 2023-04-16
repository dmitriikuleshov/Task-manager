import os.path

from flask import Flask, render_template, redirect, request, abort

from flask_login import LoginManager, login_user, current_user
from flask_login import logout_user, login_required

from data import db_session
from data.users import User
from data.notes import Notes

from forms.user import RegisterForm
from forms.login import LoginForm
from forms.notes import NoteForm
import datetime

from dotenv import load_dotenv
from mail_sender import send_mail

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def add_user(surname=None,
             name=None,
             email=None):
    new_user = User()
    new_user.surname = surname
    new_user.name = name
    # # new_user.position = position
    # # new_user.speciality = speciality
    # # new_user.address = address
    # new_user.email = email
    # if position == "captain":
    #     new_user.set_password("123")

    db_sess = db_session.create_session()
    db_sess.add(new_user)
    db_sess.commit()


def add_note(note=None,
             note_time=None,
             description=None,
             collaborators=None):
    new_note = Notes()
    new_note.note = note
    new_note.note_time = note_time
    new_note.description = description
    new_note.collaborators = collaborators
    new_note.start_date = str(datetime.datetime.now().date())
    new_note.is_finished = False

    db_sess = db_session.create_session()
    db_sess.add(new_note)
    db_sess.commit()


def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()

    add_user(surname="Scott",
             name="Ridley",
             email="scott_chief@mars.org")

    add_user(surname="Smith",
             name="John",
             email="john_smith@mars.org")

    add_user(surname="Johnson",
             name="Mary",
             email="mary_johnson@mars.org")

    add_user(surname="Lopez",
             name="Sofia",
             email="sofia_lopez@mars.org")

    add_user(surname="Wu",
             name="Li",
             email="li_wu@mars.org")

    add_note(note="deployment of residential modules 1 and 2",
             note_time=15,
             description="AAAAAAAAAAAA",
             email_send="2, 3")

    add_note(note="Exploration of mineral resources",
             note_time=15,
             description="AAAAAAAAAAAA",
             email_send="1, 2")

    add_note(note="Development of a management system",
             note_time=15,
             description="AAAAAAAAAAAA",
             email_send="1, 2")
    app.run()


@app.route('/addnote', methods=['GET', 'POST'])
@login_required
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        note = Notes()

        note.note = form.note.data
        note.note_time = form.note_time.data
        note.description = form.description.data
        note.email_send = form.email_send.data
        note.is_finished = form.is_finished.data
        current_user.notes.append(note)
        db_sess.merge(current_user)
        db_sess.commit()

        # email sending
        try:
            email_send = request.values.get("email_send")
            note = request.values.get("note")
            description = request.values.get("description")
            if send_mail(email_send, note,
                         description, []):
                # ["1.jpg", "2.docx", "3.txt"]):
                # return f"Letter sent successfully. Address: {email_send}"
                return redirect('/')
        except:
            return redirect('/')
    return render_template('note.html', title='Note add',
                           form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/notes/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_notes(id):
    form = NoteForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        if current_user.id == 1:
            note = db_sess.query(Notes).filter(Notes.id == id).first()
        else:
            note = db_sess.query(Notes).filter(Notes.id == id,
                                               Notes.user == current_user
                                               ).first()
        if note:
            form.note.data = note.note
            form.note_time.data = note.note_time
            form.email_send.data = note.email_send
            form.is_finished.data = note.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if current_user.id == 1:
            note = db_sess.query(Notes).filter(Notes.id == id).first()
        else:
            note = db_sess.query(Notes).filter(Notes.id == id,
                                               Notes.user == current_user
                                               ).first()
        if note:
            note.note = form.note.data
            note.note_time = form.note_time.data
            note.email_send = form.email_send.data
            note.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('note.html',
                           title='Note edit',
                           form=form
                           )


@app.route('/notes_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def notes_delete(id):
    db_sess = db_session.create_session()

    if current_user.id == 1:
        note = db_sess.query(Notes).filter(Notes.id == id).first()
    else:
        note = db_sess.query(Notes).filter(Notes.id == id,
                                           Notes.user == current_user).first()
    if note:
        db_sess.delete(note)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route("/")
def index():
    db_sess = db_session.create_session()
    notes = db_sess.query(Notes).all()
    return render_template("index1.html", title="Task Manager", notes=notes)
    # return render_template("index.html", notes=notes)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data)

        user.set_password(form.password.data)
        db_sess.add(user)
        print(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Registration', form=form)


if __name__ == '__main__':
    if os.path.exists("db/blogs.db"):
        db_session.global_init("db/blogs.db")
        db_sess = db_session.create_session()
        app.run()
    else:
        main()
