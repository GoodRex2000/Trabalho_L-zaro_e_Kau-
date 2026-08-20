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
        self.limite_inventario = 20

        # OURO
        self.ouro = 0

        # EQUIPAMENTOS
        self.arma = "Arma principal"
        self.anel = None
        self.armadura = None
        self.escudo = None

        # ELEMENTO DO ANEL MÁGICO
        self.elemento_anel = None

        # NÍVEIS DOS EQUIPAMENTOS
        self.nivel_espada = 0
        self.nivel_anel = 0
        self.nivel_armadura = 0

        # RESISTÊNCIA DO ESCUDO (% de redução de dano)
        self.resistencia_escudo = 0

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

        else:
            self.hp = 100
            self.hp_max = 100
            self.danobase = 20
            self.agilidadebase = 10

    # ==================================================
    # INVENTÁRIO
    # ==================================================

    def adicionar_item(self, item):
        if len(self.inventario) >= self.limite_inventario:
            print("\nSeu inventário está cheio!")
            return False

        self.inventario.append(item)
        print(f"\n>>> {item} foi adicionado ao inventário!")
        return True

    def remover_item(self, item, quantidade=1):
        removidos = 0

        for _ in range(quantidade):
            if item in self.inventario:
                self.inventario.remove(item)
                removidos += 1

        return removidos == quantidade

    def quantidade_item(self, item):
        return self.inventario.count(item)

    def mostrar_inventario(self):
        print("\n==============================")
        print("          INVENTÁRIO")
        print("==============================")

        if not self.inventario:
            print("\nO inventário está vazio.")
        else:
            for numero, item in enumerate(self.inventario, start=1):
                print(f"{numero} - {item}")

        print(
            f"\nEspaços: {len(self.inventario)}/"
            f"{self.limite_inventario}"
        )
        print(f"Ouro: {self.ouro}")

        print("\n--- EQUIPAMENTOS ---")
        print(f"Arma: {self.arma}")
        print(f"Anel: {self.anel or 'Nenhum'}")
        print(f"Armadura: {self.armadura or 'Nenhuma'}")
        print(f"Escudo: {self.escudo or 'Nenhum'}")
        print(f"Resistência do escudo: {self.resistencia_escudo}%")

        if self.anel == "Anel mágico":
            print(f"Elemento do Anel mágico: {self.elemento_anel}")

    # ==================================================
    # USAR / EQUIPAR ITEM
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
            self.hp = min(self.hp + cura, self.hp_max)
            self.inventario.pop(numero - 1)

            print(f"\nVocê recuperou {cura} de HP!")
            print(f"HP: {self.hp}/{self.hp_max}")

        # ARMAS
        elif item in ("Espada de ferro", "Espada de ferro reforçada", "Arco"):
            if self.arma != "Arma principal":
                print("\nVocê já possui uma arma equipada!")
                print(f"Arma atual: {self.arma}")
                return

            self.arma = item
            self.inventario.pop(numero - 1)

            if item == "Espada de ferro":
                self.danobase += 10
                print("\nEspada de ferro equipada!")
            elif item == "Espada de ferro reforçada":
                self.danobase += 25
                print("\nEspada de ferro reforçada equipada!")
            else:
                self.danobase += 20
                self.agilidadebase += 5
                print("\nArco equipado!")
                print("Bônus: +20 dano e +5 agilidade.")

            print(f"Dano: {self.danobase}")

        # ANEL MÁGICO
        elif item == "Anel mágico":
            if self.anel is not None:
                print("\nVocê já possui um anel equipado!")
                return

            self.anel = item
            self.inventario.pop(numero - 1)
            self.agilidadebase += 10

            print("\nAnel mágico equipado!")
            print(f"Agilidade: {self.agilidadebase}")

            print("\nEscolha o elemento do Anel mágico:")
            print("1 - Água")
            print("2 - Fogo")
            print("3 - Terra")
            print("4 - Vento")

            while True:
                elemento = input("\nEscolha o elemento: ")

                if elemento == "1":
                    self.elemento_anel = "Água"
                    break
                elif elemento == "2":
                    self.elemento_anel = "Fogo"
                    break
                elif elemento == "3":
                    self.elemento_anel = "Terra"
                    break
                elif elemento == "4":
                    self.elemento_anel = "Vento"
                    break
                else:
                    print("\nOpção inválida!")

            print(f"\n>>> Elemento escolhido: {self.elemento_anel} <<<")

        # ANEL DE AGILIDADE
        elif item == "Anel de agilidade":
            if self.anel is not None:
                print("\nVocê já possui um anel equipado!")
                return

            self.anel = item
            self.inventario.pop(numero - 1)
            self.agilidadebase += 25

            print("\nAnel de agilidade equipado!")
            print(f"Agilidade: {self.agilidadebase}")

        # ARMADURAS
        elif item in ("Armadura de ferro", "Armadura de ferro reforçada"):
            if self.armadura is not None:
                print("\nVocê já possui uma armadura!")
                return

            self.armadura = item
            self.inventario.pop(numero - 1)

            if item == "Armadura de ferro":
                aumento_hp = 25
            else:
                aumento_hp = 50

            self.hp_max += aumento_hp
            self.hp += aumento_hp

            print(f"\n{item} equipada!")
            print(f"HP máximo: {self.hp_max}")

        # ESCUDOS
        elif item in ("Escudo de madeira", "Escudo de aço"):
            if self.escudo is not None:
                print("\nVocê já possui um escudo equipado!")
                return

            self.escudo = item
            self.inventario.pop(numero - 1)

            if item == "Escudo de madeira":
                self.resistencia_escudo = 15
            else:
                self.resistencia_escudo = 30

            print(f"\n{item} equipado!")
            print(
                f"Você agora recebe {self.resistencia_escudo}% "
                "menos dano dos inimigos."
            )

        else:
            print("\nEsse item não pode ser usado aqui.")

    # ==================================================
    # SISTEMA DE CRAFT
    # ==================================================

    def mostrar_recursos(self):
        madeira = self.quantidade_item("Madeira")
        aco = self.quantidade_item("Aço reforçado")

        print("\n--- MATERIAIS ---")
        print(f"Madeira: {madeira}")
        print(f"Aço reforçado: {aco}")

    def craftar(self, item):
        receitas = {
            "Arco": {"Madeira": 3, "Aço reforçado": 2},
            "Escudo de madeira": {"Madeira": 4},
            "Escudo de aço": {"Madeira": 2, "Aço reforçado": 3},
        }

        if item not in receitas:
            print("\nItem de craft inválido!")
            return

        receita = receitas[item]

        # Verifica os materiais antes de remover qualquer coisa.
        for material, quantidade in receita.items():
            if self.quantidade_item(material) < quantidade:
                print(f"\nMateriais insuficientes para fabricar {item}!")
                print("Você precisa de:")
                for nome, qtd in receita.items():
                    print(f"- {qtd}x {nome}")
                self.mostrar_recursos()
                return

        # Evita criar o item se o inventário estiver cheio.
        if len(self.inventario) >= self.limite_inventario:
            print("\nSeu inventário está cheio!")
            return

        for material, quantidade in receita.items():
            self.remover_item(material, quantidade)

        self.inventario.append(item)

        print("\n==============================")
        print("       ITEM FABRICADO!")
        print("==============================")
        print(f"\n>>> {item} <<<")

        for material, quantidade in receita.items():
            print(f"- {quantidade}x {material}")

    def sistema_craft(self):
        while True:
            print("\n==============================")
            print("       CONSTRUÇÃO / CRAFT")
            print("==============================")

            self.mostrar_recursos()

            print("\nReceitas:")
            print("\n1 - Arco")
            print("    3 Madeira + 2 Aço reforçado")

            print("\n2 - Escudo de madeira")
            print("    4 Madeira")
            print("    Redução de dano: 15%")

            print("\n3 - Escudo de aço")
            print("    2 Madeira + 3 Aço reforçado")
            print("    Redução de dano: 30%")

            print("\n4 - Voltar")

            escolha = input("\nEscolha: ")

            if escolha == "1":
                self.craftar("Arco")
            elif escolha == "2":
                self.craftar("Escudo de madeira")
            elif escolha == "3":
                self.craftar("Escudo de aço")
            elif escolha == "4":
                break
            else:
                print("\nOpção inválida!")

    # ==================================================
    # MELHORAR EQUIPAMENTOS
    # ==================================================

    def melhorar_equipamentos(self):
        while True:
            print("\n==============================")
            print("     MELHORAR EQUIPAMENTOS")
            print("==============================")
            print(f"\nOuro disponível: {self.ouro}")

            print("\n1 - Melhorar arma")
            print("2 - Melhorar anel")
            print("3 - Melhorar armadura")
            print("4 - Melhorar escudo")
            print("5 - Voltar")

            escolha = input("\nEscolha: ")

            # MELHORAR ARMA
            if escolha == "1":
                if self.arma is None:
                    print("\nVocê não possui uma arma.")
                    continue

                custo = 100 + (self.nivel_espada * 100)

                print(f"\nArma atual: {self.arma}")
                print(f"Nível da arma: {self.nivel_espada}")
                print(f"Custo: {custo} ouro")

                if self.ouro < custo:
                    print("\nVocê não possui ouro suficiente!")
                    continue

                self.ouro -= custo
                self.nivel_espada += 1

                if self.arma == "Espada de ferro":
                    self.danobase += 10
                elif self.arma == "Espada de ferro reforçada":
                    self.danobase += 15
                elif self.arma == "Arco":
                    self.danobase += 12
                else:
                    self.danobase += 10

                print(f"\n>>> {self.arma.upper()} MELHORADA! <<<")
                print(f"Nível: {self.nivel_espada}")
                print(f"Dano: {self.danobase}")

            # MELHORAR ANEL
            elif escolha == "2":
                if self.anel is None:
                    print("\nVocê não possui um anel.")
                    continue

                custo = 100 + (self.nivel_anel * 100)

                print(f"\nCusto: {custo} ouro")

                if self.ouro < custo:
                    print("\nVocê não possui ouro suficiente!")
                    continue

                self.ouro -= custo
                self.nivel_anel += 1

                if self.anel == "Anel mágico":
                    self.agilidadebase += 5
                    if self.elemento_anel == "Água":
                        print("\nHabilidade: Onda Elemental")
                    elif self.elemento_anel == "Fogo":
                        print("\nHabilidade: Chama Elemental")
                    elif self.elemento_anel == "Terra":
                        print("\nHabilidade: Força da Terra")
                    elif self.elemento_anel == "Vento":
                        print("\nHabilidade: Lâmina de Vento")
                elif self.anel == "Anel de agilidade":
                    self.agilidadebase += 10
                else:
                    self.agilidadebase += 5

                print(f"\n>>> {self.anel.upper()} MELHORADO! <<<")
                print(f"Agilidade: {self.agilidadebase}")

            # MELHORAR ARMADURA
            elif escolha == "3":
                if self.armadura is None:
                    print("\nVocê não possui uma armadura.")
                    continue

                custo = 150 + (self.nivel_armadura * 150)

                print(f"\nCusto: {custo} ouro")

                if self.ouro < custo:
                    print("\nVocê não possui ouro suficiente!")
                    continue

                self.ouro -= custo
                self.nivel_armadura += 1

                if self.armadura == "Armadura de ferro":
                    aumento_hp = 25
                elif self.armadura == "Armadura de ferro reforçada":
                    aumento_hp = 40
                else:
                    aumento_hp = 25

                self.hp_max += aumento_hp
                self.hp += aumento_hp

                print(f"\n>>> {self.armadura.upper()} MELHORADA! <<<")
                print(f"HP máximo: {self.hp_max}")

            # MELHORAR ESCUDO
            elif escolha == "4":
                if self.escudo is None:
                    print("\nVocê não possui um escudo.")
                    continue

                custo = 150 + (
                    self.resistencia_escudo * 5
                )

                print(f"\nEscudo atual: {self.escudo}")
                print(f"Resistência atual: {self.resistencia_escudo}%")
                print(f"Custo: {custo} ouro")

                if self.ouro < custo:
                    print("\nVocê não possui ouro suficiente!")
                    continue

                self.ouro -= custo
                aumento = 5
                self.resistencia_escudo += aumento

                print(f"\n>>> {self.escudo.upper()} MELHORADO! <<<")
                print(
                    f"Resistência contra dano: "
                    f"{self.resistencia_escudo}%"
                )

            elif escolha == "5":
                break
            else:
                print("\nOpção inválida!")

    # ==================================================
    # LOJA
    # ==================================================

    def loja(self):
        while True:
            print("\n==============================")
            print("             LOJA")
            print("==============================")
            print(f"\nSeu ouro: {self.ouro}")

            print("\n1 - Espada de ferro reforçada")
            print("    +25 dano - 300 ouro")

            print("\n2 - Anel de agilidade")
            print("    +25 agilidade - 300 ouro")

            print("\n3 - Armadura de ferro reforçada")
            print("    +50 HP - 400 ouro")

            print("\n4 - Poção de cura")
            print("    +50 HP - 50 ouro")

            print("\n5 - Madeira")
            print("    1 unidade - 25 ouro")

            print("\n6 - Aço reforçado")
            print("    1 unidade - 60 ouro")

            print("\n7 - Melhorar equipamentos")
            print("\n8 - Sair da loja")

            escolha = input("\nEscolha: ")

            # ESPADA
            if escolha == "1":
                preco = 300

                if self.arma != "Arma principal":
                    print("\nVocê já possui uma arma equipada.")
                    continue

                if self.ouro < preco:
                    print("\nOuro insuficiente!")
                    continue

                self.ouro -= preco
                self.adicionar_item("Espada de ferro reforçada")

            # ANEL
            elif escolha == "2":
                preco = 300

                if self.anel is not None:
                    print("\nVocê já possui um anel equipado.")
                    continue

                if self.ouro < preco:
                    print("\nOuro insuficiente!")
                    continue

                self.ouro -= preco
                self.adicionar_item("Anel de agilidade")

            # ARMADURA
            elif escolha == "3":
                preco = 400

                if self.armadura is not None:
                    print("\nVocê já possui uma armadura.")
                    continue

                if self.ouro < preco:
                    print("\nOuro insuficiente!")
                    continue

                self.ouro -= preco
                self.adicionar_item("Armadura de ferro reforçada")

            # POÇÃO
            elif escolha == "4":
                preco = 50

                if self.ouro < preco:
                    print("\nOuro insuficiente!")
                    continue

                self.ouro -= preco
                self.adicionar_item("Poção de cura")

            # MADEIRA
            elif escolha == "5":
                preco = 25

                if self.ouro < preco:
                    print("\nOuro insuficiente!")
                    continue

                if len(self.inventario) >= self.limite_inventario:
                    print("\nSeu inventário está cheio!")
                    continue

                self.ouro -= preco
                self.adicionar_item("Madeira")

            # AÇO REFORÇADO
            elif escolha == "6":
                preco = 60

                if self.ouro < preco:
                    print("\nOuro insuficiente!")
                    continue

                if len(self.inventario) >= self.limite_inventario:
                    print("\nSeu inventário está cheio!")
                    continue

                self.ouro -= preco
                self.adicionar_item("Aço reforçado")

            # MELHORAR
            elif escolha == "7":
                self.melhorar_equipamentos()

            # SAIR
            elif escolha == "8":
                print("\nVocê saiu da loja.")
                break

            else:
                print("\nOpção inválida!")

    # ==================================================
    # MENU DO PERSONAGEM
    # ==================================================

    def menu_inventario(self):
        while True:
            print("\n==============================")
            print("       MENU DO PERSONAGEM")
            print("==============================")

            print("1 - Inventário")
            print("2 - Usar equipamento/item")
            print("3 - Craft / Construir itens")
            print("4 - Loja")
            print("5 - Melhorar equipamentos")
            print("6 - Voltar")

            escolha = input("\nEscolha: ")

            if escolha == "1":
                self.mostrar_inventario()

            elif escolha == "2":
                self.mostrar_inventario()

                if self.inventario:
                    try:
                        numero = int(
                            input("\nNúmero do item: ")
                        )
                        self.usar_item(numero)
                    except ValueError:
                        print("\nDigite um número!")

            elif escolha == "3":
                self.sistema_craft()

            elif escolha == "4":
                self.loja()

            elif escolha == "5":
                self.melhorar_equipamentos()

            elif escolha == "6":
                break

            else:
                print("\nOpção inválida!")


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

        escolha = input("\nEscolha: ")

        if escolha == "1":
            inicio()
            break

        elif escolha == "2":
            print("\nSaindo do jogo...")
            break

        else:
            print("\nOpção inválida!")


# ==================================================
# INÍCIO
# ==================================================

def inicio():
    input(
        "\nBem-vindo ao jogo!"
        "\nAperte ENTER para continuar..."
    )

    nome = input("\nDigite o nome do personagem: ")

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
        print("\nDigite um número!")
        return

    if escolha == 1:
        classe = classes[0]
    elif escolha == 2:
        classe = classes[1]
    elif escolha == 3:
        classe = classes[2]
    else:
        print("\nClasse inválida!")
        return

    personagem = Personagem(nome, classe)

    personagem.adicionar_item("Poção de cura")

    print("\n==============================")
    print("        PERSONAGEM")
    print("==============================")

    print(f"\nNome: {personagem.nome}")
    print(f"Classe: {personagem.classe}")
    print(f"HP: {personagem.hp}")
    print(f"Dano: {personagem.danobase}")
    print(f"Agilidade: {personagem.agilidadebase}")

    input("\nAperte ENTER para continuar...")

    mundo(personagem)


# ==================================================
# MUNDO
# ==================================================

def mundo(personagem):
    while True:
        print("\n")
        print("========================================")
        print("              MAPA")
        print("========================================")

        print(f"\nPersonagem: {personagem.nome}")
        print(f"HP: {personagem.hp}/{personagem.hp_max}")
        print(f"Dano: {personagem.danobase}")
        print(f"Ouro: {personagem.ouro}")
        print(f"Escudo: {personagem.escudo or 'Nenhum'}")
        print(f"Resistência: {personagem.resistencia_escudo}%")

        print("\nÁreas disponíveis:")
        print("\n1 - Floresta obscura")
        print("2 - Vilarejo")
        print("3 - Castelo do rei")
        print("4 - Caverna do dragão")
        print("5 - Abrir inventário")
        print("6 - Sair do jogo")

        escolha = input("\nEscolha seu destino: ")

        if escolha == "1":
            fim = explorar("floresta obscura", personagem)
            if fim:
                return

        elif escolha == "2":
            fim = explorar("vilarejo", personagem)
            if fim:
                return

        elif escolha == "3":
            fim = explorar("castelo do rei", personagem)
            if fim:
                return

        elif escolha == "4":
            print(
                "\nVocê está entrando "
                "na Caverna do Dragão..."
            )
            time.sleep(1)

            fim = explorar("caverna do dragão", personagem)
            if fim:
                return

        elif escolha == "5":
            personagem.menu_inventario()

        elif escolha == "6":
            print("\nSaindo do jogo...")
            return

        else:
            print("\nOpção inválida!")


# ==================================================
# EXPLORAR ÁREA
# ==================================================

def explorar(local, personagem):
    print("\n================================")
    print("          EXPLORAÇÃO")
    print("================================")

    print(f"\nVocê está explorando a {local}...")
    time.sleep(1)

    return adversario(local, personagem)


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
        return False

    print("\n================================")
    print("        INIMIGO ENCONTRADO")
    print("================================")

    print(f"\nInimigo: {inimigo.nome}")
    print(f"HP: {inimigo.hp}")
    print(f"Dano: {inimigo.dano}")
    print(f"Ouro: {inimigo.ouro}")

    input("\nAperte ENTER para lutar...")

    return batalha(personagem, inimigo)


# ==================================================
# BATALHA
# ==================================================

def batalha(personagem, inimigo):
    while personagem.hp > 0 and inimigo.hp > 0:
        print("\n================================")
        print("             BATALHA")
        print("================================")

        print(f"\n{personagem.nome}")
        print(f"HP: {personagem.hp}/{personagem.hp_max}")
        print(f"Dano: {personagem.danobase}")
        print(
            f"Escudo: {personagem.escudo or 'Nenhum'} "
            f"({personagem.resistencia_escudo}% resistência)"
        )

        print(f"\n{inimigo.nome}")
        print(f"HP: {inimigo.hp}")

        print("\n1 - Atacar")
        print("2 - Recuar")
        print("3 - Inventário")

        escolha = input("\nEscolha: ")

        if escolha == "1":
            atacar(personagem, inimigo)

            if inimigo.hp > 0:
                ataque_inimigo(personagem, inimigo)

        elif escolha == "2":
            print("\nVocê recuou!")
            return False

        elif escolha == "3":
            personagem.menu_inventario()

        else:
            print("\nOpção inválida!")

    if personagem.hp <= 0:
        print("\n================================")
        print("          VOCÊ MORREU")
        print("================================")
        print("\nFim de jogo!")
        return True

    if inimigo.hp <= 0:
        print("\n================================")
        print("          VOCÊ VENCEU!")
        print("================================")

        print(f"\nVocê derrotou {inimigo.nome}!")

        personagem.ouro += inimigo.ouro

        print(f"\nVocê recebeu {inimigo.ouro} ouro!")
        print(f"Ouro total: {personagem.ouro}")

        # BOSS FINAL
        if inimigo.nome == "DRAGÃO":
            print("\n========================================")
            print("          DRAGÃO DERROTADO!")
            print("========================================")

            print(
                "\nDepois de uma batalha épica, "
                "você conseguiu derrotar o Dragão!"
            )

            print("\nA ameaça que aterrorizava o reino acabou.")
            print(f"O herói {personagem.nome} salvou o reino!")

            print("\n========================================")
            print("             FIM DO JOGO")
            print("========================================")
            print("\nPARABÉNS! VOCÊ ZEROU O JOGO!")
            print("\nObrigado por jogar!")

            return True

        input("\nAperte ENTER para continuar...")

        # Depois da vitória, o personagem caminha.
        caminhar(personagem)

    return False


# ==================================================
# ATAQUE
# ==================================================

def atacar(personagem, inimigo):
    dano = personagem.danobase

    critico = random.randint(1, 100)

    if critico <= 20:
        dano *= 2
        print("\n!!! ATAQUE CRÍTICO !!!")

    inimigo.hp -= dano

    if inimigo.hp < 0:
        inimigo.hp = 0

    print(f"\nVocê causou {dano} de dano!")
    print(f"HP do {inimigo.nome}: {inimigo.hp}")


# ==================================================
# ATAQUE DO INIMIGO
# ==================================================

def ataque_inimigo(personagem, inimigo):
    desvio = random.randint(1, 100)

    if desvio <= personagem.agilidadebase:
        print("\nVocê desviou do ataque!")
        return

    dano_original = inimigo.dano

    # O escudo reduz o dano recebido.
    dano_reduzido = dano_original * (
        1 - personagem.resistencia_escudo / 100
    )

    dano_final = max(1, round(dano_reduzido))

    personagem.hp -= dano_final

    if personagem.hp < 0:
        personagem.hp = 0

    if personagem.resistencia_escudo > 0:
        print(
            f"\nO escudo absorveu parte do ataque!"
            f"\nDano original: {dano_original}"
            f"\nDano recebido: {dano_final}"
        )
    else:
        print(
            f"\n{inimigo.nome} causou "
            f"{dano_final} de dano!"
        )

    print(
        f"Seu HP: "
        f"{personagem.hp}/{personagem.hp_max}"
    )


# ==================================================
# CAMINHADA
# ==================================================

def caminhar(personagem):
    print("\n================================")
    print("           CAMINHANDO")
    print("================================")

    tempo = random.randint(2, 4)

    for i in range(tempo):
        print(f"\nCaminhando... {i + 1}/{tempo}")
        time.sleep(1)

    # CHANCE DE ENCONTRAR LOJA
    chance_loja = random.randint(1, 100)

    if chance_loja <= 40:
        encontrar_loja(personagem)

    # SEMPRE TEM CHANCE DE BAÚ
    encontrar_bau(personagem)

    print("\nVocê terminou sua caminhada.")
    print("\nVocê pode continuar explorando o mapa.")


# ==================================================
# LOJA NO CAMINHO
# ==================================================

def encontrar_loja(personagem):
    print("\n================================")
    print("        LOJA ENCONTRADA!")
    print("================================")

    print("\nEnquanto caminhava, você encontrou uma loja!")

    while True:
        escolha = input(
            "\nDeseja entrar na loja? (s/n): "
        ).lower()

        if escolha == "s":
            personagem.loja()
            break

        elif escolha == "n":
            print("\nVocê continuou caminhando.")
            break

        else:
            print("\nDigite S ou N.")


# ==================================================
# BAÚ
# ==================================================

def encontrar_bau(personagem):
    print("\n================================")
    print("            BAÚ!")
    print("================================")

    print("\nVocê encontrou um baú no caminho!")

    escolha = input(
        "\nDeseja abrir o baú? (s/n): "
    ).lower()

    if escolha == "s":
        abrir_bau(personagem)
    else:
        print("\nVocê deixou o baú para trás.")


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
        "Espada de ferro",
        "Espada de ferro reforçada",
        "Anel mágico",
        "Anel de agilidade",
        "Armadura de ferro",
        "Armadura de ferro reforçada",
        "Madeira",
        "Madeira",
        "Madeira",
        "Aço reforçado",
        "Aço reforçado",
    ]

    item = random.choice(itens)

    print("\n!!! VOCÊ ENCONTROU !!!")
    print(f"\n>>> {item} <<<")

    personagem.adicionar_item(item)

    print("\nO item foi guardado no seu inventário!")


# ==================================================
# INICIAR
# ==================================================

jogar()