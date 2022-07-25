from app import db


class Fact(db.Model):
    __tablename__ = "fact"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    subject_url = db.Column(db.String, nullable=False)
    subject_id = db.Column(db.String, nullable=False)

    predicate_url = db.Column(db.String, nullable=False)
    predicate_id = db.Column(db.String, nullable=False)

    object_url = db.Column(db.String, nullable=False)
    object_id = db.Column(db.String, nullable=False)

    source_url = db.Column(db.String, nullable=False)

    object_label = db.Column(db.String, nullable=False)
    confidence_reader = db.Column(db.Float, nullable=False)
    feedback = db.Column(db.Integer, nullable=False, default=-1)  # -1: no feedback, 0: wrong, 1: correct
