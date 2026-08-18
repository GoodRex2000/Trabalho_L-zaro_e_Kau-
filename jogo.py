import random


# =========================
# CLASSE DO PERSONAGEM
# =========================

class Personagem:
    def __init__(self, nome, classe):
        self.nome = nome
        self.classe = classe
        self.iventario = []
        self.arma = None
        self.anel = None

        # ATRIBUTOS DAS CLASSES

        if classe == "guerreiro":
            self.hp = 150
            self.danobase = 30
            self.agilidadebase = 10

        elif classe == "arqueiro":
            self.hp = 100
            self.danobase = 25
            self.agilidadebase = 30

        elif classe == "escudeiro":
            self.hp = 200
            self.danobase = 15
            self.agilidadebase = 5

        else:
            print("Classe inválida!")

    # =========================
    # ADICIONAR ITEM
    # =========================

    def adicionar_item_iventario(self, item):
        self.iventario.append(item)
        print(f"o item {item} foi adicionado ao inventário!")

    # =========================
    # MOSTRAR INVENTÁRIO
    # =========================

    def mostrar_iventario(self):

        if not self.iventario:
            print("o inventário está vazio!")
            return
        for item in self.iventario:
            print(f" - {item}")

        else:
            print("\n=========================")
            print("       INVENTÁRIO")
            print("=========================")

            for item in self.iventario:
                print(f" - {item}")


# =========================
# CLASSE DO INIMIGO
# =========================

class Inimigo:
    def __init__(self, nome, hp, dano, agilidade):
        self.nome = nome
        self.hp = hp
        self.dano = dano
        self.agilidade = agilidade


# =========================
# MENU PRINCIPAL
# =========================

def jogar():

    while True:

        print("\n=========================")
        print("       MEU JOGO")
        print("=========================")
        print("1 - iniciar jogo")
        print("2 - sair do jogo")

        escolha = input("escolha uma opção: ")

        if escolha == "1":
            inicio()
            break

        elif escolha == "2":
            print("saindo do jogo...")
            break

        else:
            print("opção inválida!")


# =========================
# INÍCIO DO JOGO
# =========================

def inicio():

    input("\nbem vindo ao jogo, aperte enter para continuar...")

    nome = input("\ndigite o nome do personagem: ")

    classes = [
        "guerreiro",
        "arqueiro",
        "escudeiro"
    ]

    try:

        escolha_sua_classe = int(
            input(
                f"\nescolha sua classe "
                f"(1 - {classes[0]}, "
                f"2 - {classes[1]}, "
                f"3 - {classes[2]}): "
            )
        )

    except ValueError:

        print("você precisa digitar um número!")
        return

    if escolha_sua_classe == 1:
        classe = classes[0]

    elif escolha_sua_classe == 2:
        classe = classes[1]

    elif escolha_sua_classe == 3:
        classe = classes[2]

    else:

        print("classe inválida!")
        return

    # CRIA O PERSONAGEM

    personagem = Personagem(nome, classe)

    # ADICIONA UM ITEM INICIAL

    personagem.adicionar_item_iventario("Poção de cura")

    print("\n=========================")
    print("      PERSONAGEM")
    print("=========================")

    print(f"nome: {personagem.nome}")
    print(f"classe: {personagem.classe}")
    print(f"HP: {personagem.hp}")
    print(f"dano: {personagem.danobase}")
    print(f"agilidade: {personagem.agilidadebase}")

    input("\naperta enter para continuar...")

    mundo("The Nether", personagem)


# =========================
# MUNDO
# =========================

def mundo(mapa, personagem):

    print(f"\nvocê recebeu um mapa do mundo {mapa}!")

    locais = [
        "floresta obscura",
        "caverna do dragão",
        "castelo do rei",
        "vilarejo"
    ]

    try:

        local_de_escolha = int(
            input(
                f"\nescolha um local para explorar "
                f"(1 - {locais[0]}, "
                f"2 - {locais[1]}, "
                f"3 - {locais[2]}, "
                f"4 - {locais[3]}): "
            )
        )

    except ValueError:

        print("você precisa digitar um número!")
        return

    if 1 <= local_de_escolha <= 4:

        local = locais[local_de_escolha - 1]

        print(f"\nvocê escolheu explorar a {local}!")

        adversario(local, personagem)

    else:

        print("local inválido!")


# =========================
# CRIA O INIMIGO
# =========================

def adversario(local, personagem):

    if local == "floresta obscura":

        inimigo = Inimigo(
            "Lobo",
            80,
            15,
            25
        )

    elif local == "caverna do dragão":

        inimigo = Inimigo(
            "Dragão",
            300,
            40,
            10
        )

    elif local == "castelo do rei":

        inimigo = Inimigo(
            "Cavaleiro",
            180,
            30,
            15
        )

    elif local == "vilarejo":

        inimigo = Inimigo(
            "goblin",
            100,
            20,
            35
        )

    else:

        print("nenhum inimigo encontrado!")
        return

    print("\n=========================")
    print("    VOCÊ ENCONTROU UM")
    print("       ADVERSÁRIO!")
    print("=========================")

    print(f"\ninimigo: {inimigo.nome}")
    print(f"HP: {inimigo.hp}")
    print(f"dano: {inimigo.dano}")
    print(f"agilidade: {inimigo.agilidade}")

    input("\naperta enter para continuar...")

    batalha(personagem, inimigo)


# =========================
# BATALHA
# =========================

def batalha(personagem, inimigo):

    while personagem.hp > 0 and inimigo.hp > 0:

        print("\n=========================")
        print("          BATALHA")
        print("=========================")

        print(f"\n{personagem.nome}")
        print(f"HP: {personagem.hp}")

        print(f"\n{inimigo.nome}")
        print(f"HP: {inimigo.hp}")

        print("\n1 - atacar")
        print("2 - recuar")
        print("3 - abrir inventário")

        escolha = input("\nescolha uma opção: ")

        if escolha == "1":

            atacar(personagem, inimigo)

            if inimigo.hp > 0:
                ataque_inimigo(personagem, inimigo)

        elif escolha == "2":

            print("\nvocê recuou da batalha!")
            return

        elif escolha == "3":

            personagem.mostrar_inventario()

        else:

            print("\nopção inválida!")

    if personagem.hp <= 0:

        print("\n=========================")
        print("       VOCÊ MORREU")
        print("=========================")

    elif inimigo.hp <= 0:

        print("\n=========================")
        print("     VOCÊ VENCEU!")
        print("=========================")

        print(f"\nvocê derrotou o {inimigo.nome}!")


# =========================
# ATAQUE DO JOGADOR
# =========================

def atacar(personagem, inimigo):

    dano = personagem.danobase

    critico = random.randint(1, 100)

    if critico <= 20:

        dano *= 2

        print("\nATAQUE CRÍTICO!")

    inimigo.hp -= dano

    if inimigo.hp < 0:
        inimigo.hp = 0

    print(
        f"\n{personagem.nome} atacou "
        f"{inimigo.nome} e causou {dano} de dano!"
    )

    print(f"HP do {inimigo.nome}: {inimigo.hp}")


# =========================
# ATAQUE DO INIMIGO
# =========================

def ataque_inimigo(personagem, inimigo):

    chance_desvio = random.randint(1, 100)

    if chance_desvio <= personagem.agilidadebase:

        print(
            f"\n{personagem.nome} desviou "
            f"do ataque do {inimigo.nome}!"
        )

        return

    dano = inimigo.dano

    personagem.hp -= dano

    if personagem.hp < 0:
        personagem.hp = 0

    print(
        f"\n{inimigo.nome} atacou "
        f"{personagem.nome} e causou {dano} de dano!"
    )

    print(f"Seu HP: {personagem.hp}")
jogar()

