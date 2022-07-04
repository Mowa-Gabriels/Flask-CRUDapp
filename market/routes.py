
from flask import render_template, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user
from market import app
from market.forms import LoginForm, RegisterForm
from market.models import MarketModel, User
from market import db

@app.route('/')
@login_required
def index():
    item = MarketModel.query.all()


    return render_template('index.html', items=item)



@app.route('/market/<int:id>', methods=['GET'])
def item_detail(id):
    item = MarketModel.query.get_or_404(id)
    return render_template('detail.html',items=item)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
        
            login_user(attempted_user)
            return redirect(url_for('index'))

        else:
            flash(f'Invalid Login details', category='warning')


    return render_template('auth/login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
        email=form.email.data,
        password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()

        # moves registered users to login page
        # return redirect(url_for('login'))

        #to automatically log users in 
        login_user(user_to_create)
        flash(f'Hello {user_to_create.username},your account has been created successfully.', category='success')
        return redirect(url_for('index'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='warning')

    return render_template('auth/register.html', form=form)