// Funções para Modal de logout e Flash Messages - Sistema
document.addEventListener("DOMContentLoaded", function (){
    // Lógica do modal
    var modal = document.getElementById("ConfirmarSair");
    var confirmBtn = document.getElementById("confirmarSairBtn");
    modal.addEventListener("show.bs.modal", function (event) {
        var button = event.relatedTarget;
        if (button) {
            confirmBtn.href = "/logout";
        }
    });
    // Lógica para remover as flash messages
    let flashMessages = document.querySelectorAll('.flash-message');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(msg => {
                msg.style.transition = "opacity 0.5s ease";
                msg.style.opacity = "0";
                setTimeout(() => msg.remove(), 500);
            });
        }, 3000);
    }
})

// Função para ativar/desativar "Quantidade de filhos" - Cliente
const campoFilhos = document.getElementById("possui_filhos");
if (campoFilhos) {
    document.getElementById("possui_filhos").addEventListener("change", function(){
        const valorSelecionado = this.value;
        const campo = document.getElementById("qtn_filhos")

        if (valorSelecionado === "Não"){
            campo.disabled = true;
        }else {
            campo.disabled = false;
        }
    })
}

// Função para ativar/desativar "Possui plano de saúde" - Cliente
const campoPlanoSaude = document.getElementById("plano_saude");
if (campoPlanoSaude) {
    document.getElementById("plano_saude").addEventListener("change", function(){
        const valorSelecionado = this.value;
        const campo = document.getElementById("nome_plano_saude");

        if (valorSelecionado === "Não"){
            campo.disabled = true;
        }else {
            campo.disabled = false;
        }
    })
}

// Função para Calcular a Idade - Cliente
const campoDtNascimento = document.getElementById("dt_nascimento");
if (campoDtNascimento) {
    document.getElementById("dt_nascimento").addEventListener("change", function(){
        const nascimento = new Date(this.value);
        const hoje = new Date();

        let idade = hoje.getFullYear() - nascimento.getFullYear();
        const mes = hoje.getMonth() - nascimento.getMonth();

        if (mes < 0 || (mes === 0 && hoje.getDate() < nascimento.getDate())){
            idade--;
        }

        const campoIdade = document.getElementById("idade");
        if (isNaN(idade) || idade < 0) {
            campoIdade.value = '';
        }else{
            campoIdade.value = idade;
        }
        
        const camposResponsaveis = document.getElementById("campos_adicionais");
        if (idade < 18 ){
            camposResponsaveis.style.display = "block";
        }else {
            camposResponsaveis.style.display = "none";  
        }
    })
}

// Função para buscar CEP - Cliente e Profissional
function buscarCep() {
    const cep = document.getElementById('cep').value.trim();
    const bairro = document.getElementById('bairro');
    const cidade = document.getElementById('cidade');
    const estado = document.getElementById('estado');
    let endereco = document.getElementById('endereco');
    if (!endereco){
        endereco = document.getElementById('endereco_profissional');
    }

    // Verifica se o CEP está preenchido e tem 8 dígitos
    if (!cep || cep.length !== 9) {
        alert("CEP inválido! Digite um CEP com 8 números.");
        console.log(cep.length)
        console.log(cep)
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



// Função para buscar Clientes - Encaminhamento e Guia
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

// Função para buscar Profissional - Encaminhamento
function buscarProfissional() {
    const codigo = document.getElementById('profissional_id').value;
    const nomeProfissionalInput = document.getElementById('resultadoProfissional');

    if (!codigo.trim()) {
        nomeProfissionalInput.value = '';
        return;
    }

    fetch(`/buscar_profissional?codigo=${codigo}`)
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
}

// Função para buscar profissionais encaminhados para um cliente - Guia
function buscarProfissionais() {
    let clienteId = document.getElementById("cliente_id").value;

    if (!clienteId.trim()) return;

    fetch(`/buscar_profissionais/${clienteId}`)
        .then(response => response.json())
        .then(data => {
            let select = document.getElementById("profissional_id");

            // Limpa todas as opções antes de adicionar as novas
            select.innerHTML = '';

            if (!data.profissionais || data.profissionais.length === 0) {
                select.innerHTML = '<option value="">Nenhum profissional encontrado</option>';
                return;
            }

            // Adiciona uma opção padrão vazia
            select.innerHTML = '<option value="">Selecione um profissional</option>';

            data.profissionais.forEach(profissional => {
                let option = document.createElement("option");
                option.value = profissional.id;
                option.textContent = profissional.nome + ' - ' + profissional.graduacao;
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

// Função para calcular o saldo - Cliente
function calcularResultado() {
    const campo1 = parseFloat(document.getElementById('remuneracao').value) || 0;
    const campo2 = parseFloat(document.getElementById('renda_familiar').value) || 0;
    const campo3 = parseFloat(document.getElementById('despesa_mensal').value) || 0;

    const resultado = campo1 + campo2 - campo3;
    document.getElementById('saldo').value = resultado;
}
const campoRemuneracao = document.getElementById("remuneracao");
if (campoFilhos) {
    document.getElementById('remuneracao').addEventListener('input', calcularResultado);
    document.getElementById('renda_familiar').addEventListener('input', calcularResultado);
    document.getElementById('despesa_mensal').addEventListener('input', calcularResultado);
}
// Função para ativar o tolltip
document.addEventListener('DOMContentLoaded', function () {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

//  Máscaras para os campos
const foneProfissional = document.getElementById('fone_profissional');
if (foneProfissional) IMask(foneProfissional, { mask: '(00) 00000-0000' });
const fonePessoal = document.getElementById('fone_pessoal');
if (fonePessoal )IMask( fonePessoal, { mask: '(00) 00000-0000' });
const foneContato = document.getElementById('fone_contato');
if (foneContato) IMask(foneContato, { mask: '(00) 00000-0000' });
const cpf = document.getElementById('cpf');
if (cpf) IMask(cpf, { mask: '000.000.000-00'})
const cep = document.getElementById('cep')
if (cep) IMask(cep, '00000-000')