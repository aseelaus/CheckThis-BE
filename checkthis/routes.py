"""Routes"""
from checkthis import app
from checkthis.API.ChecklistDefinitions import checklist_definition_bp
from checkthis.API.TaskDefinition import task_definition_bp


# Provide some very basic test URL
@app.route('/')
def home():
    """returns a simple string to test routing"""
    return 'Feels like home!'


# Register Blueprints
app.register_blueprint(task_definition_bp)
app.register_blueprint(checklist_definition_bp)
