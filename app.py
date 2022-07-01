'''CheckThis app'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from views.TaskDefinition import TaskDefinition_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Provide some very basic test URL
@app.route('/')
def home():
    '''returns a simple string to test routing'''
    return 'Feels like home!'

#Register Blueprints
app.register_blueprint(TaskDefinition_bp)

#Run App
if __name__ == "__main__":
    app.run(debug = True)
