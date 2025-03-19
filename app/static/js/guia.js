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

function buscarProfissionais() {
    let clienteId = document.getElementById("cliente_id").value;

    if (!clienteId.trim()) return;

    fetch(`/buscar_profissionais/${clienteId}`)
        .then(response => response.json())
        .then(data => {
            let select = document.getElementById("profissional_id");
            select.innerHTML = '<option value="">Selecione um profissional</option>';

            if (!data.profissionais || data.profissionais.length === 0) {
                select.innerHTML = '<option value="">Nenhum profissional encontrado</option>';
                return;
            }

            data.profissionais.forEach(profissional => {
                let option = document.createElement("option");
                option.value = profissional.id;
                option.textContent = profissional.nome;
                select.appendChild(option);
            });
        })
        .catch(error => {
            console.error("Erro ao buscar profissionais:", error);
            document.getElementById("profissional_id").innerHTML = '<option value="">Erro ao carregar profissionais</option>';
        });
}
