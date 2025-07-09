$(document).ready(function() {
    $('#cpf').mask('000.000.000-00');
    $('#rg').mask('00.000.000-0');
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

function buscarCEP() {
    const cep = document.getElementById('cep').value.trim();
    const bairro = document.getElementById('bairro');
    const cidade = document.getElementById('cidade');
    const estado = document.getElementById('estado');
    const endereco = document.getElementById('endereco');

    // Verifica se o CEP está preenchido e tem 8 dígitos
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

// Função para calcular a idade
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

// Função que é chamada quando o valor do campo de data é alterado
function atualizarIdade() {
    const dataNascimento = document.getElementById('dt_nascimento').value;
    if (dataNascimento) {
        const idade = calcularIdade(dataNascimento);
        document.getElementById('idade').value = idade; // Exibe a idade no campo visual
        document.getElementById('idade_hidden').value = idade; // Preenche o campo oculto com a idade
    } else {
        document.getElementById('idade').value = '';
        document.getElementById('idade_hidden').value = '';
    }
}

function toggleCampos() {
    var campos = document.getElementById("campos_adicionais");
    if (campos.style.display === "none" || campos.style.display === "") {
        campos.style.display = "block";
    } else {
        campos.style.display = "none";
    }
}

// Adiciona um evento para chamar a função quando o valor do campo de data for alterado
document.getElementById('dt_nascimento').addEventListener('input', atualizarIdade);


function alertaCalculo() {
    document.getElementById("renda_familiar").addEventListener("focus", function() {
    alert("Somar: Água + Luz + Alim. + Transp. + Aluguel + Saúde + Escola + Outros");
  });
}