from main import db
from main.models import User

class Week_board(db.Model):
    __tablename__ = "week_board"
    
    # 기본키
    board_id = db.Column('ID', db.Integer, primary_key=True, nullable = False)
    user_id =  db.Column('USER_ID', db.ForeignKey('user.ID', ondelete='CASCADE'), nullable = False)
    user = db.relationship('User', backref=db.backref('tables', cascade='all, delete-orphan'))
    week = db.Column('WEEK', db.Integer, nullable = False)
    mon = db.Column('MON', db.Integer, nullable = False)
    tue = db.Column('TUE', db.Integer, nullable = False)
    wed = db.Column('WED', db.Integer, nullable = False)
    thu = db.Column('THU', db.Integer, nullable = False)
    fri = db.Column('FRI', db.Integer, nullable = False)
    sat = db.Column('SAT', db.Integer, nullable = False)
    sun = db.Column('SUN', db.Integer, nullable = False)
    total = db.Column('TOTAL', db.Integer, nullable = False)
    
    def __init__(self, user_id, week):
        self.user_id = user_id
        self.week = week
        self.mon = 0
        self.tue = 0
        self.wed = 0
        self.thu = 0
        self.fri = 0
        self.sat = 0
        self.sun = 0
        self.total = 0

    def __str__(self):
        return "Week_board({}님의 {}주차, {}, {}, {}, {}, {}, {}, {} | {})".format(User.query.get(self.user_id).username, self.week, str(self.mon), str(self.tue), str(self.wed), str(self.thu), str(self.fri), str(self.sat), str(self.sun), str(self.total))
    
    def update(self, day, num):
        # is this 최선?
        """
        test = [self.mon, self.tue, self.wed, self.thu, self.fri, self.sat, self.sun][day]
        print(id(self.mon))
        print(id(test))
        test+=1
        print(test)
        self.mon+=1
        print(self.mon)
        #[self.mon, self.tue, self.wed, self.thu, self.fri, self.sat, self.sun][day]+=num
        #self.tue+=1
        #print([self.mon, self.tue, self.wed, self.thu, self.fri, self.sat, self.sun][day]=num)
        #print(day, num)
        #print(id([self.mon, self.tue, self.wed, self.thu, self.fri, self.sat, self.sun][day]))
        """
        if day==0:
            self.mon += num
        elif day==1:
            self.tue += num
        elif day==2:
            self.wed += num
        elif day==3:
            self.thu += num
        elif day==4:
            self.fri += num
        elif day==5:
            self.sat += num
        else:
            self.sun += num
        self.total += num
    def get_info(self):
        return [self.mon, self.thu, self.wed, self.thu, self.fri, self.sat, self.sun, self.total]
"""
str(self.mon), str(self.tue), str(self.wed), str(self.thu), str(self.fri), str(self.sat), str(self.sun), str(self.total)
from main.models import User, Week_board
from main import db
user = User.query.get(1)
week = Week_board.query.filter(Week_board.user_id == user.user_id).first()
week.update(0, 2)
        """