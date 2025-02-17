def converter_para_float(valor):
    if not valor:
        return 0.0
    # Remove 'R$', pontos e troca vírgula por ponto
    valor = valor.replace('R$', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(valor)
    except ValueError:
        return 0.0
