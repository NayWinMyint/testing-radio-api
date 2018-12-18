from db import db;

class RecogniseTaskModel(db.Model):
    __tablename__ = "recognisetasks"

    id = db.Column(db.Integer, primary_key=True)
    task_uuid = db.Column(db.String(50), unique=True, nullable=False)
    file = db.Column(db.String(256), nullable=False)
    channel = db.Column(db.String(40), nullable=False)
    broadcasted_datetime = db.Column(db.String(20), nullable=False)
    progress = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)
    created = db.Column(db.String(20), unique=True, nullable=False)
    modified = db.Column(db.String(20))

    def __init__(self,
                task_uuid, file, channel,
                broadcasted_datetime,
                progress, completed,
                created, modified):
        self.task_uuid = task_uuid
        self.file = file
        self.channel = channel
        self.broadcasted_datetime = broadcasted_datetime
        self.progress = progress
        self.completed = completed
        self.created = created
        self.modified = modified

    def json(self):
        return {
            # 'id': self._id,
            'task_uuid': self.task_uuid,
            'file': self.dir,
            'channel': self.channel,
            'broadcasted_datetime': self.broadcasted_datetime,
            'progress': self.progress,
            'completed': self.completed,
            'created': self.created,
            'modified': self.modified,
        }

    @classmethod
    def find_by_task_uuid(cls, task_uuid):
        return cls.query.filter_by(task_uuid=task_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
