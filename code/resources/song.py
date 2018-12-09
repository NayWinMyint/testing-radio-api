import werkzeug, os, json

from flask_restful import Resource, reqparse
from dejavu import Dejavu

with open("dejavu.cnf.SAMPLE") as f:
    config = json.load(f)

class SongFingerprint(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file',
        type=werkzeug.datastructures.FileStorage,
        location='files',
        required=True,
        help="You cannot fingerprint without an audio file."
    )

    def post(self):
        print('heki')
        data = SongFingerprint.parser.parse_args()
        print('heki')
        print(data['file'])
        if data['file']:
            song = data['file']
            file_name = str(song.filename)
            song.save(os.path.join(file_name))

            djv = Dejavu(config)
            djv.fingerprint_file(file_name)

            return {'message': 'Fingerprinting success.'}

        return {'message': 'No audio file found.'}, 404
