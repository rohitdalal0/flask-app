from flask import Flask, render_template, url_for, redirect, flash, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user
from flask_bootstrap import Bootstrap
from model import *



app = Flask(__name__, static_folder='static', template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://localhost:password@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'SecretKey'

db = SQLAlchemy(app)
login_manager = LoginManager()
bootstrap = Bootstrap(app)



# login init
db.init_app(app)
login_manager.init_app(app)





@login_manager.user_loader
def user_loader(user_id):
    return Login.query.get(user_id)



# routes
@app.route('/')
def index():
    all_posts = db.session.query(Post).all()
    return render_template('index.html', posts=all_posts)


@app.route('/post')
def post():
    all_posts = db.session.query(Post).all()
    return render_template('post.html', posts=all_posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

@app.route('/add_post')
def add_post():
    return render_template('add_post.html')


# url shortcut
@app.route('/<string:no>/post')
def post_direction(no):
    one_post = db.session.query(Post).filter_by(id=no)
    return render_template('post.html', posts=one_post)

# login and signup page
@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = Login_form()
    user_check = db.session.query(Login).filter_by(email=login_form.email.data).first()

    if login_form.validate_on_submit():
        if user_check and (login_form.password.data == user_check.password):
            login_user(user_check, remember=login_form.remember.data)
            return redirect(request.args.get('next'), url_for('/index'))
        else:
            flash('Email and password match not found!')
            return render_template('login.html')
    else:
        return render_template('login.html', login_form=login_form)

@app.route('/signup')
def signup():
    return render_template('signup.html', Signup_form=Signup_form('/signup'))


# unauthorized handler
@login_manager.unauthorized_handler
def unauthorized():
    return redirect('login')



if __name__ == '__main__':
    app.run(debug=True)
