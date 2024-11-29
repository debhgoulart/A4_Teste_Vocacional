from flask import Flask, render_template, request
from pyswip import Prolog
import json

app = Flask(__name__)

# Carrega as perguntas do arquivo JSON
with open("perguntas.json", encoding='utf-8') as f:
    perguntas = json.load(f)

# Inicializa o Prolog
prolog = Prolog()

# Carrega a base de conhecimento no Prolog (simplificado)
carreiras = [
    ("administracao", 10, 30),
    ("artes_cenicas", 31, 50),
    ("arquitetura", 51, 70),
    ("ciencia_da_computacao", 71, 90),
    ("ciencias_biologicas", 91, 110),
    ("design_grafico", 111, 130),
    ("direito", 131, 150),
    ("economia", 151, 170),
    ("educacao_fisica", 171, 180),
    ("engenharia", 181, 200),
    ("jornalismo", 201, 220),
    ("letras", 221, 240),
    ("marketing", 241, 260),
    ("medicina", 261, 280),
    ("medicina_veterinaria", 281, 300),
    ("psicologia", 301, 320),
    ("relacoes_internacionais", 321, 340)
]

# Adiciona os fatos de carreira no Prolog
for carreira, min_pontos, max_pontos in carreiras:
    prolog.assertz(f"carreira({carreira}, {min_pontos}, {max_pontos})")

# Regra para encontrar a carreira
prolog.assertz("""
encontrar_carreira(Pontos, Carreira) :-
    carreira(Carreira, Min, Max),
    Pontos >= Min,
    Pontos =< Max.
""")

@app.route('/')
def inicial():
    return render_template('inicial.html')

@app.route('/questionario')
def questionario():
    # Renderiza a página de questionário com as perguntas do JSON
    return render_template('questionario.html', perguntas=perguntas["perguntas"])

@app.route('/resultado', methods=['POST'])
def resultado():
    pontuacao_total = 0
    respostas_invalidas = []

    # Processa as respostas do formulário
    for i in range(len(perguntas["perguntas"])):
        resposta = request.form.get(f'pergunta_{i}')
        if resposta and resposta.isdigit() and int(resposta) in [1, 2, 3]:
            pontuacao_total += int(resposta)
        else:
            respostas_invalidas.append(i + 1)

    # Caso haja respostas inválidas, mostra uma mensagem de erro
    if respostas_invalidas:
        return f"As perguntas {', '.join(map(str, respostas_invalidas))} contêm respostas inválidas. Por favor, corrija."

    # Consulta o Prolog para encontrar a carreira
    resultado_prolog = list(prolog.query(f"encontrar_carreira({pontuacao_total}, Carreira)"))
    if resultado_prolog:
        carreira = resultado_prolog[0]['Carreira']
        mensagem = f"Com base na sua pontuação ({pontuacao_total}), a carreira sugerida é: {carreira.replace('_', ' ').capitalize()}."
    else:
        mensagem = f"Não foi possível determinar uma carreira com base na pontuação total: {pontuacao_total}."

    # Renderiza a página de resultado
    return render_template('resultado.html', mensagem=mensagem)

if __name__ == '__main__':
    app.run(debug=True)
