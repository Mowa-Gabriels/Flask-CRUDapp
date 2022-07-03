from flask import render_template, url_for, redirect
from market import app
from market.forms import RegisterForm
from market.models import MarketModel, User
from market import db

@app.route('/')
def index():
    item = MarketModel.query.all()
    return render_template('index.html', items=item)

@app.route('/market')
def market():
    return render_template('marketplace.html', context='Hello, World!')

@app.route('/market/<int:id>', methods=['GET'])
def item_detail(id):
    item = MarketModel.query.get_or_404(id)
    return render_template('detail.html',items=item)

@app.route('/login')
def login():
    return render_template('auth/login.html', context='Hello, World!')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
        email=form.email.data,
        password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('index'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')

    return render_template('auth/register.html', form=form)