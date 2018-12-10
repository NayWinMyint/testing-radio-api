from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT

from resources.song import SongFingerprint
from resources.audio import AudioRecognise

app = Flask(__name__)
api = Api(app)

api.add_resource(SongFingerprint, '/fingerprint')
api.add_resource(AudioRecognise, '/recognise')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
