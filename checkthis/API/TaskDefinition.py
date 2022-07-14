import sys

from flask import Blueprint, request, Response
from checkthis.models import TaskDefinition, task_definitions_schema, task_definition_schema
from checkthis.models import db
from sqlalchemy import exc as sql_alchemy_exceptions

# Blueprint Creation. Note the URL_Prefix!
task_definition_bp = Blueprint(name='task_definition_blueprint', import_name=__name__, url_prefix='/TaskDefinitions')

# Some commonly used attributes
_db_integrity_error_rsp = Response("Database Integrity Error. Do all referenced objects exist?", status=400)
_mimetype_json = "application/json"


# TODO for all routes: find a better way to query json, what if request.json is not compliant with the model?

@task_definition_bp.route('/', methods=['GET', 'POST'])
def base():
    if request.method == 'GET':
        task_definitions = TaskDefinition.query.all()
        return Response(task_definitions_schema.dumps(task_definitions), status=200, mimetype=_mimetype_json)
    if request.method == 'POST':
        try:
            json = request.json
            new_task_definition = TaskDefinition(title=json["title"],
                                                 checklist_definition_id=json["checklist_definition_id"],
                                                 description=json["description"])
            db.session.add(new_task_definition)
            db.session.commit()
        except sql_alchemy_exceptions.IntegrityError:
            db.session.rollback()
            return _db_integrity_error_rsp

        return Response(task_definition_schema.dumps(new_task_definition), status=200, mimetype=_mimetype_json)
    else:
        return Response(status=405)


@task_definition_bp.route('/<task_definition_id>/', methods=['GET', 'PUT', 'DELETE'])
def specific(task_definition_id):
    if request.method == 'GET':
        task_definition = TaskDefinition.query.get(task_definition_id)
        if task_definition is None:
            return Response(status=404)
        return Response(task_definition_schema.dumps(task_definition), status=200, mimetype=_mimetype_json)
    if request.method == 'PUT':
        try:
            task_definition = TaskDefinition.query.get(task_definition_id)
            if task_definition is None:
                return Response(status=404)
            json = request.json
            task_definition.title = json["title"]
            task_definition.checklist_definition_id = json["checklist_definition_id"]
            task_definition.description = json["description"]
            db.session.commit()
        except sql_alchemy_exceptions.IntegrityError:
            db.session.rollback()
            return _db_integrity_error_rsp

        return Response(task_definition_schema.dumps(task_definition), status=200, mimetype=_mimetype_json)
    if request.method == 'DELETE':
        task_definition = TaskDefinition.query.get(task_definition_id)
        if task_definition is None:
            return Response(status=404)

        db.session.delete(task_definition)
        db.session.commit()
        return Response(status=200)
    else:
        return Response(status=405)
