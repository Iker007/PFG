from flask import render_template, request, Blueprint
from getitnow.models import Restaurant, SelectedProduct


main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    restaurants = Restaurant.query.all()
    selected_products = SelectedProduct.query.all()
    return render_template('home.html', restaurants=restaurants, selected_products=selected_products)

@main.route("/about")
def about():
    selected_products = SelectedProduct.query.all()
    return render_template('about.html', title='GetItNow', selected_products=selected_products)