document.getElementById('valor').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    let formattedValue = (Number(value) / 100).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    });
    
    e.target.value = formattedValue;
});