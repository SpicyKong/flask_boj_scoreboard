from main import db

class User(db.Model):
    __tablename__ = "user"
    
    # 기본키
    user_id = db.Column('ID', db.Integer, primary_key=True)

    username = db.Column('USERNAME', db.String(40), nullable = False)
    timestamp = db.Column('TIMESTAMP', db.Integer, nullable = False)
    
    def __init__(self, username, timestamp):
        self.username = username
        
        self.timestamp = timestamp
        
    def __str__(self):
        return 'User({}, {}, latest: {})'.format(self.user_id,self.username, str(self.timestamp))