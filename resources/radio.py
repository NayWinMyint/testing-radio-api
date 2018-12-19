import json
import datetime

from flask_restful import Resource, reqparse
from models.radio import RadioModel

class Radio(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('recognised_times',
        type=int,
        required=True,
        help="This field requires when you update the channel."
    )
    parser.add_argument('matches_found',
        type=int,
        required=True,
        help="This field requires when you update the channel."
    )

    def get(self, name):
        channel = RadioModel.find_by_name(name)
        if channel:
            return channel.json()
        return {'message': 'Channel not found'}, 404

    def post(self, name):
        if RadioModel.find_by_name(name):
            return {'message': "A channel with name '{}' already existed.".format(name)}, 400

        data = Radio.parser.parse_args()
        created = modified = datetime.datetime.now().timestamp()
        channel = RadioModel(
            name,
            data['recognised_times'],
            data['matches_found'],
            created,
            modified
        )

        try:
            channel.save_to_db()
        except:
            return {'message': 'An error occurred while creating the channel.'}, 500

        return channel.json(), 201

    def delete(self, name):
        channel = RadioModel.find_by_name(name)
        if channel:
            channel.delete_from_db()

        return {'message': 'Channel deleted'}

    def put(self, name):
        data = Radio.parser.parse_args()

        channel = RadioModel.find_by_name(name)

        if channel is None:
            channel = RadioModel(name, **data)
            channel.created = datetime.datetime.now().timestamp()
        else:
            channel.recognised_times = data['recognised_times']
            channel.matches_found = data['matches_found']
            channel.modified = datetime.datetime.now().timestamp()

        channel.save_to_db()

        return channel.json()

class RadioList(Resource):
    def get(self):
        return {'channels': list(map(lambda channel: channel.json(), RadioModel.query.all()))}
