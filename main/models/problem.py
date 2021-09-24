from main import db
from main.models import User

class Problem(db.Model):
    __tablename__ = "problem"
    
    # 기본키
    problem_id = db.Column('ID', db.Integer, primary_key=True)
    user_id =  db.Column('USER_ID', db.ForeignKey('user.ID', ondelete='CASCADE'), nullable = False)
    user = db.relationship('User', backref=db.backref('utop', cascade='all, delete-orphan'))
    boj_id = db.Column('B_ID', db.Integer, nullable = False)
    
    def __init__(self, user_id, boj_id):
        self.user_id = user_id
        self.boj_id = boj_id
        
    def __str__(self):
        return 'Problem({}, {})'.format(User.query.get(self.user_id).username, str(self.boj_id))