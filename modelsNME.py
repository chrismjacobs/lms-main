from datetime import datetime, timedelta
from app import app, db, login_manager
from flask_login import UserMixin, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# verify token
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from meta import BaseConfig

modDictUnits_NME = {}
modDictAss_NME = {}



''' top of page

modDictUnits_NME = {}  dictionary of all unit models   01 : [None, Mod1, Mod2, Mod3, Mod4]
modDictAss_NME = {}  dictionary of all assignment models  01 : Model

'''



class ChatBox_NME(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, nullable=False)
    chat = db.Column(db.String)
    response = db.Column(db.String)
    learner_id = db.Column(db.Integer, db.ForeignKey('user.id')) # lower case becasue looking for table in database

    def __repr__(self):
        return f"ChatBox('{self.username}','{self.chat}','{self.response}')"
     # the foreignkey shows a db.relationship to User ID ('User' is the class whereas 'user' is the table name which would be lower case)

class Attendance_NME(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, unique=True, nullable=False)
    studentID = db.Column(db.String(9), unique=True, nullable=False)
    attend = db.Column(db.String)
    teamnumber = db.Column(db.Integer)
    teamsize = db.Column(db.Integer)
    teamcount = db.Column(db.Integer)
    unit = db.Column(db.String(9))

class AttendLog_NME(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, nullable=False)
    studentID = db.Column(db.String(9), nullable=False)
    attend = db.Column(db.String)
    teamnumber = db.Column(db.Integer)
    attScore = db.Column(db.Integer)
    extraStr = db.Column(db.String)
    extraInt = db.Column(db.Integer)


class Units_NME(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String)
    u1 = db.Column(db.Integer)
    u2 = db.Column(db.Integer)
    u3 = db.Column(db.Integer)
    u4 = db.Column(db.Integer)
    uA = db.Column(db.Integer)

class Exams_NME(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    j1 = db.Column(db.String)
    j2 = db.Column(db.String)
    j3 = db.Column(db.String)
    j4 = db.Column(db.String)
    j5 = db.Column(db.String)
    j6 = db.Column(db.String)
    j7 = db.Column(db.String)
    j8 = db.Column(db.String)

class Errors_NME(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #date_added = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String)
    err = db.Column(db.String)
    device = db.Column(db.String)
    mode = db.Column(db.String)
    unit = db.Column(db.String)




############### UNIT MODELS ###################################

class BaseUnits(db.Model):
    __abstract__ = True
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String)
    teamnumber = db.Column(db.Integer, unique=True)
    Ans01 = db.Column(db.String)
    Ans02 = db.Column(db.String)
    Ans03 = db.Column(db.String)
    Ans04 = db.Column(db.String)
    Ans05 = db.Column(db.String)
    Ans06 = db.Column(db.String)
    Ans07 = db.Column(db.String)
    Ans08 = db.Column(db.String)
    Ans09 = db.Column(db.String)
    Grade = db.Column(db.Integer)
    Comment = db.Column(db.String)

class U001U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)


class U002U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)

class U003U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)

class U004U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)


# remove after intro class

# print('Unit Filter', Units.query.filter_by(unit='00').first())



modDictUnits_NME['00']=[None]
modDictUnits_NME['00'].append(U001U_NME)
modDictUnits_NME['00'].append(U002U_NME)
modDictUnits_NME['00'].append(U003U_NME)
modDictUnits_NME['00'].append(U004U_NME)

########################################

class U011U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['01']=[None]
modDictUnits_NME['01'].append(U011U_NME)

class U012U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['01'].append(U012U_NME)

class U013U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['01'].append(U013U_NME)

class U014U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['01'].append(U014U_NME)



##########################################

class U021U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['02']=[None]
modDictUnits_NME['02'].append(U021U_NME)

class U022U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['02'].append(U022U_NME)

class U023U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['02'].append(U023U_NME)

class U024U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['02'].append(U024U_NME)


##########################################

class U031U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['03']=[None]
modDictUnits_NME['03'].append(U031U_NME)

class U032U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['03'].append(U032U_NME)

class U033U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['03'].append(U033U_NME)

class U034U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['03'].append(U034U_NME)

##########################################

class U041U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['04']=[None]
modDictUnits_NME['04'].append(U041U_NME)

class U042U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['04'].append(U042U_NME)

class U043U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['04'].append(U043U_NME)

class U044U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['04'].append(U044U_NME)


##########################################

class U051U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['05']=[None]
modDictUnits_NME['05'].append(U051U_NME)

class U052U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['05'].append(U052U_NME)

class U053U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['05'].append(U053U_NME)

class U054U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['05'].append(U054U_NME)



##########################################

class U061U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['06']=[None]
modDictUnits_NME['06'].append(U061U_NME)

class U062U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['06'].append(U062U_NME)

class U063U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['06'].append(U063U_NME)

class U064U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['06'].append(U064U_NME)


##########################################

class U071U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['07']=[None]
modDictUnits_NME['07'].append(U071U_NME)

class U072U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['07'].append(U072U_NME)

class U073U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['07'].append(U073U_NME)

class U074U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['07'].append(U074U_NME)


##########################################

class U081U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['08']=[None]
modDictUnits_NME['08'].append(U081U_NME)

class U082U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['08'].append(U082U_NME)

class U083U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['08'].append(U083U_NME)

class U084U_NME(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NME['08'].append(U084U_NME)


############### ASSIGNMENT MODELS ###################################

class BaseAss(db.Model):
    __abstract__ = True
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String(300))
    AudioDataOne = db.Column(db.String)
    LengthOne = db.Column(db.Integer)
    AudioDataTwo = db.Column(db.String)
    LengthTwo = db.Column(db.Integer)
    Notes = db.Column(db.String)
    TextOne = db.Column(db.String)
    TextTwo = db.Column(db.String)
    DateStart= db.Column(db.DateTime)
    Grade = db.Column(db.Integer)
    Comment = db.Column(db.String)

class A00A_NME (BaseAss):
    id = db.Column(db.Integer, primary_key=True)


### remove after intro class
## intro edit

### recode UNIT 00
modDictAss_NME['00'] = A00A_NME
# print('MOD ASS FRD 00')

class A01A_NME (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_NME['01'] = A01A_NME

class A02A_NME (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_NME['02'] = A02A_NME

class A03A_NME (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_NME['03'] = A03A_NME

class A04A_NME (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_NME['04'] = A04A_NME

class A05A_NME (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_NME['05'] = A05A_NME

class A06A_NME (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_NME['06'] = A06A_NME

class A07A_NME (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_NME['07'] = A07A_NME

class A08A_NME (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_NME['08'] = A08A_NME


##############################################



