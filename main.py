from flask import Flask, render_template, request, redirect, session

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask('app')
app.config['SECRET_KEY'] = 'agend7842423423mod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class users(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  email = db.Column(db.String())
  password = db.Column(db.String())
  created_at = db.Column(db.String())
  updated_at = db.Column(db.String())

class contacts(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100))
  name = db.Column(db.String())
  email = db.Column(db.String())
  phone = db.Column(db.String())
  image = db.Column(db.String())
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  created_at = db.Column(db.String())
  updated_at = db.Column(db.String())
  

@app.route('/')
def index():
  if 'user_id' not in session:
    return redirect('/login')
    
  contact = contacts.query.all()
  return render_template(
    'index.html',
    contacts=contact
  )

@app.route('/create/', methods=['POST'])
def create():
  name = request.form.get('name')
  email = request.form.get('email')
  phone = request.form.get('phone')
  
  new_contacts = contacts(
    name=name,
    email=email,
    phone=phone
  )
  db.session.add(new_contacts)
  db.session.commit()
  return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
  name = request.form.get('name')
  email = request.form.get('email')
  phone = request.form.get('phone')

  contact = contacts.query.filter_by(id=id).first()
  contact.name = name
  contact.email = email
  contact.phone = phone
  db.session.commit()
  return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
  contact = contacts.query.filter_by(id=id).first()
  db.session.delete(contact)
  db.session.commit()
  return redirect('/')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/register')
def register():
  return render_template('register.html')

@app.route('/signup', methods=['POST'])
def signup():
  name_input = request.form.get('name')
  email_input = request.form.get('email')
  password_input= request.form.get('password')

  # Verificar se o e-mail já existe no DB!
  user = users.query.filter_by(email=email_input).first()
  if user:
    return redirect('/register')

  new_user = users (
    name=name_input,
    email=email_input,
    password=generate_password_hash(password_input)
  )
  
  db.session.add(new_user)
  db.session.commit()
  return redirect('/login')

@app.route('/signin', methods=['POST'])
def signin():
  email_input = request.form.get('email')
  password_input= request.form.get('password')

  # Verificar se existe um user com o e-mail
  user = users.query.filter_by(email=email_input).first()
  if not user:
    return redirect('/login')
    
  # Verificar se a senha está correta
  if not check_password_hash(user.password, password_input):
    return redirect('/login')

  # Guardar o user na sessão
  session['user_id'] = user.id
  return redirect('/')

@app.route('/logout')
def logout():
  session.pop('user_id', None)
  return redirect('/login')

if __name__ == '__main__':
  db.create_all()
  app.run(host='0.0.0.0', port=8080) 