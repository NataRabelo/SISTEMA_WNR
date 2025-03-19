function buscarProfissional() {
    const codigo = document.getElementById('profissional_id').value;
    const nomeClienteInput = document.getElementById('resultadoProfissional');

    if (!codigo.trim()) {
        nomeClienteInput.value = '';
        return;
    }

    fetch(`/buscar_profissional?codigo=${codigo}`)
        .then(response => response.json())
        .then(data => {
            if (data.erro) {
                nomeClienteInput.value = data.erro;
            } else {
                nomeClienteInput.value = data.nome;
            }
        })
        .catch(error => {
            nomeClienteInput.value = 'Erro na requisição';
            console.error('Erro:', error);
        });
}


function buscarCliente() {
    const codigo = document.getElementById('cliente_id').value;
    const nomeClienteInput = document.getElementById('resultadoCliente');

    if (!codigo.trim()) {
        nomeClienteInput.value = '';
        return;
    }

    fetch(`/buscar_cliente?codigo=${codigo}`)
        .then(response => response.json())
        .then(data => {
            if (data.erro) {
                nomeClienteInput.value = data.erro;
            } else {
                nomeClienteInput.value = data.nome;
            }
        })
        .catch(error => {
            nomeClienteInput.value = 'Erro na requisição';
            console.error('Erro:', error);
        });
}

document.getElementById('valor').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    let formattedValue = (Number(value) / 100).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    });
    
    e.target.value = formattedValue;
});