from my_conf import db


class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.LargeBinary)
    filename = db.Column(db.String)
    time_to_die = db.Column(db.DATETIME)
