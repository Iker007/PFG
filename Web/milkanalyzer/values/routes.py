
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_required, current_user
from milkanalyzer.models import AIModel, Value
from milkanalyzer.values.forms import ValueForm
from milkanalyzer import db

values = Blueprint('values', __name__)

@values.route("/aimodel/<int:id>/value/new", methods=['GET', 'POST'])
@login_required
def new_value(id):
    if current_user.username != 'admin':
        abort(403)
    else:
        value_form = ValueForm()
        if value_form.validate_on_submit():
            value = Value(name=value_form.name.data, proportion=value_form.proportion.data, description=value_form.description.data)
            value.aimodel_id = id
            db.session.add(value)
            db.session.commit()
            flash('Value information succesfully added!', 'success')
            return redirect(url_for('main.home'))
        return render_template('add_value.html', title='New value', form=value_form, legend='Add value')

@values.route("/aimodel/<int:aimodel_id>/value/<int:id>")
def value(aimodel_id, id):
    value = Value.query.get_or_404(id)
    aimodel = AIModel.query.get_or_404(aimodel_id)
    aimodel_id = aimodel_id
    return render_template('value.html', title=value.name, value=value, aimodel=aimodel)

@values.route("/aimodel/<int:aimodel_id>/value/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_value(aimodel_id, id):
    value = Value.query.get_or_404(id)
    aimodel = AIModel.query.get_or_404(aimodel_id)
    aimodel_id = aimodel_id
    if current_user.username != 'admin':
        abort(403)
    update_value_form = ValueForm()
    if update_value_form.validate_on_submit():
        value.name = update_value_form.name.data
        value.proportion = update_value_form.proportion.data
        value.description = update_value_form.description.data
        db.session.commit()
        flash('Value information succesfully updated!', 'success')
        return redirect(url_for('values.value', aimodel_id=aimodel.id, id=value.id))
    elif request.method == 'GET':
        update_value_form.name.data = value.name
        update_value_form.proportion.data = value.proportion
        update_value_form.description.data = value.description
    return render_template('add_value.html', title='Update value', form=update_value_form, legend='Update value', aimodel=aimodel)

@values.route("/aimodel/<int:aimodel_id>/value/<int:id>/delete", methods=['POST'])
@login_required
def delete_value(aimodel_id, id):
    value = Value.query.get_or_404(id)
    aimodel_id = aimodel_id
    if current_user.username != 'admin':
        abort(403)
    db.session.delete(value)
    db.session.commit()
    flash('Value information succesfully removed!', 'success')
    return redirect(url_for('main.home'))

@values.route("/aimodel/<int:aimodel_id>/value/<int:id>/add", methods=['GET', 'POST'])
@login_required
def add_value(aimodel_id, id):
    value = Value.query.get_or_404(id)
    aimodel_id = aimodel_id
    db.session.commit()
    flash('Value added to chart!', 'success')
    return redirect(url_for('main.home'))
