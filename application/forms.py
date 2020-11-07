from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User


class RegistrationForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите пароль',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегестрироваться')

    recaptcha = RecaptchaField()

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Пользователь с данной почтой уже зарегистрирован. Выберите другую, пожалуйста.')


class LoginForm(FlaskForm):
    email = StringField('Почта',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    recaptcha = RecaptchaField()
    submit = SubmitField('Войти')