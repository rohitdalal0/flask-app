from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import input_required, Length, Email
from run import db


date = datetime.datetime.strftime(datetime.datetime.now(), '%B %d, %Y')


class Contacts(db.Model):
    __tablename__ = 'contacts'
    id = db.Column('No', db.Integer, primary_key=True)
    name = db.Column('Name', db.String(15), nullable=True)
    email = db.Column('Email', db.String(20), nullable=True)
    phone = db.Column('Phone', db.String(15), nullable=True)
    message = db.Column('Message', db.String(100))
    date = db.Column('Date', db.VARCHAR(20), default=date)

    def __repr__(self):
        return '<contacts(Name=%s, Email=%s, Phone=%s, Message=%s, Date=%s)>' % (
            self.name, self.email, self.phone, self.message, self.date)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column('No', db.Integer, primary_key=True)
    title = db.Column('Title', db.String(100), nullable=False)
    post = db.Column('Post', db.String(1000), nullable=False)
    tag = db.Column('Tag', db.String(200), nullable=False)
    url = db.Column('Url', db.String(500), nullable=False)
    date = db.Column('Date', db.String(20), nullable=False, default=date)

    def __repr__(self):
        return '<Post(title=%s, post=%s, Url=%s date=%s)>' % (self.title, self.post, self.url, self.date)


class Login(db.Model, UserMixin):
    __tablename__ = 'login'
    id = db.Column('No', db.Integer, primary_key=True)
    username = db.Column('Username', db.String(50), nullable=False)
    email = db.Column('Email', db.String(100), nullable=False)
    password = db.Column('Password', db.String(50), nullable=False)
    date = db.Column('Date', db.String(20), nullable=False, default=date)

    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return True
    @property
    def get_id(self):
        return self.id
    @property
    def __repr__(self):
        return '<Login(name=%s, email=%s, password=%s, date=%s)>' % (self.name, self.email, self.password, self.date)

class Login_form(FlaskForm):
    email = StringField('Email *', validators=[input_required()])
    password = PasswordField('Password *', validators=[input_required(), Length(min=8, max=20)])
    remember = BooleanField('Remember me')

class Signup_form(FlaskForm):
    username = StringField('Username *', validators=[input_required(), Length(min=5, max=15)])
    email = StringField('Email *', validators=[input_required(), Email('Invalid email*')])
    password = PasswordField('Password *', validators=[input_required(), Length(min=8, max=20)])


# admin.add_views(ModelView(Post, db.session))
# admin.add_view(ModelView(Login, db.session))
# admin.add_view(ModelView(Contacts, db.session))

