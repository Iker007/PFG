
from flask import render_template, redirect, url_for, Blueprint, current_app
from flask_login import login_required, current_user
from milkanalyzer.models import Prediction
from milkanalyzer import db
import os, subprocess


predictions = Blueprint('predictions', __name__)

@predictions.route("/predictions")
@login_required
def prediction_list():
    predictions = Prediction.query.filter_by(user_id = current_user.id).all()
    return render_template('predictions.html', title='Your predictions', predictions=predictions)

@predictions.route("/predictions/<int:id>/download")
@login_required
def download_prediction(id):
    prediction = Prediction.query.get_or_404(id)
    predictions = Prediction.query.filter_by(user_id = current_user.id).all()
    print(prediction.prediction_file)
    #file_path = os.path.join(current_app.root_path, 'static/predicted_files')
    file_path = "D:\\Uni\\2021-22\\PFG\\git\\PFG\\Web\\milkanalyzer\\static\\predicted_files\\" + prediction.prediction_file
    print(file_path)
    subprocess.Popen(f'explorer /select, {file_path}')
    return render_template('predictions.html', title='Your predictions', predictions=predictions)