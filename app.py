from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('calc-imc.html')

@app.route('/resultado', methods=["GET"])
def calc_imc():
    nome = request.args.get("nome")
    altura = request.args.get("altura")
    peso = request.args.get("peso")

    # Verifica se todos os campos estão preenchidos
    if not altura or not peso or not nome:
        return render_template("resultado.html", mensagem="Preencha todos os campos corretamente!")

    try:
        altura = float(altura)
        peso = float(peso)
        # Calculando o IMC
        imc = round((peso / altura**2), 2)
    except ValueError:
        return render_template("resultado.html", mensagem="Valores inválidos! Insira números válidos para peso e altura.")

    # Categorizar o IMC
    if imc < 18.5:
        mensagem = "Você está abaixo do peso!"
    elif imc < 24.9:
        mensagem = "Você está com o peso normal!"
    elif imc < 29.9:
        mensagem = "Você está com sobrepeso!"
    else:
        mensagem = "Você está obeso!"

    return render_template("resultado.html", mensagem=mensagem, imc=imc)

if __name__ == '__main__':
    app.run(debug=True)