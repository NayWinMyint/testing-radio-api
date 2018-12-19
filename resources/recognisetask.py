import werkzeug, os, json, csv, json, datetime

from flask_restful import Resource, reqparse
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer
from pydub import AudioSegment
from mutagen.mp3 import MP3
import numpy as np
from models.recognisetask import RecogniseTaskModel

with open("dejavu.cnf") as f:
    config = json.load(f)

class RecogniseTask(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('file',
        type=werkzeug.datastructures.FileStorage,
        location='files',
        required=True,
        help="You cannot recognise without an audio file."
    )
    parser.add_argument('channel_id',
        type=str,
        required=True,
        help="Every task needs a channel id."
    )
    parser.add_argument('data',
        type=str,
        required=True,
        help="Please provide the detail of this task."
    )

    def post(self):
        # extract post form data
        data = RecogniseTask.parser.parse_args()
        audio = data['file']
        dataObj = json.loads(data['data'])

        task_uuid = dataObj['task_uuid']
        channel = dataObj['channel']
        broadcasted_datetime = dataObj['broadcasted_datetime']
        created = datetime.datetime.now().timestamp()

        # save the recording file to temp folder
        file_name = audio.filename
        dir_path = '/Volumes/Data/Workspace/pancasikha_radio_monitoring_api/code/temp/to_recognise'
        file_path = os.path.join(dir_path, file_name)
        audio.save(file_path)

        # save to db
        task = RecogniseTaskModel.find_by_task_uuid(task_uuid)
        if task is None:
            task = RecogniseTaskModel(
                task_uuid,
                file_path, #file
                channel, #channel
                broadcasted_datetime, #broadcasted_datetime
                0, #progress
                0, #completed
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

        #
        #
        # if data['file']:
        #     audio = data['file']
        #     file_name = audio.filename
        #     dir_path = '/Volumes/Data/Workspace/pancasikha_radio_monitoring_api/code/temp/audio_to_recognise'
        #     file_path = os.path.join(dir_path, file_name)
        #     audio.save(file_path)
        #
        #     audio_ms = int(round(MP3(file_path).info.length * 1000))
        #     segment_ms = int(10 * 1000)
        #     audio_to_segment = AudioSegment.from_mp3(file_path)
        #
        #     # print(audio_to_segment.get_array_of_samples())
        #     # print(audio_to_segment.frame_rate)
        #
        #     # split sound in 5-second slices and export
        #     for i, chunk in enumerate(audio_to_segment[::segment_ms]):
        #         segment_file_path = os.path.join(dir_path, "sound-%s.mp3" % i)
        #         with open(segment_file_path, "wb") as f:
        #             chunk.export(f, format="mp3")
        #
        #             djv = Dejavu(config)
        #             song = djv.recognize(FileRecognizer, segment_file_path)
        #
        #             with open('test.csv', 'a') as csv_file:
        #                 resultWriter = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #
        #                 resultWriter.writerow([
        #                     (segment_ms*i)/1000,
        #                     song['song_id'],
        #                     song['confidence'],
        #                     song['offset_seconds'],
        #                     song['offset'],
        #                     song['song_name'],
        #                     song['file_sha1'],
        #                     song['match_time'],
        #                     1
        #                 ])
        #
        #             print ("++: %s\n" % song)
        #
        #     # for segment in np.arange(segment_ms,audio_ms,segment_ms):
        #     #     segment_end_ms = segment+segment_ms
        #     #     audio_to_segment[segment:segment_end_ms]
        #     #     segment_file_name = "{}-{}.mp3".format(segment, segment_end_ms)
        #     #     audio_to_segment.export(os.path.join(dir_path, segment_file_name), format="mp3")
        #     #     print "done '{}' ---> ".format(segment_file_name)
        #
        #     # print([i for i in [float(j) / 1000 for j in range(duration_ms)]])
        #     # for i in [j/100 for j in range(duration_ms)]:
        #     #     print(i)
        #         # print(i)
        #
        #     #
        #     # for song in songs:
        #     #     print('----------->')
        #     #     print(song)
        #     #     file_name = song.filename.encode('utf-8')
        #     #     file_path = os.path.join('/Volumes/Data/Workspace/pancasikha_radio_monitoring_api/code/temp', file_name)
        #     #     song.save(file_path)
        #     #
        #     #     print("'{}' uploaded. Start fingerprinting...".format(file_name))
        #     #     djv = Dejavu(config)
        #     #     djv.fingerprint_file(file_path)
        #     #     print("'{}' fingerptinted. Next...".format(file_name))
        #
        #     return {'message': 'Recognising success.'}
        #
        # return {'message': 'No audio file found.'}, 404
