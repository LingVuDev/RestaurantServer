from flask import Flask, render_template, request, url_for, redirect
from src.models.RestaurantModels import db, Restaurant, MenuItem
from flask_sqlalchemy import SQLAlchemy

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
with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route('/')
@app.route('/restaurants')
def show_restaurants():
    restaurants = Restaurant.query.all()
    return render_template('restaurants.html', restaurants=restaurants)


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
    return render_template('menu.html', restaurant=restaurant, menu=items)


@app.route('/restaurants/<int:restaurant_id>/menu/new')
def new_menuitem(restaurant_id: int):
    return render_template('newmenuitem.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menuitem_id>/edit')
def edit_menuitem(restaurant_id: int, menuitem_id: int):
    return render_template('editmenuitem.html', restaurant=restaurant, item=item)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menuitem_id>/delete')
def delete_menuitem(restaurant_id: int, menuitem_id: int):
    return render_template('deletemenuitem.html', restaurant=restaurant, item=item)
