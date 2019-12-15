from flask import Flask, render_template, url_for, redirect, flash, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os



app = Flask(__name__, static_folder='static', template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://rohit:password@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'ITSHOULDBESECRETKEY'
app.config['UPLOAD_FOLDER'] = 'static/img/'

ALLOW_EXTENSIONS = {'jpg','png','txt','jpeg','gif','pdf'}

db = SQLAlchemy(app)
login_manager = LoginManager()
bootstrap = Bootstrap(app)


from model import *

# login init
db.init_app(app)
login_manager.init_app(app)





@login_manager.user_loader
def user_loader(user_id):
    return Login.query.get(user_id)



# routes
@app.route('/')
def index():
    one = db.session.query(Post).all()[:1]
    two = db.session.query(Post).all()[1:2]
    three = db.session.query(Post).all()[2:3]
    four = db.session.query(Post).all()[3:4]
    five = db.session.query(Post).all()[4:5]
    return render_template('index.html', one=one, two=two, three=three, four=four, five=five)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

@app.route('/public/post', methods=['GET','POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        tag = request.form['tag']
        file = request.files['file']

        if title != '' and body != '' and tag != '':
            if file.filename !="":
                    # checking file extension
                    def check_file(file):
                        return '.' in file and file.rsplit('.', 1)[1].lower() in ALLOW_EXTENSIONS

                    if check_file(file.filename):
                        file_name = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                        file.save(file_name)

                        post = Post(title=title, body=body, tag=tag, url='img/'+file.filename)
                        db.session.add(post)
                        db.session.commit()
                        flash('Successfully posted!')
                        return render_template('index.html')

                    else:
                        flash('File isn\'t secure')
                        return redirect(url_for('new_post'))
            else:
                flash('No file selected!')
                return redirect(url_for('new_post'))
        else:
            flash('Please, fill all the input!')
            return redirect(url_for('new_post'))
    else:
        return render_template('add_post.html')


# url shortcut
@app.route('/post/<int:no>')
def post_direction(no):
    one_post = db.session.query(Post).filter_by(id=no).first()
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
            return render_template('login.html', login_form=login_form)
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
