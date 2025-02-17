// Remove a máscara e converte para float antes de calcular
function obterValorNumerico(valor) {
    return parseFloat(valor.replace('R$', '').replace(/\./g, '').replace(',', '.')) || 0;
}

function verificaDropdown_PlanodeSaude() {
let dropdown = document.getElementById("plano_saude");
let input = document.getElementById("nome_plano_saude");

if (dropdown.value === "nao") {
    input.disabled = true;
    input.value = ""; // Limpa o que está escrito
} else {
    input.disabled = false;
}
}


function verificarDropdown_Filhos() {
    let dropdown = document.getElementById('possui_filhos');
    let input = document.getElementById('qtn_filhos');
    
    if (dropdown.value === "nao"){
        input.disabled = true;
        input.value = "";
    }else {
        input.disabled = false;
    }
}


$(document).ready(function() {
$('#cpf').mask('000.000.000-00'); // Máscara para CPF
$('#rg').mask('00.000.000-0'); // Máscara para RG
$('#cep').mask('00000-000'); // Máscara para CEP
$('#telefone').mask('(00) 00000-0000'); // Máscara para telefone (suporta celular e fixo)
$('#celular').mask('(00) 00000-0000'); // Máscara para Celular
$('#cpf_responsavel').mask('000.000.000-00'); // Máscara para CPF responsável
});


function verificarIdade() {
    const dt_nascimento = document.getElementById("dt_nascimento").value;
    const camposAdicionais = document.getElementById("campos_adicionais");
    const idade = calcularIdade(dt_nascimento);
    
    // Verifica se a idade é menor que 18 para exibir os campos adicionais
    if (idade < 18) {
        camposAdicionais.style.display = "block";  // Exibe os campos adicionais
    } else {
        camposAdicionais.style.display = "none";  // Oculta os campos adicionais
    }
}


function calcularIdade(dt_nascimento) {
    const hoje = new Date();
    const nascimento = new Date(dt_nascimento);
    let idade = hoje.getFullYear() - nascimento.getFullYear();
    const m = hoje.getMonth() - nascimento.getMonth();

    if (m < 0 || (m === 0 && hoje.getDate() < nascimento.getDate())) {
        idade--;
    }
    return idade;
}

function formatarMoeda(campo) {
    let valor = campo.value.replace(/\D/g, '');
    if (valor === '') {
        campo.value = 'R$ 0,00';
        return;
    }

    valor = (parseFloat(valor) / 100).toFixed(2);
    valor = valor.replace('.', ',');
    valor = valor.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    campo.value = 'R$ ' + valor;
}

// Função para extrair valor numérico do campo formatado
function obterValorNumerico(valorFormatado) {
    if (!valorFormatado) return 0;
    return parseFloat(valorFormatado.replace(/\D/g, '')) / 100;
}

// Função para calcular e exibir o saldo
function calcularSaldo() {
    const remuneracao = obterValorNumerico(document.getElementById('remuneracao').value);
    const rendaFamiliar = obterValorNumerico(document.getElementById('renda_familiar').value);
    const despesaMensal = obterValorNumerico(document.getElementById('despesa_mensal').value);

    const saldo = (remuneracao + rendaFamiliar) - despesaMensal;

    const saldoCampo = document.getElementById('saldo');
    saldoCampo.value = saldo.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

// Capturando os campos de entrada
const camposMonetarios = [
    document.getElementById('remuneracao'),
    document.getElementById('renda_familiar'),
    document.getElementById('despesa_mensal')
];

// Adicionando evento a cada campo
camposMonetarios.forEach(campo => {
    campo.addEventListener('input', function () {
        formatarMoeda(campo);
        calcularSaldo();
    });
});

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

document.addEventListener('DOMContentLoaded', function () {
    const formulario = document.getElementById('meuFormulario');

    if (formulario) {
        formulario.addEventListener('submit', function (event) {
            if (!validarDropdownsObrigatorios()) {
                event.preventDefault();
            }
        });
    }
});
