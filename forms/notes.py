# imports for News
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, TimeField, EmailField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class NoteForm(FlaskForm):
    note = TextAreaField("Note Title", validators=[DataRequired()])
    # team_leader = IntegerField("Team Leader id")
    note_time = TimeField("Notification time")
    description = TextAreaField("Description")
    email_send = EmailField("Email for notification")
    collaborators = TextAreaField("Collaborators")
    is_finished = BooleanField("Is finished")
    submit = SubmitField('Submit')
