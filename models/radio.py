from db import db;

class RadioModel(db.Model):
    __tablename__ = "radios"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    recognised_times = db.Column(db.Integer)
    matches_found = db.Column(db.Integer)
    created = db.Column(db.String(20))
    modified = db.Column(db.String(20))

    def __init__(self,
                name, recognised_times, matches_found,
                created, modified):
        self.name = name
        self.recognised_times = recognised_times
        self.matches_found = matches_found
        self.created = created
        self.modified = modified

    def json(self):
        return {
            'name': self.name,
            'recognised_times': self.recognised_times,
            'matches_found': self.matches_found,
            'created': self.created,
            'modified': self.modified,
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(_id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
