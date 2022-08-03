from flask import Blueprint, request, Response
from checkthis.models import TaskDefinition, task_definitions_schema, task_definition_schema
from checkthis.models import db
from sqlalchemy import exc as sql_alchemy_exceptions
from checkthis.errors import Error, TaskDefinitionRelationError, TaskDefinitionMissingParentError, \
    TaskDefinitionCircularReferenceError

# Blueprint Creation. Note the URL_Prefix!
task_definition_bp = Blueprint(name='task_definition_blueprint', import_name=__name__, url_prefix='/TaskDefinitions')

# Some commonly used attributes
_db_integrity_error_rsp = Response("Database Integrity Error. Do all referenced objects exist?", status=400)
_mimetype_json = "application/json"


def _error_response(error: Error):
    return Response(error.message, status=400)


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
                                                 parent_task_definition_id=json["parent_task_definition_id"],
                                                 description=json["description"])
            new_task_definition.validate_store()
        except sql_alchemy_exceptions.IntegrityError:
            db.session.rollback()
            return _db_integrity_error_rsp
        except TaskDefinitionRelationError:
            db.session.rollback()
            return _error_response(TaskDefinitionRelationError)
        except TaskDefinitionMissingParentError:
            db.session.rollback()
            return _error_response(TaskDefinitionMissingParentError)
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
            task_definition.parent_task_definition_id = json["parent_task_definition_id"]
            task_definition.description = json["description"]
            task_definition.validate_store()
        except sql_alchemy_exceptions.IntegrityError:
            db.session.rollback()
            return _db_integrity_error_rsp
        except TaskDefinitionRelationError:
            db.session.rollback()
            return _error_response(TaskDefinitionRelationError)
        except TaskDefinitionMissingParentError:
            db.session.rollback()
            return _error_response(TaskDefinitionMissingParentError)
        except TaskDefinitionCircularReferenceError:
            db.session.rollback()
            return _error_response(TaskDefinitionCircularReferenceError)

        return Response(task_definition_schema.dumps(task_definition), status=200, mimetype=_mimetype_json)
    if request.method == 'DELETE':
        """Deletes the Object and all its descendants"""
        task_definition = TaskDefinition.query.get(task_definition_id)
        if task_definition is None:
            return Response(status=404)
        db.session.delete(task_definition)
        db.session.commit()
        return Response(status=200)
    else:
        return Response(status=405)
