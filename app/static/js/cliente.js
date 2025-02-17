// Remove a máscara e converte para float antes de calcular
function obterValorNumerico(valor) {
    return parseFloat(valor.replace('R$', '').replace(/\./g, '').replace(',', '.')) || 0;
}

// Função para calcular e exibir o saldo
function calcularSaldo() {
    const remuneracao = obterValorNumerico(document.getElementById('remuneracao').value);
    const rendaFamiliar = obterValorNumerico(document.getElementById('renda_familiar').value);
    const despesaMensal = obterValorNumerico(document.getElementById('despesa_mensal').value);

    // Calculando o saldo
    const saldo = (remuneracao + rendaFamiliar) - despesaMensal;

    // Exibindo o saldo formatado (sem máscara para facilitar no backend)
    document.getElementById('saldo').value = saldo.toFixed(2);
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
