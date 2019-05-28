from flask import Flask, render_template
from src.routes.routes import *

if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)
