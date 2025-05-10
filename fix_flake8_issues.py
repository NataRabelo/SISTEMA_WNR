import subprocess
import sys
import os


def get_flake8_errors(path):
    """Executa o flake8 e retorna os arquivos com erro."""
    try:
        result = subprocess.run(["flake8", path], capture_output=True, text=True)
        return result.stdout.splitlines()
    except FileNotFoundError:
        print("flake8 não encontrado. Instale com: pip install flake8")
        sys.exit(1)


def extract_files_from_flake8_output(output_lines):
    """Extrai os caminhos únicos dos arquivos que apresentam erro."""
    files = set()
    for line in output_lines:
        if line.strip():
            filepath = line.split(":", 1)[0]
            if os.path.isfile(filepath):  # Só pega arquivos, não pastas
                files.add(filepath)
    return list(files)


def fix_with_autopep8(files):
    """Aplica autopep8 a todos os arquivos."""
    try:
        for file in files:
            print(f"Corrigindo {file} com autopep8...")
            subprocess.run(["autopep8", "--in-place", "--aggressive", "--aggressive", file])
        print("Correções aplicadas.")
    except FileNotFoundError:
        print("autopep8 não encontrado. Instale com: pip install autopep8")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        path = "."
    else:
        path = sys.argv[1]

    flake8_output = get_flake8_errors(path)
    files_with_errors = extract_files_from_flake8_output(flake8_output)

    if not files_with_errors:
        print("Nenhum erro encontrado pelo flake8.")
    else:
        fix_with_autopep8(files_with_errors)
