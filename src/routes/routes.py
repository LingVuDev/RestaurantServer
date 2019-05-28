from flask import Flask, render_template

app = Flask("main", template_folder="src/templates")


@app.route('/')
@app.route('/restaurants')
def show_restaurants():
    return render_template('restaurants.html')
