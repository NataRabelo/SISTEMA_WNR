
let timeout = null;

function buscarProfissional() {
    const codigo = document.getElementById('profissional_id').value;
    const nomeProfissionalInput = document.getElementById('resultadoProfissional');
    if (!codigo) {
        nomeProfissionalInput.value = '';
        return;
    }
    // Evita fazer requisições a cada tecla digitada (debounce)
    clearTimeout(timeout);
    timeout = setTimeout(() => {
        fetch(`http://127.0.0.1:5000/buscar_profissional?codigo=${codigo}`)
            .then(response => response.json())
            .then(data => {
                if (data.erro) {
                    nomeProfissionalInput.value = data.erro;
                } else {
                    nomeProfissionalInput.value = data.nome;
                }
            })
            .catch(error => {
                nomeProfissionalInput.value = 'Erro na requisição';
                console.error('Erro:', error);
            });
    }, 500);
}


function buscarCliente() {
    const codigo = document.getElementById('client_id').value;
    const nomeClienteInput = document.getElementById('resultadoCliente');
    if (!codigo) {
        nomeClienteInput.value = '';
        return;
    }
    // Evita fazer requisições a cada tecla digitada (debounce)
    clearTimeout(timeout);
    timeout = setTimeout(() => {
        fetch(`http://127.0.0.1:5000/buscar_cliente?codigo=${codigo}`)
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
    }, 500);
}
