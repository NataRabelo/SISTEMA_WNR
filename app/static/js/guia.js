// Função para bucar o valor acordado - Guia
document.addEventListener("DOMContentLoaded", function () {
    const tipoPagamento = document.getElementById('tipo_pagamento');
    if (tipoPagamento) {
        tipoPagamento.addEventListener('change', buscarValor);
    }
});

function buscarValor() {
    const codigoCliente = document.getElementById('cliente_id').value;
    const codigoProfissional = document.getElementById('profissional_id').value;
    const valorUnitario = document.getElementById('valor_unitario');
    const tipoPagamento = document.getElementById('tipo_pagamento').value;

    if (!codigoCliente.trim() && !codigoProfissional.trim()) {
        valorUnitario.value = '';
        return;
    }

    fetch(`/buscar_valor?codigoCliente=${codigoCliente}&codigoProfissional=${codigoProfissional}&tipoPagamento=${tipoPagamento}`)
        .then(response => response.json())
        .then(data => {
            if (data.erro) {
                valorUnitario.value = data.erro;
            } else {
                valorUnitario.value = data.valor;
            }
        })
        .catch(error => {
            valorUnitario.value = 'Erro na requisição';
            console.error('Erro:', error);
        });
}


function calcularTotal() {
    const quantidadeElement = document.getElementById('quantidade_emissoes');
    let quantidade = quantidadeElement.value.trim();
    let valorUnitario = document.getElementById('valor_unitario').value.trim();
    const valorTotal = document.getElementById('valor_total');

    // Verifica se os campos estão preenchidos
    if ( !valorUnitario) {
        valorUnitario.value = "R$ 0,00";
        return;
    }else if (!quantidade) {
        // Se algum campo estiver vazio, assume 1 para quantidade
        quantidade = "1"; // Definindo "1" como valor padrão
        valorUnitario = valorUnitario.replace(/[R$\s]/g, "").replace(",", ".");
        const total = parseFloat(quantidade) * parseFloat(valorUnitario);
        valorTotal.value = `R$ ${total.toFixed(2).replace(".", ",")}`;
        quantidadeElement.value = "1"; // Definindo "1" no campo quantidade no HTML
        return;
    }

    // Converte o valor unitário para número, removendo "R$" e formatando corretamente
    valorUnitario = valorUnitario.replace(/[R$\s]/g, "").replace(",", ".");

    if (isNaN(quantidade) || isNaN(valorUnitario)) {
        valorTotal.value = "Valor inválido";
        return;
    }

    // Calcula o valor total
    const total = parseFloat(quantidade) * parseFloat(valorUnitario);

    // Exibe o resultado formatado
    valorTotal.value = `R$ ${total.toFixed(2).replace(".", ",")}`;
}

