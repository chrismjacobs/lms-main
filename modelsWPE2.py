from datetime import datetime
from app import db


modDictUnits_WPE2 = {}


modDictAss_WPE2 = {}



''' top of page

modDictUnits_WPE2 = {}  dictionary of all unit models   01 : [None, Mod1, Mod2, Mod3, Mod4]
modDictAss_WPE2 = {}  dictionary of all assignment models  01 : Model

'''



class ChatBox_WPE2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, nullable=False)
    chat = db.Column(db.String)
    response = db.Column(db.String)
    learner_id = db.Column(db.Integer, db.ForeignKey('user.id')) # lower case becasue looking for table in database

    def __repr__(self):
        return f"ChatBox('{self.username}','{self.chat}','{self.response}')"
     # the foreignkey shows a db.relationship to User ID ('User' is the class whereas 'user' is the table name which would be lower case)

class Attendance_WPE2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, unique=True, nullable=False)
    studentID = db.Column(db.String(9), unique=True, nullable=False)
    attend = db.Column(db.String)
    teamnumber = db.Column(db.Integer)
    teamsize = db.Column(db.Integer)
    teamcount = db.Column(db.Integer)
    unit = db.Column(db.String(9))

class AttendLog_WPE2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, nullable=False)
    studentID = db.Column(db.String(9), nullable=False)
    attend = db.Column(db.String)
    teamnumber = db.Column(db.Integer)
    attScore = db.Column(db.Integer)
    extraStr = db.Column(db.String)
    extraInt = db.Column(db.Integer)


class Units_WPE2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String)
    u1 = db.Column(db.Integer)
    u2 = db.Column(db.Integer)
    u3 = db.Column(db.Integer)
    u4 = db.Column(db.Integer)
    uA = db.Column(db.Integer)

class Exams_WPE2(db.Model):
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

class Errors_WPE2(db.Model):
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

class U001U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)


class U002U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)

class U003U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)

class U004U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)


# remove after intro class

# print('Unit Filter', Units.query.filter_by(unit='00').first())



modDictUnits_WPE2['00']=[None]
modDictUnits_WPE2['00'].append(U001U_WPE2)
modDictUnits_WPE2['00'].append(U002U_WPE2)
modDictUnits_WPE2['00'].append(U003U_WPE2)
modDictUnits_WPE2['00'].append(U004U_WPE2)

########################################

class U011U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['01']=[None]
modDictUnits_WPE2['01'].append(U011U_WPE2)

class U012U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['01'].append(U012U_WPE2)

class U013U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['01'].append(U013U_WPE2)

class U014U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['01'].append(U014U_WPE2)



##########################################

class U021U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['02']=[None]
modDictUnits_WPE2['02'].append(U021U_WPE2)

class U022U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['02'].append(U022U_WPE2)

class U023U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['02'].append(U023U_WPE2)

class U024U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['02'].append(U024U_WPE2)


##########################################

class U031U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['03']=[None]
modDictUnits_WPE2['03'].append(U031U_WPE2)

class U032U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['03'].append(U032U_WPE2)

class U033U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['03'].append(U033U_WPE2)

class U034U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['03'].append(U034U_WPE2)

##########################################

class U041U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['04']=[None]
modDictUnits_WPE2['04'].append(U041U_WPE2)

class U042U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['04'].append(U042U_WPE2)

class U043U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['04'].append(U043U_WPE2)

class U044U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['04'].append(U044U_WPE2)


##########################################

class U051U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['05']=[None]
modDictUnits_WPE2['05'].append(U051U_WPE2)

class U052U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['05'].append(U052U_WPE2)

class U053U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['05'].append(U053U_WPE2)

class U054U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['05'].append(U054U_WPE2)



##########################################

class U061U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['06']=[None]
modDictUnits_WPE2['06'].append(U061U_WPE2)

class U062U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['06'].append(U062U_WPE2)

class U063U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['06'].append(U063U_WPE2)

class U064U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['06'].append(U064U_WPE2)


##########################################

class U071U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['07']=[None]
modDictUnits_WPE2['07'].append(U071U_WPE2)

class U072U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['07'].append(U072U_WPE2)

class U073U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['07'].append(U073U_WPE2)

class U074U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['07'].append(U074U_WPE2)


##########################################

class U081U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['08']=[None]
modDictUnits_WPE2['08'].append(U081U_WPE2)

class U082U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['08'].append(U082U_WPE2)

class U083U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['08'].append(U083U_WPE2)

class U084U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['08'].append(U084U_WPE2)

class U091U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['09']=[None]
modDictUnits_WPE2['09'].append(U091U_WPE2)

class U092U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['09'].append(U092U_WPE2)

class U093U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['09'].append(U093U_WPE2)

class U094U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['09'].append(U084U_WPE2)


class U101U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['10']=[None]
modDictUnits_WPE2['10'].append(U101U_WPE2)

class U102U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['10'].append(U102U_WPE2)

class U103U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['10'].append(U103U_WPE2)

class U104U_WPE2(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_WPE2['10'].append(U104U_WPE2)

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

class A00A_WPE2 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)


### remove after intro class
## intro edit

### recode UNIT 00
modDictAss_WPE2['00'] = A00A_WPE2
# print('MOD ASS WPE2 00')

class A01A_WPE2 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_WPE2['01'] = A01A_WPE2

class A02A_WPE2 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_WPE2['02'] = A02A_WPE2

class A03A_WPE2 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_WPE2['03'] = A03A_WPE2

class A04A_WPE2 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_WPE2['04'] = A04A_WPE2

class A05A_WPE2 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_WPE2['05'] = A05A_WPE2

class A06A_WPE2 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_WPE2['06'] = A06A_WPE2

class A07A_WPE2 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_WPE2['07'] = A07A_WPE2

class A08A_WPE2 (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_WPE2['08'] = A08A_WPE2


##############################################



