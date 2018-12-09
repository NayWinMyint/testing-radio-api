from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT

from resources.song import SongFingerprint

UPLOAD_FOLDER = '/upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)

@app.route('/')
def handler():
    pass

api.add_resource(SongFingerprint, '/fingerprint')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
