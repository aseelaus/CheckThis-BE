from flask import Blueprint, request, Response
from checkthis.models import TaskDefinition, task_definitions_schema, task_definition_schema
from checkthis.models import db

# Blueprint Creation. Note the URL_Prefix!
task_definition_bp = Blueprint(name='task_definition_blueprint', import_name=__name__, url_prefix='/TaskDefinitions')


# Provide some basic test URL
@task_definition_bp.route('/hello')
def hw2():
    return 'Hello from the other side!'


@task_definition_bp.route('/', methods=['GET', 'POST'])
def base():
    if request.method == 'GET':
        task_definitions = TaskDefinition.query.all()
        return Response(task_definitions_schema.dumps(task_definitions), status=200, mimetype="application/json")
    if request.method == 'POST':
        # TODO referencing a checklist_definition_id that does not exist should throw an error?
        json = request.json
        new_task_definition = TaskDefinition(title=json["title"],
                                             checklist_definition_id=json["checklist_definition_id"],
                                             description=json["description"])
        db.session.add(new_task_definition)
        db.session.commit()
        return Response(task_definition_schema.dumps(new_task_definition), status=200, mimetype="application/json")
    else:
        return Response(status=405)


@task_definition_bp.route('/<task_definition_id>/', methods=['GET'])
def specific(task_definition_id):
    if request.method == 'GET':
        task_definition = TaskDefinition.query.get(task_definition_id)
        return task_definition_schema.dump(task_definition)
    if request.method == 'PUT':
        # TODO implement
        return Response(status=405)
    else:
        return Response(status=405)
