import subprocess, os
from flask import render_template, Blueprint, current_app
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

@main.route("/guide")
def guide():
    return render_template('guide.html', title='milkanalyzer')

@main.route("/plantilla")
def plantilla():
    file_path = os.path.join(current_app.root_path, 'static\\Plantilla.csv')
    print(file_path)
    subprocess.Popen(f'explorer /select, {file_path}')
    return render_template('guide.html', title='milkanalyzer')