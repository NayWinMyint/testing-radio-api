import werkzeug, os, json
import boto3
import datetime

from flask_restful import Resource, reqparse
from dejavu import Dejavu
from models.fingerprinttask import FingerprintTaskModel


with open("dejavu.cnf") as f:
    config = json.load(f)

class FingerprintTask(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file',
        type=werkzeug.datastructures.FileStorage,
        location='files',
        required=True,
        action='append',
        help="You cannot fingerprint without an audio file."
    )
    parser.add_argument('number_of_songs',
        type=str,
        required=True,
        help="You need to provide the total number of songs to upload."
    )
    parser.add_argument('task_uuid',
        type=str,
        required=True,
        help="A unique task id is required."
    )
    parser.add_argument('save_to_db',
        type=str,
        required=True,
        help="The server needs to know whether to save the data or not."
    )

    def get(self, id):
        task = FingerprintTaskModel.find_by_id(id)
        if task:
            return task.json()
        return {'message': 'Task not found'}, 404

    def post(self):
        data = FingerprintTask.parser.parse_args()

        songs = data['file']
        number_of_songs = int(data['number_of_songs'])
        task_uuid = data['task_uuid']
        save_to_db = data['save_to_db']

        for song in songs:
            file_name = song.filename
            file_path = os.path.join('/Volumes/Data/Workspace/pancasikha_radio_monitoring_api/code/temp/to_fingerprint', file_name)
            song.save(file_path)

        task = FingerprintTaskModel.find_by_task_uuid(task_uuid)

        if save_to_db is '1':
            # create scheduled time slot
            today_datetime = datetime.datetime.now()
            created = today_datetime.timestamp()

            scheduled_start_datetime = today_datetime.replace(hour=22, minute=0, second=0, microsecond=0).timestamp()

            scheduled_end_datetime = today_datetime + datetime.timedelta (days=1)
            scheduled_end_datetime = scheduled_end_datetime.replace(hour=9, minute=0, second=0, microsecond=0).timestamp()

            print('{} -> task uuid -> '.format(task_uuid))
            print('{} -> coming uuid -> '.format(task_uuid))

            if task is None:
                print('task is none')
                task = FingerprintTaskModel(
                    task_uuid,
                    '/Volumes/Data/Workspace/pancasikha_radio_monitoring_api/code/temp/to_fingerprint', #dir
                    number_of_songs, #number_of_songs
                    0, #completed_songs
                    0, #completed
                    scheduled_start_datetime, #scheduled_start_datetime
                    scheduled_end_datetime, #scheduled_end_datetime
                    created, #created datetime
                    created #modified datetime
                )

                try:
                    task.save_to_db()
                except:
                    return {'message': 'An error occured inserting the task'}, 500
            else:
                print('task found --> nothing to do')

        return {'message': 'Task created'}, 201

    def delete(self, id):
        task = FingerprintTaskModel.find_by_id(id)
        if task:
            task.delete_from_db()

        return {'message': 'Task deleted'}

class FingerprintTaskList(Resource):
    def get(self):
        # return {'tasks': [task.json() for task in FingerprintTaskModel.query.all()]}
        return {'tasks': list(map(lambda task: task.json(), FingerprintTaskModel.query.all()))}

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
