from datetime import datetime, timedelta
from app import app, db, login_manager
from flask_login import UserMixin, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


modDictUnits_PRON = {}
modDictAss_PRON = {}


''' top of page

modDictUnits_PRON = {}  dictionary of all unit models   01 : [None, Mod1, Mod2, Mod3, Mod4]
modDictAss_PRON = {}  dictionary of all assignment models  01 : Model

'''



class ChatBox_PRON(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, nullable=False)
    chat = db.Column(db.String)
    response = db.Column(db.String)
    learner_id = db.Column(db.Integer, db.ForeignKey('user.id')) # lower case becasue looking for table in database

    def __repr__(self):
        return f"ChatBox('{self.username}','{self.chat}','{self.response}')"
     # the foreignkey shows a db.relationship to User ID ('User' is the class whereas 'user' is the table name which would be lower case)

class Attendance_PRON(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, unique=True, nullable=False)
    studentID = db.Column(db.String(9), unique=True, nullable=False)
    attend = db.Column(db.String)
    teamnumber = db.Column(db.Integer)
    teamsize = db.Column(db.Integer)
    teamcount = db.Column(db.Integer)
    unit = db.Column(db.String(9))

class AttendLog_PRON(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, nullable=False)
    studentID = db.Column(db.String(9), nullable=False)
    attend = db.Column(db.String)
    teamnumber = db.Column(db.Integer)
    attScore = db.Column(db.Integer)
    extraStr = db.Column(db.String)
    extraInt = db.Column(db.Integer)


class Units_PRON(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String)
    u1 = db.Column(db.Integer)
    u2 = db.Column(db.Integer)
    u3 = db.Column(db.Integer)
    u4 = db.Column(db.Integer)
    uA = db.Column(db.Integer)

class Exams_PRON(db.Model):
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

class Errors_PRON(db.Model):
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

class U001U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)


class U002U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)

class U003U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)

class U004U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)


# remove after intro class

# print('Unit Filter', Units.query.filter_by(unit='00').first())



modDictUnits_PRON['00']=[None]
modDictUnits_PRON['00'].append(U001U_PRON)
modDictUnits_PRON['00'].append(U002U_PRON)
modDictUnits_PRON['00'].append(U003U_PRON)
modDictUnits_PRON['00'].append(U004U_PRON)

########################################

class U011U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['01']=[None]
modDictUnits_PRON['01'].append(U011U_PRON)

class U012U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['01'].append(U012U_PRON)

class U013U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['01'].append(U013U_PRON)

class U014U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['01'].append(U014U_PRON)



##########################################

class U021U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['02']=[None]
modDictUnits_PRON['02'].append(U021U_PRON)

class U022U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['02'].append(U022U_PRON)

class U023U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['02'].append(U023U_PRON)

class U024U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['02'].append(U024U_PRON)


##########################################

class U031U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['03']=[None]
modDictUnits_PRON['03'].append(U031U_PRON)

class U032U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['03'].append(U032U_PRON)

class U033U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['03'].append(U033U_PRON)

class U034U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['03'].append(U034U_PRON)

##########################################

class U041U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['04']=[None]
modDictUnits_PRON['04'].append(U041U_PRON)

class U042U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['04'].append(U042U_PRON)

class U043U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['04'].append(U043U_PRON)

class U044U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['04'].append(U044U_PRON)


##########################################

class U051U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['05']=[None]
modDictUnits_PRON['05'].append(U051U_PRON)

class U052U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['05'].append(U052U_PRON)

class U053U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['05'].append(U053U_PRON)

class U054U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['05'].append(U054U_PRON)



##########################################

class U061U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['06']=[None]
modDictUnits_PRON['06'].append(U061U_PRON)

class U062U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['06'].append(U062U_PRON)

class U063U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['06'].append(U063U_PRON)

class U064U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['06'].append(U064U_PRON)


##########################################

class U071U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['07']=[None]
modDictUnits_PRON['07'].append(U071U_PRON)

class U072U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['07'].append(U072U_PRON)

class U073U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['07'].append(U073U_PRON)

class U074U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['07'].append(U074U_PRON)


##########################################

class U081U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['08']=[None]
modDictUnits_PRON['08'].append(U081U_PRON)

class U082U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['08'].append(U082U_PRON)

class U083U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['08'].append(U083U_PRON)

class U084U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['08'].append(U084U_PRON)


##############################

class U091U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['09']=[None]
modDictUnits_PRON['09'].append(U091U_PRON)

class U092U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['09'].append(U092U_PRON)

class U093U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['09'].append(U093U_PRON)

class U094U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['09'].append(U094U_PRON)

class U101U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['10']=[None]
modDictUnits_PRON['10'].append(U101U_PRON)

class U102U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['10'].append(U102U_PRON)

class U103U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['10'].append(U103U_PRON)

class U104U_PRON(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_PRON['10'].append(U104U_PRON)

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

class A00A_PRON (BaseAss):
    id = db.Column(db.Integer, primary_key=True)


### remove after intro class
## intro edit

### recode UNIT 00
modDictAss_PRON['00'] = A00A_PRON
# print('MOD ASS FRD 00')

class A01A_PRON (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_PRON['01'] = A01A_PRON

class A02A_PRON (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_PRON['02'] = A02A_PRON

class A03A_PRON (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_PRON['03'] = A03A_PRON

class A04A_PRON (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_PRON['04'] = A04A_PRON

class A05A_PRON (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_PRON['05'] = A05A_PRON

class A06A_PRON (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_PRON['06'] = A06A_PRON

class A07A_PRON (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_PRON['07'] = A07A_PRON

class A08A_PRON (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_PRON['08'] = A08A_PRON


##############################################



