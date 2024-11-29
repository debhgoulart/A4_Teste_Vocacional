function calcularRespostas() {
    const form = document.getElementById('questionarioForm');
    const respostas = Array.from(form.elements)
        .filter(element => element.tagName === 'INPUT' && element.type === 'text')
        .map(input => parseInt(input.value, 10));

    if (respostas.some(isNaN)) {
        alert('Por favor, preencha todas as respostas com números válidos (1, 2 ou 3).');
        return;
    }

    const resultado = respostas.reduce((soma, atual) => soma + atual, 0);

    //redireciona
    window.location.href = `/resultado?total=${resultado}`;
}