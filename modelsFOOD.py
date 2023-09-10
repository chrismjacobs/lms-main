from datetime import datetime
from app import db


modDictUnits_FOOD = {}

modDictAss_FOOD = {}



''' top of page

modDictUnits_FOOD = {}  dictionary of all unit models   01 : [None, Mod1, Mod2, Mod3, Mod4]
modDictAss_FOOD = {}  dictionary of all assignment models  01 : Model

'''



class ChatBox_FOOD(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, nullable=False)
    chat = db.Column(db.String)
    response = db.Column(db.String)
    learner_id = db.Column(db.Integer, db.ForeignKey('user.id')) # lower case becasue looking for table in database

    def __repr__(self):
        return f"ChatBox('{self.username}','{self.chat}','{self.response}')"
     # the foreignkey shows a db.relationship to User ID ('User' is the class whereas 'user' is the table name which would be lower case)

class Attendance_FOOD(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, unique=True, nullable=False)
    studentID = db.Column(db.String(9), unique=True, nullable=False)
    attend = db.Column(db.String)
    teamnumber = db.Column(db.Integer)
    teamsize = db.Column(db.Integer)
    teamcount = db.Column(db.Integer)
    unit = db.Column(db.String(9))

class AttendLog_FOOD(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    username =  db.Column(db.String, nullable=False)
    studentID = db.Column(db.String(9), nullable=False)
    attend = db.Column(db.String)
    teamnumber = db.Column(db.Integer)
    attScore = db.Column(db.Integer)
    extraStr = db.Column(db.String)
    extraInt = db.Column(db.Integer)


class Units_FOOD(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String)
    u1 = db.Column(db.Integer)
    u2 = db.Column(db.Integer)
    u3 = db.Column(db.Integer)
    u4 = db.Column(db.Integer)
    uA = db.Column(db.Integer)

class Exams_FOOD(db.Model):
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

class Errors_FOOD(db.Model):
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

class U001U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)


class U002U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)

class U003U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)

class U004U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)


# remove after intro class

# print('Unit Filter', Units.query.filter_by(unit='00').first())



modDictUnits_FOOD['00']=[None]
modDictUnits_FOOD['00'].append(U001U_FOOD)
modDictUnits_FOOD['00'].append(U002U_FOOD)
modDictUnits_FOOD['00'].append(U003U_FOOD)
modDictUnits_FOOD['00'].append(U004U_FOOD)

########################################

class U011U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['01']=[None]
modDictUnits_FOOD['01'].append(U011U_FOOD)

class U012U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['01'].append(U012U_FOOD)

class U013U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['01'].append(U013U_FOOD)

class U014U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['01'].append(U014U_FOOD)



##########################################

class U021U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['02']=[None]
modDictUnits_FOOD['02'].append(U021U_FOOD)

class U022U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['02'].append(U022U_FOOD)

class U023U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['02'].append(U023U_FOOD)

class U024U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['02'].append(U024U_FOOD)


##########################################

class U031U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['03']=[None]
modDictUnits_FOOD['03'].append(U031U_FOOD)

class U032U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['03'].append(U032U_FOOD)

class U033U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['03'].append(U033U_FOOD)

class U034U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['03'].append(U034U_FOOD)

##########################################

class U041U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['04']=[None]
modDictUnits_FOOD['04'].append(U041U_FOOD)

class U042U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['04'].append(U042U_FOOD)

class U043U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['04'].append(U043U_FOOD)

class U044U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['04'].append(U044U_FOOD)


##########################################

class U051U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['05']=[None]
modDictUnits_FOOD['05'].append(U051U_FOOD)

class U052U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['05'].append(U052U_FOOD)

class U053U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['05'].append(U053U_FOOD)

class U054U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['05'].append(U054U_FOOD)



##########################################

class U061U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['06']=[None]
modDictUnits_FOOD['06'].append(U061U_FOOD)

class U062U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['06'].append(U062U_FOOD)

class U063U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['06'].append(U063U_FOOD)

class U064U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['06'].append(U064U_FOOD)


##########################################

class U071U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['07']=[None]
modDictUnits_FOOD['07'].append(U071U_FOOD)

class U072U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['07'].append(U072U_FOOD)

class U073U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['07'].append(U073U_FOOD)

class U074U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['07'].append(U074U_FOOD)


##########################################

class U081U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['08']=[None]
modDictUnits_FOOD['08'].append(U081U_FOOD)

class U082U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['08'].append(U082U_FOOD)

class U083U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['08'].append(U083U_FOOD)

class U084U_FOOD(BaseUnits):
    id = db.Column(db.Integer, primary_key=True)
modDictUnits_FOOD['08'].append(U084U_FOOD)


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

class A00A_FOOD (BaseAss):
    id = db.Column(db.Integer, primary_key=True)


### remove after intro class
## intro edit

### recode UNIT 00
modDictAss_FOOD['00'] = A00A_FOOD
# print('MOD ASS WPE 00')

class A01A_FOOD (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_FOOD['01'] = A01A_FOOD

class A02A_FOOD (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_FOOD['02'] = A02A_FOOD

class A03A_FOOD (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_FOOD['03'] = A03A_FOOD

class A04A_FOOD (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_FOOD['04'] = A04A_FOOD

class A05A_FOOD (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_FOOD['05'] = A05A_FOOD

class A06A_FOOD (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_FOOD['06'] = A06A_FOOD

class A07A_FOOD (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_FOOD['07'] = A07A_FOOD

class A08A_FOOD (BaseAss):
    id = db.Column(db.Integer, primary_key=True)
modDictAss_FOOD['08'] = A08A_FOOD


##############################################



