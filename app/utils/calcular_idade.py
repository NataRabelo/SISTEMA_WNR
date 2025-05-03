from datetime import date

def calcular_idade(data_nascimento):

    if data_nascimento is None:
        return None

    hoje = date.today()
    idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))
    
    return idade