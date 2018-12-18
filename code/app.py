from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api
from flask_jwt import JWT
import boto3
from config import S3_BUCKET, S3_KEY, S3_SECRET

from resources.fingerprinttask import FingerprintTask, FingerprintTaskList, SongFingerprintDir
from resources.recognisetask import RecogniseTask

s3_resource = boto3.resource(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)
bucket = s3_resource.Bucket("pancasikha")

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:nayWIN30@localhost/dejavu'
app.config['SQLCLCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLER_FINGERPRINT'] = '/Volumes/Data/Workspace/pancasikha_radio_monitoring_api/code/temp/to_fingerprint'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/files')
def files():
    for s3_file in bucket.objects.all():
        print (s3_file.key)

    return 'success'
api.add_resource(FingerprintTask, '/fingerprint_task')
api.add_resource(FingerprintTaskList, '/fingerprint_task_list')

api.add_resource(RecogniseTask, '/recognise_task')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
