import werkzeug, os, json

from flask_restful import Resource, reqparse
from dejavu import Dejavu

with open("dejavu.cnf") as f:
    config = json.load(f)

class SongFingerprint(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('files',
        type=werkzeug.datastructures.FileStorage,
        location='files',
        required=True,
        action='append',
        help="You cannot fingerprint without an audio file."
    )

    def post(self):
        data = SongFingerprint.parser.parse_args()
        print(data)
        if data['files']:
            songs = data['files']
            for song in songs:
                print('----------->')
                print(song)
                file_name = song.filename
                file_path = os.path.join('/Volumes/Data/Workspace/pancasikha_radio_monitoring_api/code/temp', file_name)
                song.save(file_path)

                print("'{}' uploaded. Start fingerprinting...".format(file_name))
                djv = Dejavu(config)
                djv.fingerprint_file(file_path)
                print("'{}' fingerptinted. Next...".format(file_name))

            return {'message': 'Fingerprinting success.'}

        return {'message': 'No audio file found.'}, 404
