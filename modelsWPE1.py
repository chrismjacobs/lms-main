from datetime import datetime
from app import db


# verify token
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from meta import BaseConfig

modDictUnits_WPE1 = {}


modDictAss_WPE1 = {}



''' top of page

modDictUnits_WPE1 = {}  dictionary of all unit models   01 : [None, Mod1, Mod2, Mod3, Mod4]
modDictAss_WPE1 = {}  dictionary of all assignment models  01 : Model

'''



class ChatBox_WPE1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, nullable=False)
    chat = db.Column(db.String)
    response = db.Column(db.String)
    learner_id = db.Column(db.Integer, db.ForeignKey('user.id')) # lower case becasue looking for table in database

    def __repr__(self):
        return f"ChatBox('{self.username}','{self.chat}','{self.response}')"
     # the foreignkey shows a db.relationship to User ID ('User' is the class whereas 'user' is the table name which would be lower case)

class Attendance_WPE1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, unique=True, nullable=False)
    studentID = db.Column(db.String(9), unique=True, nullable=False)
    attend = db.Column(db.String)
    teamnumber = db.Column(db.Integer)
    teamsize = db.Column(db.Integer)
    teamcount = db.Column(db.Integer)
    unit = db.Column(db.String(9))

class AttendLog_WPE1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, nullable=False)
    studentID = db.Column(db.String(9), nullable=False)
    attend = db.Column(db.String)
    teamnumber = db.Column(db.Integer)
    attScore = db.Column(db.Integer)
    extraStr = db.Column(db.String)
    extraInt = db.Column(db.Integer)


class Units_WPE1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String)
    u1 = db.Column(db.Integer)
    u2 = db.Column(db.Integer)
    u3 = db.Column(db.Integer)
    u4 = db.Column(db.Integer)
    uA = db.Column(db.Integer)

class Exams_WPE1(db.Model):
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

class Errors_WPE1(db.Model):
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
    Grade = db.Column(db.Integer)
    Comment = db.Column(db.String)

class U001U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)


class U002U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)

class U003U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)

class U004U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)


# remove after intro class

# print('Unit Filter', Units.query.filter_by(unit='00').first())



modDictUnits_WPE1['00']=[None]
modDictUnits_WPE1['00'].append(U001U_WPE1)
modDictUnits_WPE1['00'].append(U002U_WPE1)
modDictUnits_WPE1['00'].append(U003U_WPE1)
modDictUnits_WPE1['00'].append(U004U_WPE1)

########################################

class U011U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['01']=[None]
modDictUnits_WPE1['01'].append(U011U_WPE1)

class U012U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['01'].append(U012U_WPE1)

class U013U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['01'].append(U013U_WPE1)

class U014U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['01'].append(U014U_WPE1)



##########################################

class U021U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['02']=[None]
modDictUnits_WPE1['02'].append(U021U_WPE1)

class U022U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['02'].append(U022U_WPE1)

class U023U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['02'].append(U023U_WPE1)

class U024U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['02'].append(U024U_WPE1)


##########################################

class U031U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['03']=[None]
modDictUnits_WPE1['03'].append(U031U_WPE1)

class U032U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['03'].append(U032U_WPE1)

class U033U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['03'].append(U033U_WPE1)

class U034U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['03'].append(U034U_WPE1)

##########################################

class U041U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['04']=[None]
modDictUnits_WPE1['04'].append(U041U_WPE1)

class U042U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['04'].append(U042U_WPE1)

class U043U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['04'].append(U043U_WPE1)

class U044U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['04'].append(U044U_WPE1)


##########################################

class U051U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['05']=[None]
modDictUnits_WPE1['05'].append(U051U_WPE1)

class U052U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['05'].append(U052U_WPE1)

class U053U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['05'].append(U053U_WPE1)

class U054U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['05'].append(U054U_WPE1)



##########################################

class U061U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['06']=[None]
modDictUnits_WPE1['06'].append(U061U_WPE1)

class U062U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['06'].append(U062U_WPE1)

class U063U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['06'].append(U063U_WPE1)

class U064U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['06'].append(U064U_WPE1)


##########################################

class U071U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['07']=[None]
modDictUnits_WPE1['07'].append(U071U_WPE1)

class U072U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['07'].append(U072U_WPE1)

class U073U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['07'].append(U073U_WPE1)

class U074U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['07'].append(U074U_WPE1)


##########################################

class U081U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['08']=[None]
modDictUnits_WPE1['08'].append(U081U_WPE1)

class U082U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['08'].append(U082U_WPE1)

class U083U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['08'].append(U083U_WPE1)

class U084U_WPE1(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE1['08'].append(U084U_WPE1)


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

class A00A_WPE1 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)


### remove after intro class
## intro edit

### recode UNIT 00
modDictAss_WPE1['00'] = A00A_WPE1
# print('MOD ASS WPE 00')

class A01A_WPE1 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_WPE1['01'] = A01A_WPE1

class A02A_WPE1 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_WPE1['02'] = A02A_WPE1

class A03A_WPE1 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_WPE1['03'] = A03A_WPE1

class A04A_WPE1 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_WPE1['04'] = A04A_WPE1

class A05A_WPE1 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_WPE1['05'] = A05A_WPE1

class A06A_WPE1 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_WPE1['06'] = A06A_WPE1

class A07A_WPE1 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_WPE1['07'] = A07A_WPE1

class A08A_WPE1 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_WPE1['08'] = A08A_WPE1


##############################################



