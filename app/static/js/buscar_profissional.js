
let timeout = null;
function buscarProfissional() {
    const codigo = document.getElementById('profissional_id').value;
    const nomeProfissionalInput = document.getElementById('nomeProfissionalInput');
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
