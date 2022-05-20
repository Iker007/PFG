from flask import render_template, request, Blueprint
from milkanalyzer.models import AIModel, Restaurant, SelectedProduct


main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    aimodels = AIModel.query.all()
    return render_template('home.html', aimodels=aimodels)

@main.route("/about")
def about():
    selected_products = SelectedProduct.query.all()
    return render_template('about.html', title='milkanalyzer', selected_products=selected_products)