from flask import Flask, render_template
import random

app = Flask(__name__, template_folder ="siteciencia/templates", static_folder = "siteciencia/static")


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
