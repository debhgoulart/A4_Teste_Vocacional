from flask import Flask, render_template, request
from pyswip import Prolog
import json
import os

app = Flask(__name__)

with open("perguntas.json", encoding='utf-8') as f:
    perguntas = json.load(f)

prolog = Prolog()

prolog.consult("carreiras.pl")

carreiras_path = os.path.join(os.path.dirname(__file__), "carreiras.pl").replace("\\", "/")

print(f"Caminho do arquivo Prolog: {carreiras_path}")

try:
    prolog.consult(carreiras_path)
except Exception as e:
    print(f"Erro ao carregar o arquivo: {e}")

#frases resultado
frases_carreira = {
    "administracao": ("A Administração oferece uma ampla gama de oportunidades em diversos setores. Profissionais dessa área têm a capacidade de liderar, organizar e planejar operações de negócios, sendo essenciais para o crescimento das empresas. A carreira oferece estabilidade e boas perspectivas de crescimento, com possibilidades de atuar em gestão de equipes, finanças, marketing, recursos humanos e logística.","\n1- Gestor de Projetos\n2- Analista Financeiro\n3- Consultor Empresarial\n4- Administrador de Recursos Humanos\n5- Empreendedor."),
    "artes_cenicas": ("Optar por Artes Cênicas permite expressar criatividade e explorar a comunicação por meio da atuação, dança e teatro. É uma área que envolve constante aprendizado e desenvolvimento pessoal, além de proporcionar uma carreira apaixonante para quem deseja impactar o público. A diversidade de projetos e o trabalho em equipe tornam essa carreira enriquecedora, com oportunidades tanto no palco quanto nos bastidores.","\n1- Ator\n2- Diretor de Teatro\n3- Coreógrafo\n4- Professor de Artes\n5- Produtor Cultural."),
    "arquitetura": ("A arquitetura é uma profissão que combina criatividade, design e ciência. Ao escolher essa área, você terá a oportunidade de criar espaços que influenciam diretamente o dia a dia das pessoas, como edifícios, casas e urbanismo. A carreira oferece uma grande satisfação pessoal por meio do impacto visual e funcional das construções e uma boa perspectiva de remuneração. Além disso, a flexibilidade para atuar tanto em grandes empresas quanto em projetos independentes é um dos grandes benefícios dessa área.","Principais Carreiras:\n1- Arquiteto de Interiores\n2- Urbanista\n3- Paisagista\n4- Arquiteto Sustentável\n5- Gerente de Projetos Arquitetônicos."),
    "ciencia_da_computacao": ("Ciência da Computação é uma carreira com altíssima demanda no mercado, devido à constante evolução tecnológica. Profissionais dessa área são responsáveis por criar, analisar e melhorar sistemas, programas e aplicativos, impactando todos os aspectos da sociedade moderna. A área oferece alta empregabilidade, bons salários e a oportunidade de trabalhar com inovações como inteligência artificial, big data e segurança cibernética. Se você gosta de resolução de problemas e desafios técnicos, essa é uma escolha excelente.","Principais Carreiras:\n1- Desenvolvedor de Software\n2- Cientista de Dados\n3- Engenheiro de Machine Learning\n4- Analista de Segurança Cibernética\n5- Administrador de Redes."),
    "ciencias_biologicas": ("Escolher Ciências Biológicas significa contribuir para o entendimento da vida e dos ecossistemas, além de impactar positivamente a saúde pública e o meio ambiente. Com essa formação, você pode atuar em áreas como pesquisa, biotecnologia, conservação ambiental e medicina. A carreira oferece tanto satisfação intelectual, ao realizar descobertas científicas, quanto a oportunidade de trabalhar em diferentes setores, como educação, saúde e indústria farmacêutica.","Principais Carreiras:\n1- Biólogo Ambiental\n2- Geneticista\n3- Microbiologista\n4- Ecologista\n5- Pesquisador em Biotecnologia."),
    "design_grafico": ("O Design Gráfico é ideal para quem tem uma mente criativa e deseja trabalhar com comunicação visual. Profissionais dessa área podem atuar em publicidade, branding, marketing digital, criação de layouts, websites e até em produções cinematográficas. A carreira oferece grande flexibilidade de atuação, com a possibilidade de trabalhar como freelancer ou em grandes empresas, além de possibilitar o trabalho em diversas indústrias criativas.",
    "Principais Carreiras:\n1- Designer de Interfaces (UI/UX)\n2- Ilustrador\n3- Diretor de Arte\n4- Animador Digital\n5- Designer Editorial."),
    "direito": ("O Direito é uma das profissões mais tradicionais e respeitadas, com grande capacidade de gerar impacto social e pessoal. Ao escolher essa área, você tem a possibilidade de atuar em diferentes áreas, como direito civil, penal, corporativo, ambiental ou internacional. A carreira oferece alta remuneração, segurança e uma grande diversidade de oportunidades, além de ser fundamental para a manutenção da justiça e dos direitos humanos na sociedade.",
    "Principais Carreiras:\n1- Advogado Corporativo\n2- Promotor de Justiça\n3- Juiz\n4- Consultor Jurídico\n5- Especialista em Propriedade Intelectual."),
    "economia": ("A Economia é uma área estratégica que envolve análise de mercado, finanças, políticas públicas e tomada de decisões empresariais. Profissionais dessa área ajudam a criar soluções para problemas econômicos e sociais e podem atuar em setores como consultoria, bancos, governo e grandes empresas. A profissão oferece excelentes perspectivas de crescimento, altos salários e uma carreira desafiadora e recompensadora.","Principais Carreiras:\n1- Economista Financeiro\n2- Consultor de Investimentos\n3- Analista de Políticas Públicas\n4- Pesquisador Econômico\n5- Gerente de Riscos."),
    "educacao_fisica": ("A Educação Física é uma área voltada para a promoção da saúde e do bem-estar das pessoas. Profissionais dessa área podem atuar em diversos contextos, como academias, escolas, clubes esportivos e até em clínicas de reabilitação. Além de ser uma profissão com alta demanda por educadores e treinadores, ela também oferece a oportunidade de realizar um trabalho significativo na vida das pessoas, ajudando-as a melhorar sua qualidade de vida e a saúde física e mental.","Principais Carreiras:\n1- Personal Trainer\n2- Preparador Físico\n3- Professor de Educação Física Escolar\n4- Fisiologista do Exercício\n5- Treinador Esportivo."),
    "engenharia": ("Engenharia é uma das áreas mais dinâmicas e desafiadoras, com uma vasta gama de especializações, como civil, elétrica, mecânica, ambiental e de software. Profissionais da área são responsáveis por projetar e implementar soluções técnicas para problemas complexos, impactando diretamente a infraestrutura e o desenvolvimento tecnológico. A carreira oferece ótimas perspectivas de salários e crescimento, com a oportunidade de trabalhar em projetos inovadores e em diferentes partes do mundo.",
    "Principais Carreiras:\n1- Engenheiro Civil\n2- Engenheiro Elétrico\n3- Engenheiro Mecânico\n4- Engenheiro de Software\n5- Engenheiro Ambiental."),
    "jornalismo": ("O Jornalismo é uma carreira de grande relevância social, com o objetivo de informar e educar o público. Profissionais dessa área atuam na cobertura de eventos, produção de conteúdo jornalístico e análise crítica de fatos. A profissão oferece a oportunidade de trabalhar em diferentes meios de comunicação, como rádio, TV, impressos e mídias digitais, além de proporcionar uma carreira emocionante e dinâmica, com a chance de ser uma voz ativa na sociedade.",
    "Principais Carreiras:\n1- Repórter Investigativo\n2- Apresentador de Televisão\n3- Editor de Conteúdo\n4- Jornalista Multimídia\n5- Correspondente Internacional."),
    "letras": ("Letras é a escolha ideal para quem tem paixão pela linguagem e pela literatura. Com essa formação, você pode se tornar professor de línguas, tradutor, revisor ou trabalhar na área editorial. Além disso, é possível atuar em pesquisa literária e em atividades de criação, como roteiros e conteúdo digital. A carreira é enriquecedora para quem busca uma conexão profunda com as palavras e a comunicação.",
    "Principais Carreiras:\n1- Tradutor\n2- Editor de Textos\n3- Revisor Linguístico\n4- Escritor\n5- Professor de Línguas."),
    "marketing": ("O Marketing é uma área fundamental para o sucesso de qualquer empresa. Profissionais dessa área são responsáveis por desenvolver estratégias para promover produtos e serviços, entender o comportamento do consumidor e aumentar as vendas. A carreira oferece a oportunidade de trabalhar em setores inovadores como marketing digital, branding, publicidade e pesquisa de mercado, além de ter uma alta empregabilidade e perspectivas de crescimento rápido.",
    "Principais Carreiras:\n1- Analista de Marketing Digital\n2- Gerente de Marca\n3- Especialista em Mídias Sociais\n4- Pesquisador de Mercado\n5- Estrategista de Publicidade."),
    "medicina": ("A Medicina é uma das profissões mais nobres e essenciais, com o objetivo de salvar vidas e melhorar a saúde das pessoas. Profissionais da área têm a oportunidade de atuar em hospitais, clínicas e pesquisas, trabalhando diretamente com a saúde pública ou privada. Além de ser uma carreira altamente respeitada e bem remunerada, oferece a satisfação de fazer a diferença na vida das pessoas e de contribuir com a evolução da ciência médica.",
    "\n1- Cardiologista\n2- Cirurgião Geral\n3- Pediatra\n4- Infectologista\n5- Psiquiatra."),
    "medicina_veterinaria": ("A Medicina Veterinária é uma carreira voltada para a saúde dos animais, com possibilidades de atuação em clínicas veterinárias, hospitais, zoológicos e em pesquisas. Além de cuidar de pets, os veterinários também trabalham com animais de grande porte, como os de produção, ou em conservação de espécies ameaçadas. A profissão oferece uma grande satisfação ao ver os resultados do cuidado com os animais e proporciona uma carreira estável e com várias opções de especialização.",
    "\n1- Veterinário Clínico\n2- Especialista em Animais Silvestres\n3- Patologista Veterinário\n4- Veterinário Zootecnista\n5- Cirurgião Veterinário."),
    "psicologia": ("A Psicologia é uma área que permite ajudar as pessoas a superar desafios emocionais, comportamentais e psicológicos. Psicólogos podem atuar em diversas áreas, como clínica, organizacional, educacional e hospitalar. A carreira oferece a oportunidade de fazer uma diferença real na vida das pessoas, além de ter uma alta demanda no mercado e uma grande variedade de campos de atuação.",
    "\n1- Psicólogo Clínico\n2- Psicólogo Escolar\n3- Psicólogo Organizacional\n4- Neuropsicólogo\n5- Terapeuta Comportamental."),
    "relacoes_internacionais": ("Relações Internacionais é a área ideal para quem tem interesse por política global, comércio exterior e diplomacia. Profissionais dessa área atuam em organizações internacionais, empresas multinacionais e governos, lidando com negociações, tratados e questões de paz e segurança internacional. A carreira oferece uma visão ampla sobre o mundo e a oportunidade de impactar a política e economia global, além de abrir portas para atuar em diferentes países e culturas.",
    "\n1- Diplomata\n2- Analista de Comércio Internacional\n3- Consultor de Políticas Externas\n4- Especialista em Cooperação Internacional\n5- Tradutor e Intérprete para Organismos Globais.")
}

@app.route('/')
def inicial():
    return render_template('inicial.html')

@app.route('/questionario')
def questionario():
    perguntas_com_indices = [
        {"idx": idx, "pergunta_obj": pergunta_obj}
        for idx, pergunta_obj in enumerate(perguntas["perguntas"])
    ]
    return render_template('questionario.html', perguntas=perguntas_com_indices)

@app.route('/resultado', methods=['POST'])
def resultado():
    pontuacao_total = 0
    respostas_invalidas = []

    for i in range(len(perguntas["perguntas"])):
        resposta = request.form.get(f'pergunta_{i}')
        if resposta and resposta.isdigit() and int(resposta) in [1, 2, 3]:
            pontuacao_total += int(resposta)
        else:
            respostas_invalidas.append(i + 1)

    if respostas_invalidas:
        return f"As perguntas {', '.join(map(str, respostas_invalidas))} contêm respostas inválidas. Por favor, corrija."

    resultado_prolog = list(prolog.query(f"encontrar_carreira({pontuacao_total}, Carreira)"))
    
    if resultado_prolog:
        carreira = resultado_prolog[0]['Carreira']
        mensagem = f"Com base na sua pontuação ({pontuacao_total}), a carreira sugerida é: {carreira.replace('_', ' ').capitalize()}."
        
        if carreira in frases_carreira:
            descricao, principais_carreiras = frases_carreira[carreira]
        else:
            descricao = "Descrição não disponível."
            principais_carreiras = "Principais carreiras não disponíveis."
        
        return render_template('resultado.html', 
                               mensagem=mensagem,
                               descricao=descricao,
                               principais_carreiras=principais_carreiras)
    else:
        mensagem = f"Não foi possível determinar uma carreira com base na pontuação total: {pontuacao_total}."
        return render_template('resultado.html', mensagem=mensagem)

if __name__ == '__main__':
    app.run(debug=True)
