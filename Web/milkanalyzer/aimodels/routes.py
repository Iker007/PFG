
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask_login import login_required, current_user
from milkanalyzer.aimodels.utils import store_csv
from milkanalyzer.models import AIModel, Value, Prediction
from milkanalyzer.aimodels.forms import AIModelForm, SelectFileForm
from milkanalyzer import db
from datetime import datetime
import tensorflow as tf
import pandas as pd
import os

aimodels = Blueprint('aimodels', __name__)

@aimodels.route("/aimodel/new", methods=['GET', 'POST'])
@login_required
def new_aimodel():
    if current_user.username != 'admin':
        abort(403)
    else:
        aimodel_form = AIModelForm()
        if aimodel_form.validate_on_submit():
            aimodel = AIModel(name=aimodel_form.name.data, type=aimodel_form.type.data, description=aimodel_form.description.data, url=aimodel_form.url.data)
            db.session.add(aimodel)
            db.session.commit()
            flash('AIModel information succesfully added!', 'success')
            return redirect(url_for('main.home'))
        return render_template('add_aimodel.html', title='New aimodel', form=aimodel_form, legend='Add aimodel')

@aimodels.route("/aimodel/<int:id>")
def aimodel(id):
    aimodel = AIModel.query.get_or_404(id)
    values = Value.query.filter_by(aimodel_id = aimodel.id).all()
    return render_template('aimodel.html', title=aimodel.name, aimodel=aimodel, values=values)

@aimodels.route("/aimodel/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_aimodel(id):
    aimodel = AIModel.query.get_or_404(id)
    if current_user.username != 'admin':
        abort(403)
    update_aimodel_form = AIModelForm()
    if update_aimodel_form.validate_on_submit():
        aimodel.name = update_aimodel_form.name.data
        aimodel.type = update_aimodel_form.type.data
        aimodel.description = update_aimodel_form.description.data
        aimodel.url = update_aimodel_form.url.data
        db.session.commit()
        flash('AIModel information succesfully updated!', 'success')
        return redirect(url_for('aimodels.aimodel', id=aimodel.id))
    elif request.method == 'GET':
        update_aimodel_form.name.data = aimodel.name
        update_aimodel_form.type.data = aimodel.type
        update_aimodel_form.description.data = aimodel.description
        update_aimodel_form.url.data = aimodel.url
    return render_template('add_aimodel.html', title='Update aimodel', form=update_aimodel_form, legend='Update aimodel')

@aimodels.route("/aimodel/<int:id>/delete", methods=['POST'])
@login_required
def delete_aimodel(id):
    aimodel = AIModel.query.get_or_404(id)
    if current_user.username != 'admin':
        abort(403)
    db.session.delete(aimodel)
    db.session.commit()
    flash('AIModel information succesfully removed!', 'success')
    return redirect(url_for('main.home'))

@aimodels.route("/aimodel/<int:id>/use", methods=['GET', 'POST'])
@login_required
def use_aimodel(id):
    aimodel = AIModel.query.get_or_404(id)
    file_form = SelectFileForm()
    if file_form.validate_on_submit():
        csv_file = store_csv(file_form.csv_file.data)
        dataframe = pd.read_csv(os.path.join(current_app.root_path, 'static/prediction_files', csv_file), delimiter=';')
        dataframe.rename(columns={"Grasa (% P/P)": "grasa", "Proteina (% P/P)": "proteina", "Extracto (% P/P)": "extracto", "Lactosa (% P/P)": "lactosa", "Celulas (/ml*1000)": "celulas", "Bacterias (ufc/ml*1000)": "bacterias", "Inhb.": "inhb", "PC 1": "pc1", "Urea (mg/l)": "urea"}, inplace = True)
        currentaimodel = tf.keras.models.load_model('.\.\.\Model\MyModel_v3\content\MyModel_v3')

        predictionslist = []
        for index, row in dataframe.iterrows():
            sample = {
                "grasa": row['grasa'],
                "proteina": row['proteina'],
                "extracto": row['extracto'],
                "lactosa": row['lactosa'],
                "celulas": row['celulas'],
                "bacterias": row['bacterias'],
                "inhb": row['inhb'],
                "pc1": row['pc1'],
                "urea": row['urea'],
            }
            
            input_dict = {name: tf.convert_to_tensor([value]) for name, value in sample.items()}
            predictions = currentaimodel.predict(input_dict)

            predictionslist.append(float("{:.2f}".format(100 * predictions[0][0])))

        dataframe['Probabilidad Patogeno'] = predictionslist
        dataframe.rename(columns={"grasa" : "Grasa (% P/P)", "proteina" : "Proteina (% P/P)", "extracto" : "Extracto (% P/P)", "lactosa" : "Lactosa (% P/P)" , "celulas" : "Celulas (/ml*1000)", "bacterias" : "Bacterias (ufc/ml*1000)", "inhb" : "Inhb.", "pc1" : "PC 1", "urea" : "Urea (mg/l)"}, inplace = True)
        now = datetime.now()
        dataframe.to_csv(os.path.join(current_app.root_path, 'static/predicted_files', file_form.file_name.data) + '.csv', sep=';', encoding='utf-8')

        prediction = Prediction(prediction_file=file_form.file_name.data + '.csv', user_id=current_user.id)
        db.session.add(prediction)
        db.session.commit()

        flash('Predictions succesfully generated!', 'success')
        return redirect(url_for('main.home'))
    return render_template('use_aimodel.html', title='Use Model', form=file_form, aimodel=aimodel)
