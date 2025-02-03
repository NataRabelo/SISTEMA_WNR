def limpar_valor(valor):
    if isinstance(valor, str):
        # Remove "R$", espaços invisíveis (\xa0) e troca ',' por '.'
        valor = valor.replace('R$', '').replace('\xa0', '').replace('.', '').replace(',', '.')
        return float(valor)
    return valor