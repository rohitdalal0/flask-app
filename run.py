from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, current_user
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from model import *



app = Flask(__name__, static_folder='static', template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://rohit:password@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'SuperSecret'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LftGcEUAAAAAKjlrMb4UQ3OEfSJ4WoW32aRg_Yk'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
bootstrap = Bootstrap(app)
admin = Admin(app)

# init
db.init_app(app)
login_manager.init_app(app)




# login init
@login_manager.user_loader
def user_loader(user_id):
    return Login.query.get(user_id)



# routes
@app.route('/')
def index():
    all_posts = db.session.query(Post).all()
    return render_template('index.html', posts=all_posts)


@app.route('/post')
@login_required
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

@app.route('/add_post', methods=['POST', 'GET'])
@login_required
def add_post():
    if request.method =='POST':
        title = request.form['title']
        body = request.form['body']
        tag = request.fomr['tag']
        new_post = Post(title=title, body=body, tag=tag, url=request.files['file'])
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('post_direction'))
    else:
        return render_template('add_post.html')



# login and signup page
@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_check = Login.query

        if user_check and (login_form.password.data == user_check.password):
            login_user(user_check, remember=login_form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Email and password match not found!')
            return render_template('login.html', login_form=login_form)
    else:
        return render_template('login.html', login_form=login_form)

@app.route('/signup')
def signup():
    return render_template('signup.html', Signup_form=SignupForm('/signup'))



# url shortcut
@app.route('/post/<int:no>')
@login_required
def post_direction(no):
    one_post = db.session.query(Post).filter_by(id=no)
    return render_template('post.html', posts=one_post)




# unauthorized handler
@login_manager.unauthorized_handler
def unauthorized():
    return redirect('login')

# 404 not found
@app.errorhandler(404)
def not_found(n):
    return render_template('404.html')


@app.route('/user')
def user():
    return "Current user: {}".format(current_user)


if __name__ == '__main__':
    app.run(debug=True)
