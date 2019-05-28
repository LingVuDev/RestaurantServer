from flask import Flask, render_template

app = Flask("main", template_folder="src/templates")


@app.route('/')
@app.route('/restaurants')
def show_restaurants():
    return render_template('restaurants.html')


@app.route('/restaurants/new')
def new_restaurants():
    return render_template('newrestaurant.html')


@app.route('/restaurants/<int:restaurant_id>')
def edit_restaurants(restaurant_id: int):
    return render_template('editrestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/delete')
def delete_restaurants(restaurant_id: int):
    return render_template('deleterestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/menu')
def show_menu(restaurant_id: int):
    return render_template('menu.html')


@app.route('/restaurants/<int:restaurant_id>/menu/new')
def new_menuitem(restaurant_id: int):
    return render_template('newmenuitem.html')


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menuitem_id>')
def edit_menuitem(restaurant_id: int, menuitem_id: int):
    return render_template('editmenuitem.html')


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menuitem_id>/delete')
def delete_menuitem(restaurant_id: int, menuitem_id: int):
    return render_template('deletemenuitem.html')
