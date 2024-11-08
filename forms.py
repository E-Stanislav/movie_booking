from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    
    # Параметр для кнопки submit
    submit = SubmitField()

    def __init__(self, submit_text='Update Movie', *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        self.submit.label.text = submit_text
