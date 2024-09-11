from datetime import datetime
from app import db


modDictUnits_NEWS = {}


modDictAss_NEWS = {}

''' top of page

modDictUnits_NEWS = {}  dictionary of all unit models   01 : [None, Mod1, Mod2, Mod3, Mod4]
modDictAss_NEWS = {}  dictionary of all assignment models  01 : Model

'''



class ChatBox_NEWS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, nullable=False)
    chat = db.Column(db.String)
    response = db.Column(db.String)
    learner_id = db.Column(db.Integer, db.ForeignKey('user.id')) # lower case becasue looking for table in database

    def __repr__(self):
        return f"ChatBox('{self.username}','{self.chat}','{self.response}')"
     # the foreignkey shows a db.relationship to User ID ('User' is the class whereas 'user' is the table name which would be lower case)

class Attendance_NEWS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, unique=True, nullable=False)
    studentID = db.Column(db.String(9), unique=True, nullable=False)
    attend = db.Column(db.String)
    teamnumber = db.Column(db.Integer)
    teamsize = db.Column(db.Integer)
    teamcount = db.Column(db.Integer)
    unit = db.Column(db.String(9))

class AttendLog_NEWS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, nullable=False)
    studentID = db.Column(db.String(9), nullable=False)
    attend = db.Column(db.String)
    teamnumber = db.Column(db.Integer)
    attScore = db.Column(db.Integer)
    extraStr = db.Column(db.String)
    extraInt = db.Column(db.Integer)


class Units_NEWS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String)
    u1 = db.Column(db.Integer)
    u2 = db.Column(db.Integer)
    u3 = db.Column(db.Integer)
    u4 = db.Column(db.Integer)
    uA = db.Column(db.Integer)

class Exams_NEWS(db.Model):
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

class Errors_NEWS(db.Model):
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

class U001U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)


class U002U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)

class U003U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)

class U004U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)


# remove after intro class

# print('Unit Filter', Units.query.filter_by(unit='00').first())



modDictUnits_NEWS['00']=[None]
modDictUnits_NEWS['00'].append(U001U_NEWS)
modDictUnits_NEWS['00'].append(U002U_NEWS)
modDictUnits_NEWS['00'].append(U003U_NEWS)
modDictUnits_NEWS['00'].append(U004U_NEWS)

########################################

class U011U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['01']=[None]
modDictUnits_NEWS['01'].append(U011U_NEWS)

class U012U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['01'].append(U012U_NEWS)

class U013U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['01'].append(U013U_NEWS)

class U014U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['01'].append(U014U_NEWS)



##########################################

class U021U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['02']=[None]
modDictUnits_NEWS['02'].append(U021U_NEWS)

class U022U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['02'].append(U022U_NEWS)

class U023U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['02'].append(U023U_NEWS)

class U024U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['02'].append(U024U_NEWS)


##########################################

class U031U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['03']=[None]
modDictUnits_NEWS['03'].append(U031U_NEWS)

class U032U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['03'].append(U032U_NEWS)

class U033U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['03'].append(U033U_NEWS)

class U034U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['03'].append(U034U_NEWS)

##########################################

class U041U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['04']=[None]
modDictUnits_NEWS['04'].append(U041U_NEWS)

class U042U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['04'].append(U042U_NEWS)

class U043U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['04'].append(U043U_NEWS)

class U044U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['04'].append(U044U_NEWS)


##########################################

class U051U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['05']=[None]
modDictUnits_NEWS['05'].append(U051U_NEWS)

class U052U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['05'].append(U052U_NEWS)

class U053U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['05'].append(U053U_NEWS)

class U054U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['05'].append(U054U_NEWS)



##########################################

class U061U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['06']=[None]
modDictUnits_NEWS['06'].append(U061U_NEWS)

class U062U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['06'].append(U062U_NEWS)

class U063U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['06'].append(U063U_NEWS)

class U064U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['06'].append(U064U_NEWS)


##########################################

class U071U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['07']=[None]
modDictUnits_NEWS['07'].append(U071U_NEWS)

class U072U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['07'].append(U072U_NEWS)

class U073U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['07'].append(U073U_NEWS)

class U074U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['07'].append(U074U_NEWS)


##########################################

class U081U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['08']=[None]
modDictUnits_NEWS['08'].append(U081U_NEWS)

class U082U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['08'].append(U082U_NEWS)

class U083U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['08'].append(U083U_NEWS)

class U084U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['08'].append(U084U_NEWS)

class U091U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['09']=[None]
modDictUnits_NEWS['09'].append(U091U_NEWS)

class U092U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['09'].append(U092U_NEWS)

class U093U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['09'].append(U093U_NEWS)

class U094U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['09'].append(U084U_NEWS)


class U101U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['10']=[None]
modDictUnits_NEWS['10'].append(U101U_NEWS)

class U102U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['10'].append(U102U_NEWS)

class U103U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['10'].append(U103U_NEWS)

class U104U_NEWS(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_NEWS['10'].append(U104U_NEWS)

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

class A00A_NEWS (BaseAss):
    id = db.Column(db.Integer, primary_key=True)


### remove after intro class
## intro edit

### recode UNIT 00
modDictAss_NEWS['00'] = A00A_NEWS
# print('MOD ASS NEWS 00')

class A01A_NEWS (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_NEWS['01'] = A01A_NEWS

class A02A_NEWS (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_NEWS['02'] = A02A_NEWS

class A03A_NEWS (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_NEWS['03'] = A03A_NEWS

class A04A_NEWS (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_NEWS['04'] = A04A_NEWS

class A05A_NEWS (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_NEWS['05'] = A05A_NEWS

class A06A_NEWS (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_NEWS['06'] = A06A_NEWS

class A07A_NEWS (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_NEWS['07'] = A07A_NEWS

class A08A_NEWS (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_NEWS['08'] = A08A_NEWS


##############################################



