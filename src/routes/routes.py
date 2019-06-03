from flask import Flask, render_template


# Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {
    'name': 'Blue Burgers', 'id': '2'}, {'name': 'Taco Hut', 'id': '3'}]


# Fake Menu Items
items = [{'name': 'Cheese Pizza', 'description': 'made with fresh cheese', 'price': '$5.99', 'course': 'Entree', 'id': '1'}, {'name': 'Chocolate Cake', 'description': 'made with Dutch Chocolate', 'price': '$3.99', 'course': 'Dessert', 'id': '2'}, {'name': 'Caesar Salad', 'description': 'with fresh organic vegetables',
                                                                                                                                                                                                                                                        'price': '$5.99', 'course': 'Entree', 'id': '3'}, {'name': 'Iced Tea', 'description': 'with lemon', 'price': '$.99', 'course': 'Beverage', 'id': '4'}, {'name': 'Spinach Dip', 'description': 'creamy dip with fresh spinach', 'price': '$1.99', 'course': 'Appetizer', 'id': '5'}]
item = {'name': 'Cheese Pizza', 'description': 'made with fresh cheese',
        'price': '$5.99', 'course': 'Entree'}


app = Flask("main", template_folder="src/templates")


@app.route('/')
@app.route('/restaurants')
def show_restaurants():
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurants/new')
def new_restaurants():
    return render_template('newrestaurant.html')


@app.route('/restaurants/<int:restaurant_id>')
def edit_restaurants(restaurant_id: int):
    return render_template('editrestaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/delete')
def delete_restaurants(restaurant_id: int):
    return render_template('deleterestaurant.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/menu')
def show_menu(restaurant_id: int):
    return render_template('menu.html', restaurant=restaurant, menu=items)


@app.route('/restaurants/<int:restaurant_id>/menu/new')
def new_menuitem(restaurant_id: int):
    return render_template('newmenuitem.html')


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menuitem_id>')
def edit_menuitem(restaurant_id: int, menuitem_id: int):
    return render_template('editmenuitem.html', item=item)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menuitem_id>/delete')
def delete_menuitem(restaurant_id: int, menuitem_id: int):
    return render_template('deletemenuitem.html', item=item)
