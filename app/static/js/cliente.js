document.addEventListener('DOMContentLoaded', function () {
    // Aplicação de máscaras
    $('#cpf').mask('000.000.000-00');
    $('#rg').mask('00.000.000-0');
    $('#telefone').mask('(00) 00000-0000');
    $('#celular').mask('(00) 00000-0000');
    $('#cpf_responsavel').mask('000.000.000-00');

    // Funções utilitárias
    function formatarMoeda(campo) {
        if (!campo) return;
        let valor = campo.value.replace(/\D/g, '');
        if (valor === '') {
            campo.value = 'R$ 0,00';
            return;
        }
        valor = (parseInt(valor) / 100).toFixed(2);
        valor = valor.replace('.', ',');
        campo.value = 'R$ ' + valor.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    }

    function obterValorNumerico(valorFormatado) {
        if (!valorFormatado) return 0;
        let valor = valorFormatado.replace(/[^\d,]/g, '').replace(',', '.');
        return parseFloat(valor) || 0;
    }

    function calcularSaldo() {
        const remuneracao = obterValorNumerico(document.getElementById('remuneracao')?.value);
        const rendaFamiliar = obterValorNumerico(document.getElementById('renda_familiar')?.value);
        const despesaMensal = obterValorNumerico(document.getElementById('despesa_mensal')?.value);
        const saldo = (remuneracao + rendaFamiliar) - despesaMensal;
        const saldoCampo = document.getElementById('saldo');
        if (saldoCampo) {
            saldoCampo.value = saldo.toLocaleString('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            });
        }
    }

    const camposMonetarios = [
        document.getElementById('remuneracao'),
        document.getElementById('renda_familiar'),
        document.getElementById('despesa_mensal')
    ];

    camposMonetarios.forEach(campo => {
        if (!campo) return;
        formatarMoeda(campo);
        campo.addEventListener('input', () => {
            formatarMoeda(campo);
            calcularSaldo();
        });
    });

    function calcularIdade(dataNascimento) {
        const nascimento = new Date(dataNascimento);
        const hoje = new Date();
        let idade = hoje.getFullYear() - nascimento.getFullYear();
        const mesAtual = hoje.getMonth();
        const mesNascimento = nascimento.getMonth();
        if (mesAtual < mesNascimento || (mesAtual === mesNascimento && hoje.getDate() < nascimento.getDate())) {
            idade--;
        }
        return idade;
    }

    function atualizarIdade() {
        const dataNascimento = document.getElementById('dt_nascimento')?.value;
        const idadeCampo = document.getElementById('idade');
        const idadeHidden = document.getElementById('idade_hidden');
        const camposAdicionais = document.getElementById('campos_adicionais');

        if (dataNascimento) {
            const idade = calcularIdade(dataNascimento);
            if (idadeCampo) idadeCampo.value = idade;
            if (idadeHidden) idadeHidden.value = idade;
            if (camposAdicionais) camposAdicionais.style.display = idade < 18 ? 'block' : 'none';
        } else {
            if (idadeCampo) idadeCampo.value = '';
            if (idadeHidden) idadeHidden.value = '';
        }
    }

    document.getElementById('dt_nascimento')?.addEventListener('input', atualizarIdade);

    function validarDropdownsObrigatorios() {
        const selectsObrigatorios = document.querySelectorAll('.campoObrigatorio');
        let valido = true;

        selectsObrigatorios.forEach(select => {
            if (select.value === '') {
                valido = false;
                select.style.border = '2px solid red';
            } else {
                select.style.border = '';
            }
        });

        if (!valido) {
            alert('Por favor, selecione uma opção válida em todos os campos obrigatórios.');
        }

        return valido;
    }

    const formulario = document.getElementById('meuFormulario');
    formulario?.addEventListener('submit', function (event) {
        if (!validarDropdownsObrigatorios()) event.preventDefault();
    });

    function buscarCEP() {
        const cep = document.getElementById('cep').value.trim();
        const bairro = document.getElementById('bairro');
        const cidade = document.getElementById('cidade');
        const estado = document.getElementById('estado');
        const endereco = document.getElementById('endereco');

        if (!cep || cep.length !== 8 || isNaN(cep)) {
            alert("CEP inválido! Digite um CEP com 8 números.");
            return;
        }

        fetch(`https://viacep.com.br/ws/${cep}/json/`)
            .then(response => response.json())
            .then(data => {
                if (data.erro) {
                    alert("CEP não encontrado!");
                    bairro.value = '';
                    cidade.value = '';
                    estado.value = '';
                    endereco.value = '';
                } else {
                    bairro.value = data.bairro || '';
                    cidade.value = data.localidade || '';
                    estado.value = data.uf || '';
                    endereco.value = data.logradouro || '';
                }
            })
            .catch(error => {
                alert("Erro ao buscar o CEP. Tente novamente.");
                console.error('Erro:', error);
            });
    }

    function alertaCalculo() {
        document.getElementById("renda_familiar")?.addEventListener("focus", function () {
            alert("Somar: Água + Luz + Alim. + Transp. + Aluguel + Saúde + Escola + Outros");
        });
    }

    alertaCalculo();

    function verificaDropdown_PlanodeSaude() {
        const dropdown = document.getElementById("plano_saude");
        const input = document.getElementById("nome_plano_saude");
        if (dropdown?.value === "Não") {
            input.value = "";
            input.disabled = true;
        } else {
            input.disabled = false;
        }
    }

    function verificarDropdown_Filhos() {
        const dropdown = document.getElementById('possui_filhos');
        const input = document.getElementById('qtn_filhos');
        if (dropdown?.value === "Não") {
            input.value = "";
            input.disabled = true;
        } else {
            input.disabled = false;
        }
    }

    // Busca de cliente em tempo real
    const searchInput = document.getElementById("searchInput");
    const searchResults = document.getElementById("searchResults");

    searchInput?.addEventListener("input", function () {
        const query = searchInput.value.trim();

        if (query.length > 0) {
            fetch(`/filtra_cliente?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    searchResults.innerHTML = "";

                    if (data.length > 0) {
                        data.forEach(cliente => {
                            const item = document.createElement("div");
                            item.classList.add("p-2", "border-bottom");

                            item.innerHTML = `
                                <a href="/editar_cliente/${cliente.id}" class="text-decoration-none text-dark">
                                    <strong>${cliente.nome}</strong><br>
                                    <small>CPF: ${cliente.cpf} | Email: ${cliente.email}</small>
                                </a>
                            `;

                            searchResults.appendChild(item);
                        });
                    } else {
                        searchResults.innerHTML = "<p class='text-muted'>Nenhum cliente encontrado...</p>";
                    }
                })
                .catch(error => {
                    console.error("Erro ao buscar clientes:", error);
                });
        } else {
            searchResults.innerHTML = "<p class='text-muted'>Resultados aparecerão aqui...</p>";
        }
    });
});
