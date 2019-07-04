from flask import Flask, render_template, request, url_for, redirect, session, make_response
from src.models.RestaurantModels import db, Restaurant, MenuItem
from flask_sqlalchemy import SQLAlchemy
from src.login.login_constants import get_google_credentials
from src.login.login_helper import get_user_info_from_google_id_token
import random
import string
import json

# Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

# Fake Menu Items
items = [{'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree', 'id': '1'}, {'name': 'Chocolate Cake', 'description': 'made with Dutch Chocolate', 'price': '$3.99', 'course': 'Dessert', 'id': '2'}, {'name': 'Caesar Salad', 'description': 'with fresh organic vegetables',
                                                                                                                                                                                                                                                        'price': '$5.99', 'course': 'Entree', 'id': '3'}, {'name': 'Iced Tea', 'description': 'with lemon', 'price': '$.99', 'course': 'Beverage', 'id': '4'}, {'name': 'Spinach Dip', 'description': 'creamy dip with fresh spinach', 'price': '$1.99', 'course': 'Appetizer', 'id': '5'}]
item = {'name': 'Cheese Pizza', 'description': 'made with fresh cheese',
        'price': '$5.99', 'course': 'Entree'}


app = Flask("main", template_folder="src/templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits)
                         for x in range(32)).encode()
with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route('/')
@app.route('/restaurants')
def show_restaurants():
    restaurants = Restaurant.query.all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    session['state'] = state

    return render_template('login.html', google_credentials=get_google_credentials(), STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():

    # Validate state token
    try:
        if request.args.get('state') != session['state']:
            response = make_response(json.dumps(
                'Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
    except KeyError as e:
        response = make_response(json.dumps(
            'Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    token = request.form['data']
    client_id = request.form['client_id']

    # Get user info
    user_info = get_user_info_from_google_id_token(token, client_id)

    # Check validity
    if user_info['aud'] != get_google_credentials()['client_id']:
        response = make_response(json.dumps(
            "Token's user ID doesn't match given user", 401))
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if the user is already logged in
    stored_token = session.get('access_token')
    stored_client_id = session.get('client_id')

    # Check if already logged by comparing the session values with the request values
    if(stored_token is not None and stored_client_id == client_id):
        response = make_response(json.dumps(
            "User is already connected"), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session['access_token'] = token
    session['client_id'] = client_id

    return redirect("/")


@app.route('/restaurants/new', methods=['GET', 'POST'])
def new_restaurants():
    if request.method == 'POST':
        post = request.form
        Restaurant.create_restaurant(post['name'])
        return redirect("/")
    return render_template('newrestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def edit_restaurants(restaurant_id: int):
    if request.method == 'POST':
        post = request.form
        Restaurant.update_restaurant_name(restaurant_id, post['name'])
        return redirect("/")
    restaurant = Restaurant.get_restaurant_by_id(restaurant_id)
    return render_template('editrestaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/delete')
def delete_restaurants(restaurant_id: int):
    restaurant = Restaurant.get_restaurant_by_id(restaurant_id)
    return render_template('deleterestaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/deletation_confirmed')
def delete_restaurant_confirmed(restaurant_id: int):
    Restaurant.delete_restaurant(restaurant_id)
    return redirect("/")


@app.route('/restaurants/<int:restaurant_id>')
@app.route('/restaurants/<int:restaurant_id>/menu')
def show_menu(restaurant_id: int):
    restaurant = Restaurant.get_restaurant_by_id(restaurant_id)
    items = MenuItem.get_menu_by_restaurant_id(restaurant_id)
    return render_template('menu.html', restaurant=restaurant, menu=items)


@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def new_menuitem(restaurant_id: int):
    if request.method == 'POST':
        post = request.form
        MenuItem.create_new_menu_item(
            restaurant_id, post['name'], post['description'], post['price'], post['course'])
        return redirect("/restaurants/" + str(restaurant_id) + "/menu")
    restaurant = Restaurant.get_restaurant_by_id(restaurant_id)
    return render_template('newmenuitem.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menuitem_id>/edit', methods=['GET', 'POST'])
def edit_menuitem(restaurant_id: int, menuitem_id: int):
    if request.method == 'POST':
        post = request.form
        MenuItem.update_menu_item(
            menuitem_id, post['name'], post['description'], post['price'], post['course'])
        return redirect("/restaurants/" + str(restaurant_id) + "/menu")
    item = MenuItem.get_menu_item_by_id(menuitem_id)
    return render_template('editmenuitem.html', restaurant=restaurant, item=item)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menuitem_id>/delete')
def delete_menuitem(restaurant_id: int, menuitem_id: int):
    MenuItem.delete_menu_item(menuitem_id)
    return redirect("/restaurants/" + str(restaurant_id) + "/menu")
