
from flask import render_template, Blueprint, current_app
from flask_login import login_required, current_user
from milkanalyzer.models import Prediction, User, AIModel, Value
import os, subprocess, pdfkit


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
    file_path = os.path.join(current_app.root_path, 'static\\predicted_files\\' + prediction.prediction_file)
    print(file_path)
    subprocess.Popen(f'explorer /select, {file_path}')
    return render_template('predictions.html', title='Your predictions', predictions=predictions)

@predictions.route("/predictions/<int:id>/report")
@login_required
def report(id):
    prediction = Prediction.query.get_or_404(id)
    predictions = Prediction.query.filter_by(user_id = current_user.id).all()
    user = User.query.get_or_404(prediction.user_id)
    usedaimodel = AIModel.query.get_or_404(prediction.aimodel_id)
    values = Value.query.filter_by(aimodel_id = usedaimodel.id).all()
    url = os.path.join(current_app.root_path, 'static\\reports\\Report-' + str(prediction.id) + '.pdf')
 
    html = render_template("report.html", prediction=prediction, user=user, usedaimodel=usedaimodel, values=values)
    wkhtmltopdf_url = os.path.join(current_app.root_path, 'static\\wkhtmltox\\bin\\wkhtmltopdf.exe')
    print(wkhtmltopdf_url)

    config = pdfkit.configuration(wkhtmltopdf=bytes(wkhtmltopdf_url, 'utf8'))
    

    pdfkit.from_string(html, output_path=url, configuration=config)

    subprocess.Popen(f'explorer /select, {url}')
    return render_template('predictions.html', title='Your predictions', predictions=predictions)