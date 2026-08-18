import random
import time


# ==================================================
# CLASSE DO PERSONAGEM
# ==================================================

class Personagem:

    def __init__(self, nome, classe):

        self.nome = nome
        self.classe = classe

        # INVENTÁRIO
        self.inventario = []
        self.limite_inventario = 10

        # OURO
        self.ouro = 0

        # EQUIPAMENTOS
        self.arma = None
        self.anel = None
        self.armadura = None

        # NÍVEIS DOS EQUIPAMENTOS
        self.nivel_espada = 0
        self.nivel_anel = 0
        self.nivel_armadura = 0

        # ATRIBUTOS
        if classe == "guerreiro":

            self.hp = 150
            self.hp_max = 150
            self.danobase = 30
            self.agilidadebase = 10

        elif classe == "arqueiro":

            self.hp = 100
            self.hp_max = 100
            self.danobase = 25
            self.agilidadebase = 30

        elif classe == "escudeiro":

            self.hp = 200
            self.hp_max = 200
            self.danobase = 15
            self.agilidadebase = 5


    # ==================================================
    # ADICIONAR ITEM
    # ==================================================

    def adicionar_item(self, item):

        if len(self.inventario) >= self.limite_inventario:

            print("\nSeu inventário está cheio!")

            return False

        self.inventario.append(item)

        print(
            f"\n>>> {item} foi adicionado ao inventário!"
        )

        return True


    # ==================================================
    # MOSTRAR INVENTÁRIO
    # ==================================================

    def mostrar_inventario(self):

        print("\n==============================")
        print("          INVENTÁRIO")
        print("==============================")

        if not self.inventario:

            print("\nO inventário está vazio.")

        else:

            for numero, item in enumerate(
                self.inventario,
                start=1
            ):

                print(
                    f"{numero} - {item}"
                )

        print(
            f"\nEspaços: "
            f"{len(self.inventario)}/"
            f"{self.limite_inventario}"
        )

        print(
            f"Ouro: {self.ouro}"
        )


    # ==================================================
    # USAR ITEM
    # ==================================================

    def usar_item(self, numero):

        if numero < 1 or numero > len(self.inventario):

            print("\nItem inválido!")

            return

        item = self.inventario[numero - 1]


        # POÇÃO
        if item == "Poção de cura":

            if self.hp >= self.hp_max:

                print("\nSeu HP já está cheio!")

                return

            cura = 50

            self.hp += cura

            if self.hp > self.hp_max:

                self.hp = self.hp_max

            self.inventario.pop(numero - 1)

            print(
                f"\nVocê recuperou {cura} de HP!"
            )

            print(
                f"HP: {self.hp}/{self.hp_max}"
            )


        # ESPADA DE FERRO
        elif item == "Espada de ferro":

            if self.arma is not None:

                print(
                    "\nVocê já possui uma arma equipada!"
                )

                return

            self.arma = item

            self.inventario.pop(numero - 1)

            self.danobase += 10

            print("\nEspada de ferro equipada!")

            print(
                f"Dano: {self.danobase}"
            )


        # ESPADA DE AÇO
        elif item == "Espada de aço":

            if self.arma is not None:

                print(
                    "\nVocê já possui uma arma equipada!"
                )

                return

            self.arma = item

            self.inventario.pop(numero - 1)

            self.danobase += 25

            print("\nEspada de aço equipada!")

            print(
                f"Dano: {self.danobase}"
            )


        # ANEL MÁGICO
        elif item == "Anel mágico":

            if self.anel is not None:

                print(
                    "\nVocê já possui um anel equipado!"
                )

                return

            self.anel = item

            self.inventario.pop(numero - 1)

            self.agilidadebase += 10

            print("\nAnel mágico equipado!")

            print(
                f"Agilidade: {self.agilidadebase}"
            )


        # ANEL ENCANTADO
        elif item == "Anel encantado":

            if self.anel is not None:

                print(
                    "\nVocê já possui um anel equipado!"
                )

                return

            self.anel = item

            self.inventario.pop(numero - 1)

            self.agilidadebase += 25

            print("\nAnel encantado equipado!")

            print(
                f"Agilidade: {self.agilidadebase}"
            )


        # ARMADURA DE FERRO
        elif item == "Armadura de ferro":

            if self.armadura is not None:

                print(
                    "\nVocê já possui uma armadura!"
                )

                return

            self.armadura = item

            self.inventario.pop(numero - 1)

            self.hp_max += 25
            self.hp += 25

            print(
                "\nArmadura de ferro equipada!"
            )

            print(
                f"HP máximo: {self.hp_max}"
            )


        # ARMADURA DE AÇO
        elif item == "Armadura de aço":

            if self.armadura is not None:

                print(
                    "\nVocê já possui uma armadura!"
                )

                return

            self.armadura = item

            self.inventario.pop(numero - 1)

            self.hp_max += 50
            self.hp += 50

            print(
                "\nArmadura de aço equipada!"
            )

            print(
                f"HP máximo: {self.hp_max}"
            )


    # ==================================================
    # MELHORAR EQUIPAMENTOS
    # ==================================================

    def melhorar_equipamentos(self):

        while True:

            print("\n==============================")
            print("     MELHORAR EQUIPAMENTOS")
            print("==============================")

            print(
                f"\nOuro disponível: {self.ouro}"
            )

            print("\n1 - Melhorar arma")
            print("2 - Melhorar anel")
            print("3 - Melhorar armadura")
            print("4 - Voltar")

            escolha = input(
                "\nEscolha: "
            )


            # MELHORAR ARMA
            if escolha == "1":

                if self.arma is None:

                    print(
                        "\nVocê não possui uma arma."
                    )

                    continue

                custo = 100 + (
                    self.nivel_espada * 100
                )

                print(
                    f"\nCusto: {custo} ouro"
                )

                if self.ouro < custo:

                    print(
                        "\nVocê não possui ouro suficiente!"
                    )

                    continue

                self.ouro -= custo

                self.nivel_espada += 1

                self.danobase += 10

                print(
                    "\n>>> ARMA MELHORADA! <<<"
                )

                print(
                    f"Nível: {self.nivel_espada}"
                )

                print(
                    f"Dano: {self.danobase}"
                )


            # MELHORAR ANEL
            elif escolha == "2":

                if self.anel is None:

                    print(
                        "\nVocê não possui um anel."
                    )

                    continue

                custo = 100 + (
                    self.nivel_anel * 100
                )

                print(
                    f"\nCusto: {custo} ouro"
                )

                if self.ouro < custo:

                    print(
                        "\nVocê não possui ouro suficiente!"
                    )

                    continue

                self.ouro -= custo

                self.nivel_anel += 1

                self.agilidadebase += 5

                print(
                    "\n>>> ANEL MELHORADO! <<<"
                )

                print(
                    f"Agilidade: {self.agilidadebase}"
                )


            # MELHORAR ARMADURA
            elif escolha == "3":

                if self.armadura is None:

                    print(
                        "\nVocê não possui uma armadura."
                    )

                    continue

                custo = 150 + (
                    self.nivel_armadura * 150
                )

                print(
                    f"\nCusto: {custo} ouro"
                )

                if self.ouro < custo:

                    print(
                        "\nVocê não possui ouro suficiente!"
                    )

                    continue

                self.ouro -= custo

                self.nivel_armadura += 1

                self.hp_max += 25
                self.hp += 25

                print(
                    "\n>>> ARMADURA MELHORADA! <<<"
                )

                print(
                    f"HP máximo: {self.hp_max}"
                )


            elif escolha == "4":

                break


            else:

                print(
                    "\nOpção inválida!"
                )


    # ==================================================
    # LOJA
    # ==================================================

    def loja(self):

        while True:

            print("\n==============================")
            print("             LOJA")
            print("==============================")

            print(
                f"\nSeu ouro: {self.ouro}"
            )

            print("\n1 - Espada de aço")
            print("    +25 dano - 300 ouro")

            print("\n2 - Anel encantado")
            print("    +25 agilidade - 300 ouro")

            print("\n3 - Armadura de aço")
            print("    +50 HP - 400 ouro")

            print("\n4 - Poção de cura")
            print("    +50 HP - 50 ouro")

            print("\n5 - Melhorar equipamentos")

            print("\n6 - Sair da loja")

            escolha = input(
                "\nEscolha: "
            )


            # ESPADA
            if escolha == "1":

                preco = 300

                if self.arma is not None:

                    print(
                        "\nVocê já possui uma arma equipada."
                    )

                    continue

                if self.ouro < preco:

                    print(
                        "\nOuro insuficiente!"
                    )

                    continue

                self.ouro -= preco

                self.adicionar_item(
                    "Espada de aço"
                )


            # ANEL
            elif escolha == "2":

                preco = 300

                if self.anel is not None:

                    print(
                        "\nVocê já possui um anel equipado."
                    )

                    continue

                if self.ouro < preco:

                    print(
                        "\nOuro insuficiente!"
                    )

                    continue

                self.ouro -= preco

                self.adicionar_item(
                    "Anel encantado"
                )


            # ARMADURA
            elif escolha == "3":

                preco = 400

                if self.armadura is not None:

                    print(
                        "\nVocê já possui uma armadura."
                    )

                    continue

                if self.ouro < preco:

                    print(
                        "\nOuro insuficiente!"
                    )

                    continue

                self.ouro -= preco

                self.adicionar_item(
                    "Armadura de aço"
                )


            # POÇÃO
            elif escolha == "4":

                preco = 50

                if self.ouro < preco:

                    print(
                        "\nOuro insuficiente!"
                    )

                    continue

                self.ouro -= preco

                self.adicionar_item(
                    "Poção de cura"
                )


            # MELHORAR
            elif escolha == "5":

                self.melhorar_equipamentos()


            # SAIR
            elif escolha == "6":

                print(
                    "\nVocê saiu da loja."
                )

                break


            else:

                print(
                    "\nOpção inválida!"
                )


    # ==================================================
    # MENU
    # ==================================================

    def menu_inventario(self):

        while True:

            print("\n==============================")
            print("       MENU DO PERSONAGEM")
            print("==============================")

            print("1 - Inventário")
            print("2 - Usar equipamento/item")
            print("3 - Loja")
            print("4 - Melhorar equipamentos")
            print("5 - Voltar")

            escolha = input(
                "\nEscolha: "
            )


            if escolha == "1":

                self.mostrar_inventario()


            elif escolha == "2":

                self.mostrar_inventario()

                if self.inventario:

                    try:

                        numero = int(
                            input(
                                "\nNúmero do item: "
                            )
                        )

                        self.usar_item(
                            numero
                        )

                    except ValueError:

                        print(
                            "\nDigite um número!"
                        )


            elif escolha == "3":

                self.loja()


            elif escolha == "4":

                self.melhorar_equipamentos()


            elif escolha == "5":

                break


            else:

                print(
                    "\nOpção inválida!"
                )


# ==================================================
# CLASSE INIMIGO
# ==================================================

class Inimigo:

    def __init__(
        self,
        nome,
        hp,
        dano,
        agilidade,
        ouro
    ):

        self.nome = nome
        self.hp = hp
        self.dano = dano
        self.agilidade = agilidade
        self.ouro = ouro


# ==================================================
# MENU PRINCIPAL
# ==================================================

def jogar():

    while True:

        print("\n==============================")
        print("           MEU JOGO")
        print("==============================")

        print("1 - Iniciar jogo")
        print("2 - Sair")

        escolha = input(
            "\nEscolha: "
        )


        if escolha == "1":

            inicio()

            break


        elif escolha == "2":

            print(
                "\nSaindo do jogo..."
            )

            break


        else:

            print(
                "\nOpção inválida!"
            )


# ==================================================
# INÍCIO
# ==================================================

def inicio():

    input(
        "\nBem-vindo ao jogo!"
        "\nAperte ENTER para continuar..."
    )

    nome = input(
        "\nDigite o nome do personagem: "
    )


    classes = [
        "guerreiro",
        "arqueiro",
        "escudeiro"
    ]


    try:

        escolha = int(
            input(
                "\n1 - Guerreiro"
                "\n2 - Arqueiro"
                "\n3 - Escudeiro"
                "\n\nEscolha: "
            )
        )


    except ValueError:

        print(
            "\nDigite um número!"
        )

        return


    if escolha == 1:

        classe = classes[0]

    elif escolha == 2:

        classe = classes[1]

    elif escolha == 3:

        classe = classes[2]

    else:

        print(
            "\nClasse inválida!"
        )

        return


    personagem = Personagem(
        nome,
        classe
    )


    personagem.adicionar_item(
        "Poção de cura"
    )


    print("\n==============================")
    print("        PERSONAGEM")
    print("==============================")

    print(
        f"\nNome: {personagem.nome}"
    )

    print(
        f"Classe: {personagem.classe}"
    )

    print(
        f"HP: {personagem.hp}"
    )

    print(
        f"Dano: {personagem.danobase}"
    )

    print(
        f"Agilidade: "
        f"{personagem.agilidadebase}"
    )


    input(
        "\nAperte ENTER para continuar..."
    )


    mundo(
        personagem
    )


# ==================================================
# MUNDO
# ==================================================

def mundo(personagem):

    while True:

        print("\n")
        print("========================================")
        print("              MAPA")
        print("========================================")

        print(
            f"\nPersonagem: {personagem.nome}"
        )

        print(
            f"HP: {personagem.hp}/"
            f"{personagem.hp_max}"
        )

        print(
            f"Dano: {personagem.danobase}"
        )

        print(
            f"Ouro: {personagem.ouro}"
        )

        print("\nÁreas disponíveis:")

        print(
            "\n1 - Floresta obscura"
        )

        print(
            "2 - Vilarejo"
        )

        print(
            "3 - Castelo do rei"
        )

        print(
            "4 - Caverna do dragão"
        )

        print(
            "5 - Abrir inventário"
        )

        print(
            "6 - Sair do jogo"
        )


        escolha = input(
            "\nEscolha seu destino: "
        )


        # FLORESTA
        if escolha == "1":

            explorar(
                "floresta obscura",
                personagem
            )


        # VILAREJO
        elif escolha == "2":

            explorar(
                "vilarejo",
                personagem
            )


        # CASTELO
        elif escolha == "3":

            explorar(
                "castelo do rei",
                personagem
            )


        # DRAGÃO
        elif escolha == "4":

            print(
                "\nVocê está entrando "
                "na Caverna do Dragão..."
            )

            time.sleep(1)

            explorar(
                "caverna do dragão",
                personagem
            )


        # INVENTÁRIO
        elif escolha == "5":

            personagem.menu_inventario()


        # SAIR
        elif escolha == "6":

            print(
                "\nSaindo do jogo..."
            )

            break


        else:

            print(
                "\nOpção inválida!"
            )


# ==================================================
# EXPLORAR ÁREA
# ==================================================

def explorar(local, personagem):

    print("\n================================")
    print("          EXPLORAÇÃO")
    print("================================")

    print(
        f"\nVocê está explorando "
        f"a {local}..."
    )

    time.sleep(1)


    adversario(
        local,
        personagem
    )


# ==================================================
# INIMIGOS
# ==================================================

def adversario(local, personagem):

    if local == "floresta obscura":

        inimigo = Inimigo(
            "Lobo",
            80,
            15,
            25,
            75
        )


    elif local == "vilarejo":

        inimigo = Inimigo(
            "Goblin",
            100,
            20,
            35,
            100
        )


    elif local == "castelo do rei":

        inimigo = Inimigo(
            "Cavaleiro",
            180,
            30,
            15,
            150
        )


    elif local == "caverna do dragão":

        inimigo = Inimigo(
            "DRAGÃO",
            300,
            40,
            10,
            500
        )


    else:

        return


    print("\n================================")
    print("        INIMIGO ENCONTRADO")
    print("================================")

    print(
        f"\nInimigo: {inimigo.nome}"
    )

    print(
        f"HP: {inimigo.hp}"
    )

    print(
        f"Dano: {inimigo.dano}"
    )

    print(
        f"Ouro: {inimigo.ouro}"
    )


    input(
        "\nAperte ENTER para lutar..."
    )


    batalha(
        personagem,
        inimigo
    )


# ==================================================
# BATALHA
# ==================================================

def batalha(personagem, inimigo):

    while (
        personagem.hp > 0
        and inimigo.hp > 0
    ):

        print("\n================================")
        print("             BATALHA")
        print("================================")

        print(
            f"\n{personagem.nome}"
        )

        print(
            f"HP: {personagem.hp}/"
            f"{personagem.hp_max}"
        )

        print(
            f"Dano: {personagem.danobase}"
        )

        print(
            f"\n{inimigo.nome}"
        )

        print(
            f"HP: {inimigo.hp}"
        )


        print("\n1 - Atacar")
        print("2 - Recuar")
        print("3 - Inventário")


        escolha = input(
            "\nEscolha: "
        )


        if escolha == "1":

            atacar(
                personagem,
                inimigo
            )

            if inimigo.hp > 0:

                ataque_inimigo(
                    personagem,
                    inimigo
                )


        elif escolha == "2":

            print(
                "\nVocê recuou!"
            )

            return


        elif escolha == "3":

            personagem.menu_inventario()


        else:

            print(
                "\nOpção inválida!"
            )


    if personagem.hp <= 0:

        print("\n================================")
        print("          VOCÊ MORREU")
        print("================================")

        return


    if inimigo.hp <= 0:

        print("\n================================")
        print("          VOCÊ VENCEU!")
        print("================================")

        print(
            f"\nVocê derrotou "
            f"{inimigo.nome}!"
        )


        personagem.ouro += inimigo.ouro

        print(
            f"\nVocê recebeu "
            f"{inimigo.ouro} ouro!"
        )

        print(
            f"Ouro total: "
            f"{personagem.ouro}"
        )


        # DRAGÃO DERROTADO
        if inimigo.nome == "DRAGÃO":

            print("\n================================")
            print("        DRAGÃO DERROTADO!")
            print("================================")

            print(
                "\nVocê conseguiu derrotar "
                "o Dragão!"
            )

            print(
                "\nVOCÊ ZEROU O JOGO!"
            )

            return


        input(
            "\nAperte ENTER para continuar..."
        )


        # DEPOIS DA VITÓRIA
        # O PERSONAGEM CAMINHA
        caminhar(
            personagem
        )


# ==================================================
# ATAQUE
# ==================================================

def atacar(personagem, inimigo):

    dano = personagem.danobase

    critico = random.randint(
        1,
        100
    )


    if critico <= 20:

        dano *= 2

        print(
            "\n!!! ATAQUE CRÍTICO !!!"
        )


    inimigo.hp -= dano


    if inimigo.hp < 0:

        inimigo.hp = 0


    print(
        f"\nVocê causou "
        f"{dano} de dano!"
    )

    print(
        f"HP do {inimigo.nome}: "
        f"{inimigo.hp}"
    )


# ==================================================
# ATAQUE DO INIMIGO
# ==================================================

def ataque_inimigo(
    personagem,
    inimigo
):

    desvio = random.randint(
        1,
        100
    )


    if desvio <= personagem.agilidadebase:

        print(
            "\nVocê desviou do ataque!"
        )

        return


    personagem.hp -= inimigo.dano


    if personagem.hp < 0:

        personagem.hp = 0


    print(
        f"\n{inimigo.nome} causou "
        f"{inimigo.dano} de dano!"
    )

    print(
        f"Seu HP: "
        f"{personagem.hp}/"
        f"{personagem.hp_max}"
    )


# ==================================================
# CAMINHADA
# ==================================================

def caminhar(personagem):

    print("\n================================")
    print("           CAMINHANDO")
    print("================================")

    tempo = random.randint(
        2,
        4
    )


    for i in range(tempo):

        print(
            f"\nCaminhando..."
            f" {i + 1}/{tempo}"
        )

        time.sleep(1)


    # CHANCE DE ENCONTRAR LOJA
    chance_loja = random.randint(
        1,
        100
    )


    if chance_loja <= 40:

        encontrar_loja(
            personagem
        )


    # SEMPRE TEM CHANCE DE BAÚ
    encontrar_bau(
        personagem
    )


    print(
        "\nVocê terminou sua caminhada."
    )

    print(
        "\nVocê pode continuar "
        "explorando o mapa."
    )


# ==================================================
# LOJA NO CAMINHO
# ==================================================

def encontrar_loja(personagem):

    print("\n================================")
    print("        LOJA ENCONTRADA!")
    print("================================")

    print(
        "\nEnquanto caminhava, "
        "você encontrou uma loja!"
    )


    while True:

        escolha = input(
            "\nDeseja entrar na loja? "
            "(s/n): "
        ).lower()


        if escolha == "s":

            personagem.loja()

            break


        elif escolha == "n":

            print(
                "\nVocê continuou "
                "caminhando."
            )

            break


        else:

            print(
                "\nDigite S ou N."
            )


# ==================================================
# BAÚ
# ==================================================

def encontrar_bau(personagem):

    print("\n================================")
    print("            BAÚ!")
    print("================================")

    print(
        "\nVocê encontrou um baú "
        "no caminho!"
    )


    escolha = input(
        "\nDeseja abrir o baú? "
        "(s/n): "
    ).lower()


    if escolha == "s":

        abrir_bau(
            personagem
        )


    else:

        print(
            "\nVocê deixou o baú para trás."
        )


# ==================================================
# ABRIR BAÚ
# ==================================================

def abrir_bau(personagem):

    print("\n================================")
    print("         ABRINDO BAÚ...")
    print("================================")

    time.sleep(2)


    itens = [

        "Poção de cura",
        "Poção de cura",

        "Espada de ferro",

        "Anel mágico",

        "Armadura de ferro"

    ]


    item = random.choice(
        itens
    )


    print(
        f"\n!!! VOCÊ ENCONTROU !!!"
    )

    print(
        f"\n>>> {item} <<<"
    )


    personagem.adicionar_item(
        item
    )


    print(
        "\nO item foi guardado "
        "no seu inventário!"
    )


# ==================================================
# INICIAR
# ==================================================

jogar()
