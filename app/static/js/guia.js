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

            // Verifique se há um valor já selecionado e mantenha a seleção
            let profissionalSelecionado = "{{ guia.profissional_id }}"; // Obtém o valor de guia.profissional_id já selecionado
            if (profissionalSelecionado) {
                select.value = profissionalSelecionado; // Pre-seleciona o profissional
            }
        })
        .catch(error => {
            console.error("Erro ao buscar profissionais:", error);
            document.getElementById("profissional_id").innerHTML = '<option value="">Erro ao carregar profissionais</option>';
        });
}

function buscarValor() {
    const codigoCliente = document.getElementById('cliente_id').value;
    const codigoProfissional = document.getElementById('profissional_id').value;
    const valorUnitario = document.getElementById('valor_unitario');

    if (!codigoCliente.trim() && !codigoProfissional.trim()) {
        valorUnitario.value = '';
        return;
    }

    fetch(`/buscar_valor?codigoCliente=${codigoCliente}&codigoProfissional=${codigoProfissional}`)
        .then(response => response.json())
        .then(data => {
            if (data.erro) {
                valorUnitario.value = data.erro;
            } else {
                valorUnitario.value = data.valor;
            }
        })
        .catch(error => {
            nomeClienteInput.value = 'Erro na requisição';
            console.error('Erro:', error);
        });
}
