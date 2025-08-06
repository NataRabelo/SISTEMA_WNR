import re

def limpar_mascara(valor):
    return re.sub(r'\D', '', valor)