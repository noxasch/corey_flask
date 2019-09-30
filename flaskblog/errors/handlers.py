from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

# errorhandler - for blueprint speicific
# app_errorhandler = for entire app
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404 # page, STATUS_CODE
    # default status code response is 200


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

