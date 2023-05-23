from flask import *
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import uuid  # for public id
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs
import os
from dotenv.main import load_dotenv
from flask_recaptcha import ReCaptcha
import requests


def create_mail_body(token):
    base = os.path.dirname(os.path.abspath(__file__))+"/templates/"
    html = open(os.path.join(base, 'template.html'))
    soup = bs(html, 'html.parser')

    link = soup.find('a')
    link['href'] = "http://127.0.0.1:5000/user?token="+token

    return str(soup)


load_dotenv()

app = Flask(__name__)

captchaSiteKey = os.environ['CAPTCHA_SITE_KEY']
captchaSecretKey = os.environ['CAPTCHA_SECRET_KEY']
app.config.update({'RECAPTCHA_ENABLED': True,
                   'RECAPTCHA_SITE_KEY':
                   captchaSiteKey,
                   'RECAPTCHA_SECRET_KEY':
                   captchaSecretKey})


recaptcha = ReCaptcha(app=app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
# Generated App Password for the email
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
hashingAlgorithm = os.environ['HASHING_ALGORITHM']

db = SQLAlchemy(app)
mail = Mail(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(70), unique=True)


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/send_mail", methods=['post'])
def send_mail(**kwargs):
    if request.method == 'POST':
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                          data={'secret':
                                '6LcwpCwmAAAAAKa3NaVIRjyNSterQfA4ETZ_ltK8',
                                'response':
                                request.form['g-recaptcha-response']})

        google_response = json.loads(r.text)
        print('JSON: ', google_response)

        if google_response['success']:
            print('SUCCESS')
            email = request.form['email'].strip()
            sub = 'Test email'
            admin = os.environ['MAIL_USERNAME']

            user = User.query\
                .filter_by(email=email)\
                .first()
            if not user:
                # database ORM object
                user = User(
                    public_id=str(uuid.uuid4()),
                    email=email,
                )
                db.session.add(user)
                db.session.commit()

            token = jwt.encode({
                'public_id': user.public_id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'], hashingAlgorithm)

            mailBody = create_mail_body(token)
            message = Message(subject=sub, sender=admin,
                              recipients=email.split(), html=mailBody)
            mail.send(message)
            return render_template("Submit.html")

        else:
            # FAILED
            print('FAILED')
            return render_template('home.html')


@app.route('/user', methods=['GET'])
def get_all_users():
    args = request.args
    token = args.get('token')
    data = jwt.decode(token, app.config['SECRET_KEY'], hashingAlgorithm)

    users = User.query.all()
    output = []
    for user in users:
        output.append({
            'email': user.email
        })
    return jsonify({'users': output})


if __name__ == '__main__':
    app.run()
