$(document).ready(function() {
    $('#cpf').mask('000.000.000-00');
    $('#rg').mask('00.000.000-0');
    $('#cep').mask('00000-000'); 
    $('#telefone').mask('(00) 00000-0000'); 
    $('#celular').mask('(00) 00000-0000'); 
    $('#cpf_responsavel').mask('000.000.000-00'); 
});

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

function verificarIdade() {
    const dt_nascimento = document.getElementById("dt_nascimento").value;
    const camposAdicionais = document.getElementById("campos_adicionais");
    const idade = calcularIdade(dt_nascimento);
    

    if (idade < 18) {
        camposAdicionais.style.display = "block";
    } else {
        camposAdicionais.style.display = "none";
    }
}

function obterValorNumerico(valorFormatado) {
    if (!valorFormatado) return 0;

    let valor = valorFormatado.replace(/[^\d,]/g, '').replace(',', '.');
    
    return parseFloat(valor) || 0;
}


function calcularSaldo() {
    const remuneracao = obterValorNumerico(document.getElementById('remuneracao').value);
    const rendaFamiliar = obterValorNumerico(document.getElementById('renda_familiar').value);
    const despesaMensal = obterValorNumerico(document.getElementById('despesa_mensal').value);

    const saldo = (remuneracao + rendaFamiliar) - despesaMensal;

    const saldoCampo = document.getElementById('saldo');
    saldoCampo.value = saldo.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function formatarMoeda(campo) {
    let valor = campo.value.replace(/\D/g, '');
    if (valor === '') {
        campo.value = 'R$ 0,00';
        return;
    }

    valor = (parseInt(valor) / 100).toFixed(2);
    valor = valor.replace('.', ',');

    campo.value = 'R$ ' + valor.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}


const camposMonetarios = [
    document.getElementById('remuneracao'),
    document.getElementById('renda_familiar'),
    document.getElementById('despesa_mensal')
];

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

function verificaDropdown_PlanodeSaude() {
    let dropdown = document.getElementById("plano_saude");
    let input = document.getElementById("nome_plano_saude");
    
    if (dropdown.value === "Não") {
        input.value = "";
        input.disabled = true;

    } else {
        input.disabled = false;
    }
}

function verificarDropdown_Filhos() {
    let dropdown = document.getElementById('possui_filhos');
    let input = document.getElementById('qtn_filhos');
     
    if (dropdown.value === "Não") {
        input.value = "";
        input.disabled = true;
    } else {
        input.disabled = false;
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const formulario = document.getElementById('meuFormulario');

    camposMonetarios.forEach(campo => {
        formatarMoeda(campo);
    });

    calcularSaldo();

    if (formulario) {
        formulario.addEventListener('submit', function (event) {
            if (!validarDropdownsObrigatorios()) {
                event.preventDefault();
            }
        });
    }
});



