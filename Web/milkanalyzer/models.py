from flask import current_app
from milkanalyzer import db, login_manager
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin

@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(20), nullable=False, default='defaultprofile.jpg')
    predictions = db.relationship('Prediction', backref='prediction_of', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_picture}')"    

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            id = s.loads(token)['id']
        except:
            return None
        return User.query.get(id)

class AIModel(db.Model):
    __tablename__ = 'aimodel'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(50), nullable=False)
    aimodel_picture = db.Column(db.String(20), nullable=False, default='defaultmodel.jpg')

    def __repr__(self):
        return f"AIModel('{self.name}', '{self.type}', '{self.aimodel_picture}')"

class Value(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    proportion = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    aimodel_id = db.Column(db.Integer, db.ForeignKey('aimodel.id'), nullable=False)

    def __repr__(self):
        return f"AIModel('{self.name}', '{self.proportion}')"

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_predicted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    prediction_file = db.Column(db.String(50), nullable=False, default='predictions.csv')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Prediction('{self.date_predicted}', '{self.user_id}')"