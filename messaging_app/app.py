from flask import Flask ,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db  = SQLAlchemy(app)

@app.route('/',methods = ['POST','GET'])
def home():
    if request.method == 'POST':
        message_sender  = request.form['sender']
        message_content = request.form['content']
        new_message = Message_Class(sender=message_sender,message=message_content)
        try:
            db.session.add(new_message)
            db.session.commit()
            return redirect('/')
        except:
            return"We ran into a problem"
    else:
        messages = Message_Class.query.order_by(Message_Class.id)
        return render_template('home.html', messages=messages)

class Message_Class(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    sender  = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    time    = db.Column(db.DateTime,default= datetime.utcnow)
    def __repr__(self):
        return '<Entry %r>' % self.id


if __name__ == "__main__":
    app.run(debug=True)
