
from modelsWPE1 import U011U_WPE1, U051U_WPE1, U012U_WPE1, U052U_WPE1, U013U_WPE1, U053U_WPE1, U014U_WPE1, U054U_WPE1
from app import db

for x in U012U_WPE1.query.all():
    print(x.username)
    entry = U052U_WPE1(
                username =  x.username,
                teamnumber = x.teamnumber,
                Ans01 = x.Ans01,
                Ans02 = x.Ans02,
                Ans03 = x.Ans03,
                Ans04 = x.Ans04,
                Ans05 = x.Ans05,
                Ans06 = x.Ans06,
                Ans07 = x.Ans07,
                Ans08 = x.Ans08,
                Grade = x.Grade,
                Comment = x.Comment
    )
    db.session.add(entry)
    db.session.commit()