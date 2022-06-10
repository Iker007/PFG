
import imp
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask_login import login_required, current_user
from milkanalyzer.aimodels.utils import store_csv
from milkanalyzer.models import AIModel, Value, Prediction
from milkanalyzer.aimodels.forms import AIModelForm, SelectFileForm
from milkanalyzer import db
import tensorflow as tf
import pandas as pd
import os
import pickle
import numpy as np
import sklearn

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
@login_required
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
        dataframe.rename(columns={"Grasa (% P/P)": "grasa", "Proteina (% P/P)": "proteina", "Extracto (% P/P)": "extracto", "Lactosa (% P/P)": "lactosa", "Celulas (/ml*1000)": "celulas", "Urea (mg/l)": "urea"}, inplace = True)
        if aimodel.id < 3:
            currentaimodel = tf.keras.models.load_model('.\.\.\Model\\' + aimodel.name + '\content\\' + aimodel.name)
            modeltype = 1
        elif aimodel.id == 3:
            currentaimodel = tf.keras.models.load_model('.\.\.\Model\\' + aimodel.name + '\content\\' + aimodel.name)
            modeltype = 2
        else:
            currentaimodel = pickle.load(open('.\.\.\Model\\' + aimodel.name + '.sav', 'rb'))
            modeltype = 0

        if modeltype == 1:
            
            predictionslist = []
            for index, row in dataframe.iterrows():
                sample = {
                    "grasa": row['grasa'],
                    "proteina": row['proteina'],
                    "extracto": row['extracto'],
                    "lactosa": row['lactosa'],
                    "celulas": row['celulas'],
                    "urea": row['urea'],
                }
                
                input_dict = {name: tf.convert_to_tensor([value]) for name, value in sample.items()}
                predictions = currentaimodel.predict(input_dict)

                if predictions < 0:
                    predictions[0] = 0

                predictionslist.append(float("{:.2f}".format(100 * predictions[0][0])))

        elif modeltype == 2:

            predictionslist = []
            for index, row in dataframe.iterrows():
                sample = np.array([[
                    row['grasa'],
                    row['proteina'],
                    row['extracto'],
                    row['lactosa'],
                    row['celulas'],
                    row['urea'],
                ]])
                            
                predictions = currentaimodel.predict(sample)

                if predictions < 0:
                    predictions[0] = 0

                predictionslist.append(float("{:.2f}".format(100 * predictions[0][0])))

        else:

            predictionslist = []
            for index, row in dataframe.iterrows():

                New_grasa = row['grasa']
                New_proteina = row['proteina']
                New_extracto = row['extracto']
                New_lactosa = row['lactosa']
                New_celulas = row['celulas']
                New_urea = row['urea']
                predictions = currentaimodel.predict([[New_grasa, New_proteina, New_extracto, New_lactosa, New_celulas, New_urea]])

                predictionslist.append(predictions)
        if modeltype == 0:
            dataframe['Presencia Patogeno'] = predictionslist
        else:
            dataframe['Probabilidad Patogeno'] = predictionslist
        dataframe.rename(columns={"grasa" : "Grasa (% P/P)", "proteina" : "Proteina (% P/P)", "extracto" : "Extracto (% P/P)", "lactosa" : "Lactosa (% P/P)" , "celulas" : "Celulas (/ml*1000)", "urea" : "Urea (mg/l)"}, inplace = True)
        dataframe.to_csv(os.path.join(current_app.root_path, 'static/predicted_files', file_form.file_name.data) + '.csv', sep=';', encoding='utf-8')

        prediction = Prediction(prediction_file=file_form.file_name.data + '.csv', user_id=current_user.id, aimodel_id=aimodel.id)
        db.session.add(prediction)
        db.session.commit()

        flash('¡Predicciones generadas con éxito!', 'success')
        return redirect(url_for('main.home'))
    return render_template('use_aimodel.html', title='Use Model', form=file_form, aimodel=aimodel)
