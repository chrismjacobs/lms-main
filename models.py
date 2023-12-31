from datetime import datetime, timedelta
# from http.client import UNSUPPORTED_MEDIA_TYPE
# from msilib import AMD64
from app import app, db, login_manager
from flask_login import UserMixin, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# verify token
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from meta import *
from modelsFRD1 import *
from modelsFRD2 import *
from modelsICC import *
from modelsWPE1 import *
from modelsWPE2 import *
from modelsFOOD import *

# from modelsWRITE import *
# from modelsNME import *
# from modelsPENG import *
# from modelsLNC import *

def getSchema():
    SCHEMA = 0
    try:
        SCHEMA = int(current_user.schema)
    except:
        SCHEMA = 0

    return SCHEMA

dicts = {
        1 : [
            ChatBox_FRD1,
            Attendance_FRD1,
            AttendLog_FRD1,
            Units_FRD1,
            Exams_FRD1,
            Errors_FRD1,
        ],
        2 : [
            ChatBox_FRD2,
            Attendance_FRD2,
            AttendLog_FRD2,
            Units_FRD2,
            Exams_FRD2,
            Errors_FRD2,
        ],
        3 : [
            ChatBox_WPE1,
            Attendance_WPE1,
            AttendLog_WPE1,
            Units_WPE1,
            Exams_WPE1,
            Errors_WPE1,
        ],
        4 : [
            ChatBox_WPE2,
            Attendance_WPE2,
            AttendLog_WPE2,
            Units_WPE2,
            Exams_WPE2,
            Errors_WPE2,
        ],
        5 : [
            ChatBox_FOOD,
            Attendance_FOOD,
            AttendLog_FOOD,
            Units_FOOD,
            Exams_FOOD,
            Errors_FOOD,
        ],
        6 : [
            ChatBox_ICC,
            Attendance_ICC,
            AttendLog_ICC,
            Units_ICC,
            Exams_ICC,
            Errors_ICC,
        ],
    }

infoDict = {
        'mda' : [{},
                 modDictAss_FRD1,
                 modDictAss_FRD2,
                 modDictAss_WPE1,
                 modDictAss_WPE2,
                 modDictAss_FOOD,
                 modDictAss_ICC
                 ],
        'mdu' : [{},
                 modDictUnits_FRD1,
                 modDictUnits_FRD2,
                 modDictUnits_WPE1,
                 modDictUnits_WPE2,
                 modDictUnits_FOOD,
                 modDictUnits_ICC
                 ]
    }

def getModels():
    SCHEMA = getSchema()
    # print('getModels', SCHEMA)



    chatbox = [None]
    attend = [None]
    attl = [None]
    units = [None]
    exams = [None]
    errors = [None]

    for d in dicts:
        chatbox.append(dicts[d][0])
        attend.append(dicts[d][1])
        attl.append(dicts[d][2])
        units.append(dicts[d][3])
        exams.append(dicts[d][4])
        errors.append(dicts[d][5])

    return {
        'ChatBox_' : chatbox[SCHEMA],
        'Attendance_' : attend[SCHEMA],
        'AttendLog_' : attl[SCHEMA],
        'Units_' : units[SCHEMA],
        'Exams_' : exams[SCHEMA],
        'Errors_' : errors[SCHEMA]
    }

def getInfo():
    SCHEMA = getSchema()


    modDictAss  = infoDict['mda'][SCHEMA]
    modDictUnits = infoDict['mdu'][SCHEMA]

    #print('mod dict ass', modDictAss)
    #print('mod dict units', modDictUnits)


    """the problem with 00 is somewhere in this code"""
    """just delete the code allows 00 unit to be used"""
    """need to check if it can be used like this for midterm or not"""

    if getModels()['Units_'] and not getModels()['Units_'].query.filter_by(unit='00').first():
        try:
            print('try delete 00')
            del modDictUnits['00']
            del modDictAss['00']
        except:
            print('delete 00 fail')
    else:
        print('NO UNIT 00')



    # print('infoDict', SCHEMA, modDictUnits) #modDictAss, zeroDictAss, zeroDictUnits

    # used for admin rendering
    listAss = []
    for elements in modDictAss.values():
        listAss.append(elements)

    listUnits = []
    for elements in modDictUnits.values():
        # print('elements', elements, modDictUnits.values())
        for item in elements:
            if item != None:
                listUnits.append(item)

    # zeroAss = []
    # for elements in zeroDictAss.values():
    #     zeroAss.append(elements)

    # zeroUnits = []
    # for elements in zeroDictUnits.values():
    #     for item in elements:
    #         if item != None:
    #             zeroUnits.append(item)

    return {
        'aModsDict' : modDictAss,
        'uModsDict' : modDictUnits,
        'unit_mods_list' : listUnits,
        'ass_mods_list' : listAss,
    }





#login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), unique=True, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now)
    studentID = db.Column(db.String(9), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(), nullable=False, default='profiles/default.PNG')
    password = db.Column(db.String(60), nullable=False)
    device = db.Column (db.String(), nullable=False)
    frd1 = db.Column(db.Integer, default=0)
    frd2 = db.Column(db.Integer, default=0)
    wpe1 = db.Column(db.Integer, default=0)
    wpe2 = db.Column(db.Integer, default=0)
    food = db.Column(db.Integer, default=0)
    icc = db.Column(db.Integer, default=0)
    # app = db.Column(db.Integer, default=0)
    # vtm = db.Column(db.Integer, default=0)
    # png = db.Column(db.Integer, default=0)
    semester = db.Column(db.Integer)
    schema = db.Column(db.Integer)
    extra = db.Column(db.Integer)
    condition = db.Column(db.Integer, default=0)
    info = db.Column(db.String(), default='')


    def get_reset_token(self, expires_sec=1800):
        expires_sec = 1800
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod #tell python not to expect that self parameter as an argument, just accepting the token
    def verify_reset_token(token):
        expires_sec = 1800
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):  # double underscore method or dunder method, marks the data, this is how it is printed
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Users(db.Model): #import the model
    id = db.Column(db.Integer, primary_key=True) #kind of value and the key unique to the user
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String(20), nullable=False) #must be a unique name and cannot be null
    email = db.Column(db.String(120), unique=True, nullable=False)
    studentID = db.Column(db.String(20))
    vocab = db.Column(db.String(), nullable=False, default='generalW')
    password = db.Column(db.String(60), nullable=False)
    school = db.Column(db.String(30))
    classroom = db.Column(db.String(20))
    extraStr = db.Column(db.String())
    extraInfo = db.Column(db.String())
    extraInt = db.Column(db.Integer())


class MyModelView(ModelView):
    def is_accessible(self):
        if BaseConfig.DEBUG == True:
            return True
        elif current_user.is_authenticated:
            if current_user.id == 1 or current_user.id == 2:
                return True
            else:
                return False
        else:
            return False

#https://danidee10.github.io/2016/11/14/flask-by-example-7.html



admin = Admin(app, 'Example: Layout-BS3', base_template='admin.html', template_mode='bootstrap3')



admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Users, db.session))

mList1 = []

for d in dicts:
    mList1.append(dicts[d][1])
for d in dicts:
    mList1.append(dicts[d][2])
for d in dicts:
    mList1.append(dicts[d][3])
for d in dicts:
    mList1.append(dicts[d][4])

for m in mList1:
    # print(m, type(m))
    admin.add_view(MyModelView(m, db.session))


mList2 = []
mList3 = []


for mda in infoDict['mda']:
    if infoDict['mda'].index(mda) > 0:
        # print(mda)
        mList2.append(mda)
for mdu in infoDict['mdu']:
    if infoDict['mdu'].index(mdu) > 0:
        # print(mdu)
        mList3.append(mda)

# for s in mList3:
#     print('MDU', s)
#     for d in s:
#         print('D', d)
#         if s[d]:
#             admin.add_view(MyModelView(s[d], db.session))


### PARTICIPATION

### U01

admin.add_view(MyModelView(U011U_FRD1, db.session))
admin.add_view(MyModelView(U012U_FRD1, db.session))
admin.add_view(MyModelView(U013U_FRD1, db.session))
admin.add_view(MyModelView(U014U_FRD1, db.session))

admin.add_view(MyModelView(U011U_FRD2, db.session))
admin.add_view(MyModelView(U012U_FRD2, db.session))
admin.add_view(MyModelView(U013U_FRD2, db.session))
admin.add_view(MyModelView(U014U_FRD2, db.session))

admin.add_view(MyModelView(U011U_WPE1, db.session))
admin.add_view(MyModelView(U012U_WPE1, db.session))
admin.add_view(MyModelView(U013U_WPE1, db.session))
admin.add_view(MyModelView(U014U_WPE1, db.session))

admin.add_view(MyModelView(U011U_WPE2, db.session))
admin.add_view(MyModelView(U012U_WPE2, db.session))
admin.add_view(MyModelView(U013U_WPE2, db.session))
admin.add_view(MyModelView(U014U_WPE2, db.session))

admin.add_view(MyModelView(U011U_ICC, db.session))
admin.add_view(MyModelView(U012U_ICC, db.session))
admin.add_view(MyModelView(U013U_ICC, db.session))
admin.add_view(MyModelView(U014U_ICC, db.session))

##### U02

admin.add_view(MyModelView(U021U_FRD1, db.session))
admin.add_view(MyModelView(U022U_FRD1, db.session))
admin.add_view(MyModelView(U023U_FRD1, db.session))
admin.add_view(MyModelView(U024U_FRD1, db.session))

admin.add_view(MyModelView(U021U_FRD2, db.session))
admin.add_view(MyModelView(U022U_FRD2, db.session))
admin.add_view(MyModelView(U023U_FRD2, db.session))
admin.add_view(MyModelView(U024U_FRD2, db.session))

admin.add_view(MyModelView(U021U_WPE1, db.session))
admin.add_view(MyModelView(U022U_WPE1, db.session))
admin.add_view(MyModelView(U023U_WPE1, db.session))
admin.add_view(MyModelView(U024U_WPE1, db.session))

admin.add_view(MyModelView(U021U_WPE2, db.session))
admin.add_view(MyModelView(U022U_WPE2, db.session))
admin.add_view(MyModelView(U023U_WPE2, db.session))
admin.add_view(MyModelView(U024U_WPE2, db.session))

admin.add_view(MyModelView(U021U_ICC, db.session))
admin.add_view(MyModelView(U022U_ICC, db.session))
admin.add_view(MyModelView(U023U_ICC, db.session))
admin.add_view(MyModelView(U024U_ICC, db.session))

## U03
admin.add_view(MyModelView(U031U_FRD1, db.session))
admin.add_view(MyModelView(U032U_FRD1, db.session))
admin.add_view(MyModelView(U033U_FRD1, db.session))
admin.add_view(MyModelView(U034U_FRD1, db.session))

admin.add_view(MyModelView(U031U_FRD2, db.session))
admin.add_view(MyModelView(U032U_FRD2, db.session))
admin.add_view(MyModelView(U033U_FRD2, db.session))
admin.add_view(MyModelView(U034U_FRD2, db.session))

admin.add_view(MyModelView(U031U_WPE1, db.session))
admin.add_view(MyModelView(U032U_WPE1, db.session))
admin.add_view(MyModelView(U033U_WPE1, db.session))
admin.add_view(MyModelView(U034U_WPE1, db.session))

admin.add_view(MyModelView(U031U_WPE2, db.session))
admin.add_view(MyModelView(U032U_WPE2, db.session))
admin.add_view(MyModelView(U033U_WPE2, db.session))
admin.add_view(MyModelView(U034U_WPE2, db.session))

admin.add_view(MyModelView(U031U_ICC, db.session))
admin.add_view(MyModelView(U032U_ICC, db.session))
admin.add_view(MyModelView(U033U_ICC, db.session))
admin.add_view(MyModelView(U034U_ICC, db.session))

## U04
admin.add_view(MyModelView(U041U_FRD1, db.session))
admin.add_view(MyModelView(U042U_FRD1, db.session))
admin.add_view(MyModelView(U043U_FRD1, db.session))
admin.add_view(MyModelView(U044U_FRD1, db.session))

admin.add_view(MyModelView(U041U_FRD2, db.session))
admin.add_view(MyModelView(U042U_FRD2, db.session))
admin.add_view(MyModelView(U043U_FRD2, db.session))
admin.add_view(MyModelView(U044U_FRD2, db.session))

admin.add_view(MyModelView(U041U_WPE1, db.session))
admin.add_view(MyModelView(U042U_WPE1, db.session))
admin.add_view(MyModelView(U043U_WPE1, db.session))
admin.add_view(MyModelView(U044U_WPE1, db.session))

admin.add_view(MyModelView(U041U_WPE2, db.session))
admin.add_view(MyModelView(U042U_WPE2, db.session))
admin.add_view(MyModelView(U043U_WPE2, db.session))
admin.add_view(MyModelView(U044U_WPE2, db.session))

admin.add_view(MyModelView(U041U_ICC, db.session))
admin.add_view(MyModelView(U042U_ICC, db.session))
admin.add_view(MyModelView(U043U_ICC, db.session))
admin.add_view(MyModelView(U044U_ICC, db.session))

## ICC
admin.add_view(MyModelView(U051U_ICC, db.session))
admin.add_view(MyModelView(U052U_ICC, db.session))
admin.add_view(MyModelView(U053U_ICC, db.session))
admin.add_view(MyModelView(U054U_ICC, db.session))







admin.add_view(MyModelView(A01A_FRD1, db.session))
admin.add_view(MyModelView(A01A_FRD2, db.session))
admin.add_view(MyModelView(A01A_WPE1, db.session))
admin.add_view(MyModelView(A01A_WPE2, db.session))
admin.add_view(MyModelView(A01A_ICC, db.session))

admin.add_view(MyModelView(A02A_FRD1, db.session))
admin.add_view(MyModelView(A02A_FRD2, db.session))
admin.add_view(MyModelView(A02A_WPE1, db.session))
admin.add_view(MyModelView(A02A_WPE2, db.session))
admin.add_view(MyModelView(A02A_ICC, db.session))

admin.add_view(MyModelView(A03A_FRD1, db.session))
admin.add_view(MyModelView(A03A_FRD2, db.session))
admin.add_view(MyModelView(A03A_WPE1, db.session))
admin.add_view(MyModelView(A03A_WPE2, db.session))
admin.add_view(MyModelView(A03A_ICC, db.session))

admin.add_view(MyModelView(A04A_FRD1, db.session))
admin.add_view(MyModelView(A04A_FRD2, db.session))
admin.add_view(MyModelView(A04A_WPE1, db.session))
admin.add_view(MyModelView(A04A_WPE2, db.session))
admin.add_view(MyModelView(A04A_ICC, db.session))
admin.add_view(MyModelView(A05A_ICC, db.session))



# for d in mList2:
#     for x in d:
#         admin.add_view(MyModelView(d[x], db.session))


# mList4 = [
#             ChatBox_FRD, ChatBox_WPE, ChatBox_VTM, ChatBox_PENG, ChatBox_WRITE, ChatBox_NME,   #ChatBox_ICC, ChatBox_LNC,
#             Errors_FRD, Errors_WPE, Errors_VTM, Errors_PENG, Errors_WRITE, Errors_NME,    #Errors_ICC, Errors_LNC,
#          ]

# for m in mList4:
#     admin.add_view(MyModelView(m, db.session))








