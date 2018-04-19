
"""
    Flask-WTF forms.
""" 

from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp


class CategoryForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(max=250),
                       Regexp(regex='^[\w\s]*$',
                       message='Alphanumeric or space characters only.')])


class ItemForm(Form):
    name = StringField('Name', validators=[DataRequired(), Length(max=250),
                       Regexp(regex='^[\w\s]*$',
                       message='Alphanumeric or space characters only.')])
    description = TextAreaField('Description', validators=[Length(max=1000)])
    image = FileField('Image',
                      validators=[
                          FileAllowed(['jpeg', 'jpg', 'png', 'gif', 'bmp'],
                                      'File must be an image.')])
    category_id = SelectField('Category', choices=None, coerce=int)
