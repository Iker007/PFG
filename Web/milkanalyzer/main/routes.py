from flask import render_template, Blueprint
from milkanalyzer.models import AIModel

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    aimodels = AIModel.query.all()
    return render_template('home.html', aimodels=aimodels)

@main.route("/about")
def about():
    return render_template('about.html', title='milkanalyzer')