
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_required, current_user
from milkanalyzer.models import AIModel, Value
from milkanalyzer.aimodels.forms import AIModelForm
from milkanalyzer import db

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
