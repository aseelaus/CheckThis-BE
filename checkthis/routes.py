'''Routes'''
from checkthis import app
from checkthis.views.TaskDefinition import TaskDefinition_bp

#Provide some very basic test URL
@app.route('/')
def home():
    '''returns a simple string to test routing'''
    return 'Feels like home!'

#Register Blueprints
app.register_blueprint(TaskDefinition_bp)