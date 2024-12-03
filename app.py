from flask import Flask, render_template
import random
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime as dt
import os 

app = Flask(__name__, template_folder ="siteciencia/templates", static_folder = "siteciencia/static")

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "cd.sqlite")


app.config["SQLALCHEMY_DATABASE_URI"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
  id= db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(200), nullable=False)
  date_time = db.Column(db. DateTime, default=dt.now)
  def __repr__(self):
    return f"Task: #{self.id}, description: {self.description}"
  
class Frase(db.Model):
  id= db.Column(db.Integer, primary_key=True)
  frase = db.Column(db.String(500), nullable=False)
  autor = db.Column(db.String(50), nullable=False)
  def __repr__(self):
    return f"Frase: #{self.id}, autor: {self.description}"



@app.route("/")
def index():
  return render_template("index.html")


@app.route("/analise", defaults={'usuario':'Visitante'})
@app.route("/analise/<usuario>")
def analise(usuario):
  return render_template("analise.html", usuario=usuario)


@app.route('/estatistica') 
def estatistica(): 
  return render_template('estatistica.html') 


@app.route('/programacao') 
def programacao(): 
  return render_template('programacao.html')

@app.route("/galeria")
def galeria():
  numeros = random.sample(range(1, 26), 15)
  lista_imagens = [f"{num}.jpg" for num in numeros]
  return render_template("galeria.html", imagens=lista_imagens)



if __name__ == "__main__":
  app.run(debug=True, port=5001)
