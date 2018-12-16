from db import db;

class FingerprintTaskModel(db.Model):
    __tablename__ = "fingerprinttasks"

    id = db.Column(db.Integer, primary_key=True)
    task_uuid = db.Column(db.String(50), unique=True, nullable=False)
    dir = db.Column(db.String(256), nullable=False)
    number_of_songs = db.Column(db.Integer, nullable=False)
    completed_songs = db.Column(db.Integer)
    completed = db.Column(db.Boolean, nullable=False)
    scheduled_start_datetime = db.Column(db.String(20), nullable=False)
    scheduled_end_datetime = db.Column(db.String(20), nullable=False)
    created = db.Column(db.String(20), unique=True, nullable=False)
    modified = db.Column(db.String(20))

    def __init__(self,
                task_uuid, dir, number_of_songs, completed_songs, completed,
                scheduled_start_datetime, scheduled_end_datetime,
                created, modified):
        # self.id =  _id
        self.task_uuid = task_uuid
        self.dir = dir
        self.number_of_songs = number_of_songs
        self.completed_songs = completed_songs
        self.completed = completed
        self.scheduled_start_datetime = scheduled_start_datetime
        self.scheduled_end_datetime = scheduled_end_datetime
        self.created = created
        self.modified = modified

    def json(self):
        return {
            # 'id': self._id,
            'task_uuid': self.task_uuid,
            'dir': self.dir,
            'number_of_songs': self.number_of_songs,
            'completed_songs': self.completed_songs,
            'completed': self.completed,
            'scheduled_start_datetime': self.scheduled_start_datetime,
            'scheduled_end_datetime': self.scheduled_end_datetime,
            'created': self.created,
            'modified': self.modified,
        }

    @classmethod
    def find_by_task_uuid(cls, task_uuid):
        return cls.query.filter_by(task_uuid=task_uuid).first()

    @classmethod
    def find_by_created_date(cls, created):
        return cls.query.filter_by(created=created).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
