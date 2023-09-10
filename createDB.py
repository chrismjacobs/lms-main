
from app import db

from models import *
from aws import dbpassword
import json

def drop():
    db.drop_all()
    return False

drop()

db.create_all()

def main():
    #return False

    semester = str(2)
    ''' change jMaker global as well '''

    host = User(username='Chris',
                studentID='100000000',
                email='cjx02121981@gmail.com',
                image_file='profiles/Chris.jpg',
                password=dbpassword,
                device=json.dumps('{}'),
                semester=semester,
                icc=1,
                frd1=1,
                frd2=1,
                wpe1=1,
                wpe2=1,
                food=1,
                extra=10
                )
    db.session.add(host)
    db.session.commit()

    test = User(username='Test',
                studentID='100000001',
                email='test@gmail.com',
                image_file='profiles/default.PNG',
                password='Test0212',
                device='None'
                )
    db.session.add(test)
    db.session.commit()

    att = Attendance_FRD1(username='Chris', studentID='100000000', teamnumber=97, teamsize=4, teamcount=10, unit='RR')
    db.session.add(att)
    db.session.commit()

    att = AttendLog_FRD1(username='Chris', studentID='100000000')
    db.session.add(att)
    db.session.commit()

    att = Attendance_FRD2(username='Chris', studentID='100000000', teamnumber=97, teamsize=4, teamcount=10, unit='RR')
    db.session.add(att)
    db.session.commit()

    att = AttendLog_FRD2(username='Chris', studentID='100000000')
    db.session.add(att)
    db.session.commit()

    att = Attendance_WPE1(username='Chris', studentID='100000000', teamnumber=97, teamsize=4, teamcount=10, unit='RR')
    db.session.add(att)
    db.session.commit()

    att = AttendLog_WPE1(username='Chris', studentID='100000000')
    db.session.add(att)
    db.session.commit()

    att = Attendance_WPE2(username='Chris', studentID='100000000', teamnumber=97, teamsize=4, teamcount=10, unit='RR')
    db.session.add(att)
    db.session.commit()

    att = AttendLog_WPE2(username='Chris', studentID='100000000')
    db.session.add(att)
    db.session.commit()

    att = Attendance_ICC(username='Chris', studentID='100000000', teamnumber=97, teamsize=4, teamcount=10, unit='RR')
    db.session.add(att)
    db.session.commit()

    att = AttendLog_ICC(username='Chris', studentID='100000000')
    db.session.add(att)
    db.session.commit()

    att = Attendance_FOOD(username='Chris', studentID='100000000', teamnumber=97, teamsize=4, teamcount=10, unit='RR')
    db.session.add(att)
    db.session.commit()

    att = AttendLog_FOOD(username='Chris', studentID='100000000')
    db.session.add(att)
    db.session.commit()




action = main()