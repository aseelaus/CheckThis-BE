from flask import Blueprint, request, Response
from checkthis.models import ChecklistDefinition, checklist_definition_schema, checklist_definitions_schema
from checkthis import db

# Blueprint Creation. Note the URL_Prefix!
checklist_definition_bp = Blueprint(name='checklist_definition_blueprint', import_name=__name__,
                                    url_prefix='/ChecklistDefinitions')


# Provide some basic test URL
@checklist_definition_bp.route('/hello')
def hw2():
    return 'Hello from the other side!'


@checklist_definition_bp.route('/', methods=['GET', 'POST'])
def base():
    if request.method == 'GET':
        checklist_definitions = ChecklistDefinition.query.all()
        return Response(checklist_definitions_schema.dumps(checklist_definitions),
                        status=200,
                        mimetype="application/json")

    if request.method == 'POST':
        json = request.json
        new_checklist_definition = ChecklistDefinition(title=json["title"], description=json["description"])
        db.session.add(new_checklist_definition)
        db.session.commit()
        return Response(checklist_definition_schema.dump(new_checklist_definition),
                        status=200,
                        mimetype="application/json")

    else:
        return Response(status=405)


@checklist_definition_bp.route('/<id>/', methods=['GET', 'PUT'])
def specific(checklist_definition_id):
    if request.method == 'GET':
        checklist_def = ChecklistDefinition.query.get(checklist_definition_id)
        return Response(checklist_definition_schema.dumps(checklist_def),
                        status=200,
                        mimetype="application/json")

    if request.method == 'PUT':
        # TODO implement
        return Response('not yet implemented', status=501)

    else:
        return Response(status=405)