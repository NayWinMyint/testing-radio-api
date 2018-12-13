from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT
import boto3
from config import S3_BUCKET, S3_KEY, S3_SECRET

from resources.song import SongFingerprint, SongFingerprintDir
from resources.audio import AudioRecognise

s3_resource = boto3.resource(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)
bucket = s3_resource.Bucket("pancasikha")

app = Flask(__name__)
api = Api(app)

@app.route('/files')
def files():
    for s3_file in bucket.objects.all():
        print (s3_file.key)

    return 'success'
api.add_resource(SongFingerprint, '/fingerprint')
api.add_resource(SongFingerprintDir, '/fingerprint_dir')
api.add_resource(AudioRecognise, '/recognise')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
