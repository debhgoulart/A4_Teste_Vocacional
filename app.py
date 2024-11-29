from flask import Flask, render_template, request
from pyswip import Prolog

app = Flask(__name__)

#Perguntas
perguntas = [
    ("Qual é o seu nível de interesse em entender e apoiar as necessidades emocionais dos outros?", [
        ("1 - Costumo focar mais nas minhas próprias necessidades.", 1),
        ("2 - Procuro entender os outros quando necessário, mas sem priorizar.", 2),
        ("3 - Tenho grande interesse em compreender e apoiar os outros.", 3),
    ]),
    ("Como você se sente em relação à competição com outras pessoas no ambiente de trabalho?", [
        ("Prefiro trabalhar sem a pressão de competir.", 1),
        ("Competir é algo que faço quando a situação exige.", 2),
        ("Adoro competir e sempre procuro superar os outros.", 3),
    ]), 
    ("O quanto você prefere ter liberdade para decidir como executar suas tarefas?", [
        ("Prefiro seguir orientações claras.", 1),
        ("Gosto de autonomia em algumas áreas.", 2),
        ("Prefiro ter total autonomia.", 3),
    ]),
    ("Como você se sente em relação ao trabalho em equipe e à colaboração?", [
        ("Prefiro trabalhar de forma independente, sem muita colaboração.", 1),
        ("Gosto de colaborar, mas também valorizo minha autonomia.", 2),
        ("Considero a colaboração essencial para atingir os melhores resultados.", 3),
    ]),
    ("Quão confortável você se sente em situações onde pode focar em atividades individuais?", [
        ("Prefiro ambientes com mais interação social.", 1),
        ("Consigo trabalhar sozinho, mas gosto de momentos de interação.", 2),
        ("Sinto-me mais confortável em atividades realizadas individualmente.", 3),
    ]),
    ("Com que frequência você prefere atividades que envolvem interação constante com outras pessoas?", [
        ("Prefiro atividades mais solitárias, com pouca interação social.", 1),
        ("Gosto de um equilíbrio entre interação social e atividades solitárias.", 2),
        ("Prefiro atividades com muita interação e contato social.", 3),
    ]),
    ("Como você lida com tarefas que exigem precisão e cumprimento de prazos?", [
       ("Prefiro fazer as tarefas no meu ritmo, mesmo que tome mais tempo.", 1),
       ("Faço o possível para ser eficiente, mas sem comprometer a qualidade.", 2),
       ("Priorizo cumprir as tarefas com rapidez e eficácia acima de tudo.", 3),
    ]),
    ("Quando enfrenta um problema, qual é o seu estilo para encontrar soluções?", [
        ("Prefiro seguir métodos testados e conhecidos.", 1),
        ("Busco novas ideias, mas também considero métodos tradicionais.", 2),
        ("Gosto de experimentar soluções inovadoras e criativas.", 3),
    ]),
    ("Qual é sua prioridade ao definir metas para um projeto?", [
        ("Dou mais valor a metas que tragam satisfação e realização pessoal.", 1),
        ("Considero o impacto financeiro, mas busco equilíbrio com outros valores.", 2),
        ("Minhas prioridades são maximizar os ganhos e reduzir custos.", 3),
    ]),
    ("Como você vê o impacto de suas ações no bem-estar dos outros?", [
        ("Me concentro mais nos meus objetivos e no que é necessário para alcançá-los.", 1),
        ("Procuro equilibrar meus objetivos com ações que tragam benefício aos outros.", 2),
        ("Acredito que minhas ações devem sempre considerar o impacto positivo nas pessoas.", 3),
    ]),
    ("Quando você toma decisões, como lida com o novo e o desconhecido?", [
        ("Prefiro manter métodos e práticas já conhecidas.", 1),
        ("Gosto de evoluir aos poucos, testando novas opções.", 2),
        ("Estou aberto a experimentar e explorar novas ideias e práticas.", 3),
    ]),
    ("Com que frequência você busca criar novas formas de resolver problemas?", [
        ("Costumo me manter dentro das práticas já estabelecidas.", 1),
        ("Gosto de inovar, mas também considero métodos conhecidos.", 2),
        ("Sempre busco novas abordagens e soluções criativas para problemas.", 3),
    ]),
    ("Como você se sente em relação a ambientes que exigem constantes mudanças?", [
        ("Prefiro ambientes estáveis e com poucas mudanças.", 1),
        ("Aprecio um equilíbrio entre estabilidade e mudanças ocasionais.", 2),
        ("Me sinto confortável em ambientes que exigem constante adaptação e mudanças.", 3),
    ]),
    ("Qual é sua disposição para mudar seus planos ou rotinas quando surgem imprevistos?", [
        ("Prefiro seguir meus planos e evitar mudanças.", 1),
        ("Consigo ajustar meus planos quando necessário, mas não gosto de mudanças frequentes.", 2),
        ("Adoro a flexibilidade de mudar planos e rotinas sempre que necessário.", 3),
    ]),
    ("Como você se sente em relação ao trabalho com cálculos e questões técnicas?", [
        ("Prefiro evitar situações que envolvem cálculos ou problemas técnicos.", 1),
        ("Consigo lidar com cálculos e questões técnicas, mas não sou tão entusiasta.", 2),
        ("Gosto muito de trabalhar com cálculos e questões técnicas, sempre me aprofundando nas soluções.", 3),
    ]),
    ("Quão confortável você se sente com temas e atividades ligadas à sociedade e à cultura?", [
        ("Não tenho muito interesse por questões sociais ou comportamentais.", 1),
        ("Até gosto, mas não é o que mais me motiva.", 2),
        ("Sou muito interessado em entender o comportamento humano e as interações sociais.", 3),
    ]),
    ("Qual é o seu nível de interesse por áreas que estudam os organismos vivos, como medicina, biologia ou ecologia?", [
        ("Não tenho interesse em estudar organismos vivos e os processos biológicos que os envolvem.", 1),
        ("Tenho um interesse por biologia e ciências da vida, mas não é uma área que me motiva a me aprofundar.", 2),
        ("Tenho um grande interesse por biologia e ciências naturais.", 3),
    ]),
    ("Como você costuma abordar a resolução de problemas complexos?", [
        ("Prefiro soluções simples, sem me aprofundar muito nos detalhes.", 1),
        ("Consigo lidar com problemas complexos, mas prefiro não me aprofundar em todos os detalhes.", 2),
        ("Adoro analisar problemas complexos e resolver quebra-cabeças, explorando todos os detalhes e soluções possíveis.", 3),
    ]),
    ("Quando você enfrenta situações inesperadas ou mudanças rápidas, como você costuma reagir?", [
        ("Costumo ficar hesitante e gosto de ter tempo para planejar antes de agir.", 1),
        ("Tento avaliar rapidamente as situações, mas ainda prefiro ponderar antes de tomar decisões.", 2),
        ("Reajo de forma rápida e impulsiva, adaptando-me facilmente às mudanças.", 3),
    ]),
    ("Qual é o seu nível de envolvimento com atividades e estudos mais acadêmicos e teóricos?", [
        ("Prefiro evitar atividades acadêmicas ou estudos teóricos e me foco mais na prática.", 1),
        ("Eu me envolvo com atividades acadêmicas de forma equilibrada, mas não é o meu foco principal.", 2),
        ("Tenho grande interesse em atividades acadêmicas e teóricas, especialmente aquelas que aprofundam o conhecimento.", 3),
    ]),
    ("Como você costuma tomar decisões em situações desafiadoras ou complexas?", [
        ("Prefiro agir com base em ideias ou teorias, mesmo que não tenha certeza da aplicação prática.", 1),
        ("Tento equilibrar teorias e práticas, mas prefiro uma solução mais prática e direta.", 2),
        ("Busco sempre soluções práticas e eficazes, focando em resultados tangíveis.", 3),
    ]),
]


@app.route('/')
def index():
    return render_template('questionario.html', perguntas=enumerate(perguntas))

#envia requisição
@app.route('/resultado', methods=['POST'])
def resultado():
    pontuacao_total = 0
    for i in range(len(perguntas)):
        resposta = request.form.get(f'pergunta_{i}')
        if resposta:
            pontuacao_total += int(resposta)
    
    return f'Pontuação total: {pontuacao_total}'

if __name__ == '__main__':
    app.run(debug=True)