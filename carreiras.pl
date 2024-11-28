% Base de conhecimento com intervalos mais amplos
carreira(administracao, 10, 30).
carreira(artes_cenicas, 31, 50).
carreira(arquitetura, 51, 70).
carreira(ciencia_da_computacao, 71, 90).
carreira(ciencias_biologicas, 91, 110).
carreira(design_grafico, 111, 130).
carreira(direito, 131, 150).
carreira(economia, 151, 170).
carreira(educacao_fisica, 171, 180).
carreira(engenharia, 181, 200).
carreira(jornalismo, 201, 220).
carreira(letras, 221, 240).
carreira(marketing, 241, 260).
carreira(medicina, 261, 280).
carreira(medicina_veterinaria, 281, 300).
carreira(psicologia, 301, 320).
carreira(relacoes_internacionais, 321, 340).

% Regra para encontrar a carreira com base nos pontos
encontrar_carreira(Pontos, Carreira) :-
    carreira(Carreira, Min, Max),
    Pontos >= Min,
    Pontos =< Max.