$(document).ready(function() {
    $('#cpf').mask('000.000.000-00'); // Máscara para CPF
    $('#rg').mask('00.000.000-0'); // Máscara para RG
    $('#cep').mask('00000-000'); // Máscara para CEP
    $('#fone_profissional').mask('(00) 00000-0000'); // Máscara para telefone (suporta celular e fixo)
    $('#fone_pessoal').mask('(00) 00000-0000'); // Máscara para Celular
    });
    
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
    