from cardination import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Patient.query.get(int(user_id))

class Patient(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)



    def __repr__(self):
        return f"Patient('{self.username}', '{self.email}', '{self.image_file}')"

class Doctor(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)

    def __repr__(self):
        return f"Doctor('{self.username}', '{self.email}', '{self.image_file}')"


class PatientRecords(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20), unique = False, nullable = False)
    age  = db.Column(db.Integer, unique = False, nullable = True)
    cholestrol = db.Column(db.Integer, unique = False, nullable = True)
    glucose = db.Column(db.Integer, unique = False, nullable = True)
    bp = db.Column(db.Integer, unique = False, nullable = True)
    skin = db.Column(db.Integer, unique = False, nullable = True)
    insulin = db.Column(db.Integer, unique = False, nullable = True)
    bmi = db.Column(db.Integer, unique = False, nullable = True)
    pedi = db.Column(db.Integer, unique = False, nullable = True)
    pregnancies = db.Column(db.Integer, unique = False, nullable = True)

    def __repr__(self):
        return f"PatientRecord('{self.username}', '{self.cholestrol}', '{self.glucose}','{self.bp}', '{self.skin}', '{self.insulin}','{self.bmi}', '{self.pedi}', '{self.pregnancies}')"