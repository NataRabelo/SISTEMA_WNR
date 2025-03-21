$(document).ready(function() {
    $('#cpf').mask('000.000.000-00'); // Máscara para CPF
    $('#rg').mask('00.000.000-0'); // Máscara para RG
    $('#fone_profissional').mask('(00) 00000-0000'); // Máscara para telefone (suporta celular e fixo)
    $('#fone_pessoal').mask('(00) 00000-0000'); // Máscara para Celular
});

function buscarCEP() {
    const cep = document.getElementById('cep').value.trim();
    const bairro = document.getElementById('bairro');
    const cidade = document.getElementById('cidade');
    const estado = document.getElementById('estado');
    const endereco = document.getElementById('endereco_profissional');

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

    
document.addEventListener("DOMContentLoaded", function () {
    const valorMinimoInput = document.getElementById('valor_minimo');
    
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

    if (valorMinimoInput && valorMinimoInput.value) {
        valorMinimoInput.value = parseFloat(valorMinimoInput.value).toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });
    }

    if (valorMinimoInput) {
        valorMinimoInput.addEventListener('input', function () {
            formatarMoeda(valorMinimoInput);
        });
    }
});