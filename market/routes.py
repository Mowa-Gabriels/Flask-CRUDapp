
from urllib import request
from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, login_required, logout_user
from market import app
from market.forms import LoginForm, PurchaseForm, RegisterForm, SellForm
from market.models import MarketModel, User
from market import db

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    selling_form = SellForm()
    purchase_form = PurchaseForm()
    if request.method=="POST":

        #PurchaseLogic
        purchase_item = request.form.get('purchased_item')
        p_item_object = MarketModel.query.filter_by(name=purchase_item).first()

        #line20 -36 basically defines if a user can make a purchase based on budget
        #but then this operation has been sorted on the template using conditional statements but here is another way to execute it 
        #by creating a CAN_PURCHASE method in the models

        if p_item_object:
            if current_user.can_purchase(p_item_object): 
               
                # p_item_object.owner = current_user.id
                # current_user.budget -= p_item_object.price
                # db.session.commit()
                # the above live of codes was commented out to create a method in the models
                p_item_object.buy(current_user)
                flash(f'Congratulations, you purchased {p_item_object.name} for the price of ${p_item_object.price}.', category='primary')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name} for the price of ${p_item_object.price}.", category='warning')

        #SellingLogic
        sold_item = request.form.get('sold_item')
        s_item_object = MarketModel.query.filter_by(name=sold_item).first()
        
        #line20 -36 basically defines if a user can make a sell based on the item availability in the database
        #but then this operation has been sorted on the template using conditional statements but here is another way to execute it 
        #by creating a CAN_SELL method in the models

        if s_item_object:
            if current_user.can_sell(s_item_object): 
            
                # s_item_object.owner = current_user.id
                # current_user.budget += s_item_object.price
                # db.session.commit()
                # the above live of codes was commented out to create a method in the models
                s_item_object.sell(current_user)
                flash(f'Congratulations, you sold {s_item_object.name} back to market!')
            else:
                flash(f"Something went wrong while trying to sell {s_item_object.name}.")
        return redirect (url_for('index'))
    
    
    if request.method=='GET':
        item = MarketModel.query.filter_by(owner=None)
        owned_items = MarketModel.query.filter_by(owner=current_user.id)
        return render_template('index.html', items=item, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)



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

        # redirects registerd users to login page
        # return redirect(url_for('login'))

        #to automatically log users in 
        login_user(user_to_create)
        flash(f'Hello {user_to_create.username},your account has been created successfully.', category='success')
        return redirect(url_for('index'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='warning')

    return render_template('auth/register.html', form=form)