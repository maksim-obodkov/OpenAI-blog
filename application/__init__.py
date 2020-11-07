from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfW4t8ZAAAAAJWYMK0HOdRGoUO3A7Yo7MrfxbBi'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfW4t8ZAAAAACKBJ11xMZd_oRhq5izc8T-j7QGI'

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = 'success'

from application import routes
