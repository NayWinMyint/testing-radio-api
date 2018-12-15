import werkzeug, os, json

from flask_restful import Resource, reqparse
from dejavu import Dejavu
import boto3

with open("dejavu.cnf") as f:
    config = json.load(f)

class SongUpload(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file',
        type=werkzeug.datastructures.FileStorage,
        location='files',
        required=True,
        action='append',
        help="You cannot fingerprint without an audio file."
    )

    def post(self):
        data = SongUpload.parser.parse_args()
        print(data)
        if data['file']:
            songs = data['file']
            for song in songs:
                print('----------->')
                print(song)
                file_name = song.filename
                file_path = os.path.join('/Volumes/Data/Workspace/pancasikha_radio_monitoring_api/code/temp', file_name)
                song.save(file_path)
                print("'{}' uploaded.".format(file_name))
                #
                # print("'{}' uploaded. Start fingerprinting...".format(file_name))
                # djv = Dejavu(config)
                # djv.fingerprint_file(file_path)
                # print("'{}' fingerptinted. Next...".format(file_name))

            return {'message': 'Upload success.'}

        return {'message': 'No audio file found.'}, 404

class SongFingerprintDir(Resource):
    def post(self):

        local_dir = '/Volumes/Data/Workspace/pancasikha_radio_monitoring_api/code/temp'
        prefix = 'to_fingerprint/'

        print("started ->")
        djv = Dejavu(config)
        djv.fingerprint_directory(local_dir, [".mp3"])
        print("ended ->")

        for filename in os.listdir(local_dir):
            if filename.endswith(".mp3"):
                remotekeyfile = prefix + filename
                localfilepath = os.path.join(local_dir, filename)

                try:
                    if os.path.isfile(localfilepath):
                        #move fingerprinted songs to s3
                        s3_client = boto3.client('s3')
                        s3_client.upload_file(localfilepath, 'pancasikha', remotekeyfile)
                        print("{} done moved".format(filename))
                        os.unlink(localfilepath)
                except Exception as e:
                    print(e)


        return {'message': 'Fingerprinting success.'}

        return {'message': 'No audio file found.'}, 404
