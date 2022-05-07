from flask import render_template, Blueprint

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(403)
def error403(error):
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(404)
def error404(error):
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(500)
def error500(error):
    return render_template('errors/500.html'), 500