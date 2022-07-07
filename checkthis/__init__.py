from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()


def create_app(database_uri):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()

    # init DB and Schema
    db.init_app(app)
    ma.init_app(app)

    # register models and create corresponding tables
    from checkthis.models import ChecklistDefinition, TaskDefinition
    db.create_all()

    # Register Blueprints
    from checkthis.API.ChecklistDefinitions import checklist_definition_bp
    from checkthis.API.TaskDefinition import task_definition_bp
    app.register_blueprint(task_definition_bp)
    app.register_blueprint(checklist_definition_bp)

    # Return
    return app


