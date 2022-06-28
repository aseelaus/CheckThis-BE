from flask import Blueprint

#Blueprint Creation. Note the URL_Prefix!
TaskDefinition_bp = Blueprint(name='task_definition_blueprint', import_name= __name__, url_prefix='/TaskDefinitions')

@TaskDefinition_bp.route('/hello')
def hw2():
    return 'Hello from the other side!'