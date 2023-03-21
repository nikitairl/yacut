from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        "Длинная ссылка",
        validators=[DataRequired(message="Поле не может быть пустым")],
    )
    custom_id = StringField("Короткая ссылка", validators=[Length(max=5), Optional()])
    submit = SubmitField("Создать")
