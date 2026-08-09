import hashlib
import json
from functools import wraps


arquivo: str = "usuarios.json"


def carregar_usuarios() -> list[dict]:
    try:
        with open(arquivo, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def salvar_usuarios(usuarios: list[dict]) -> None:
    with open(arquivo, "w") as f:
        json.dump(usuarios, f, indent=2)


def gerar_hash(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


def exige_senha_valida(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        senha = kwargs.get("senha")
        if senha is None and args:
            senha = args[-1]

        if not senha or len(senha) < 4:
            print("Senha muito curta")
            return False, "Senha muito curta"

        return func(*args, **kwargs)
    return wrapper


def buscar_usuario(usuarios: list[dict], nome: str) -> dict | None:
    for usuario in usuarios:
        if usuario["nome"] == nome:
            return usuario
    return None


@exige_senha_valida
def cadastrar(
    usuarios: list[dict],
    nomes_existentes: set[str],
    nome: str,
    senha: str
) -> tuple[bool, str]:
    if nome in nomes_existentes:
        return False, "Usuário já existe."
    novo = {"nome": nome, "senha": gerar_hash(senha)}
    usuarios.append(novo)
    nomes_existentes.add(nome)
    salvar_usuarios(usuarios)
    return True, "Cadastrado com sucesso!"


def login(usuarios: list[dict]) -> None:
    nome = input("Usuário: ").strip().lower()
    usuario = buscar_usuario(usuarios, nome)
    if usuario is None:
        print("Usuário não encontrado.")
        return

    tentativas = 0
    while tentativas < 3:
        senha = input("Senha: ")
        if gerar_hash(senha) == usuario["senha"]:
            print(f"Bem-vindo, {nome}!")
            return
        tentativas += 1
        print(f"Senha incorreta. Tentativas restantes: {3 - tentativas}")
    print("Muitas tentativas erradas. Tente novamente mais tarde.")


def menu() -> None:
    usuarios = carregar_usuarios()
    nomes_existentes = {u["nome"] for u in usuarios}

    while True:
        print("\n1 - Cadastrar\n2 - Login\n3 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            nome = input("Novo usuário: ").strip().lower()
            senha = input("Senha: ")
            sucesso, mensagem = cadastrar(usuarios, nomes_existentes, nome, senha)
            print(mensagem)
            if sucesso:
                print("Agora faça o login.")
        elif opcao == "2":
            login(usuarios)
        elif opcao == "3":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
