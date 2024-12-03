from flask import Flask, render_template, request, redirect
from datetime import datetime as dt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random
import os

app = Flask(__name__, template_folder ="siteciencia/templates", static_folder = "siteciencia/static")

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "cd.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(200), nullable=False)
  date_created = db.Column(db.DateTime, default=dt.now())
  def __repr__(self):
    return  f"Task: #{self.id}, description: {self.description}"

class Frase(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  frase = db.Column(db.String(500), nullable=False)
  autor = db.Column(db.String(100), default='Anônimo')
  def __repr__(self):
    return  f"Frase: #{self.id}, autor: {self.autor}, frase: {self.frase}"

@app.route("/")
def index():
  # return "<h1>Bom dia, professor.</h1>"
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


@app.route("/tarefas", methods=['POST', 'GET'])
def tarefas():
  if request.method == "POST":
    task = Task(description=request.form["description"])
    try:
      db.session.add(task)
      db.session.commit()
      return redirect("/tarefas")
    except:
      return "Houve um erro ao inserir a tarefa"
  else:
    tasks = Task.query.order_by(Task.date_created).all()
    return render_template("tarefas.html", tasks=tasks)


@app.route("/tarefas/delete/<int:id>")
def tarefasDelete(id):
  task = Task.query.get_or_404(id)
  try:
    db.session.delete(task)
    db.session.commit()
    return redirect("/tarefas")
  except:
    return "Houve um problema na remoção da tarefa"


@app.route("/tarefas/update/<int:id>", methods=['POST', 'GET'])
def tarefasUpdate(id):
  task = Task.query.get_or_404(id)
  if request.method == "POST":
    task.description = request.form["description"]
    try:
      db.session.commit()
      return redirect("/tarefas")
    except:
      return "Houve um erro ao atualizar a tarefa"
  else:
    return render_template("tarefas-update.html", task=task)


@app.route("/frases", defaults={'nome':''})
@app.route("/frases/<nome>", methods=['GET'])
def frases(nome):
  if not nome: 
    nome = request.args.get('nome', '')
  frases = Frase.query.all()
  aleatoria = random.choice(frases) if frases else None
  return render_template("frases.html", nome=nome, frase=aleatoria)


@app.route("/frases/adm", methods=['POST', 'GET'])
def frasesAdm():
  if request.method == "POST":
    fr = request.form["frase"]
    at = request.form["autor"]
    if at == "":
      at = "Anônimo"
    frase = Frase(frase=fr, autor=at)
    try:
      db.session.add(frase)
      db.session.commit()
      return redirect("/frases/adm")
    except:
      return "Houve um erro ao inserir a frase"
  else:
      frases = Frase.query.order_by(Frase.autor).all()
      return render_template("frases-adm.html", frases=frases)



@app.route("/frases/update/<int:id>", methods=['POST', 'GET'])
def frasesUpdate(id):
  frase = Frase.query.get_or_404(id)
  if request.method == "POST":
    frase.frase = request.form["frase"]
    frase.autor = request.form["autor"]
    try:
      db.session.commit()
      return redirect("/frases/adm")
    except:
      return "Houve um erro ao atualizar a tarefa"
  else:
    return render_template("frases-update.html", frase=frase)


@app.route("/frases/delete/<int:id>")
def frasesDelete(id):
  frase = Frase.query.get_or_404(id)
  try:
    db.session.delete(frase)
    db.session.commit()
    return redirect("/frases/adm")
  except:
    return "Houve um problema na remoção da tarefa"


if __name__ == "__main__":
  with app.app_context():
    db.create_all()
  app.run(debug=True, port=5001)
