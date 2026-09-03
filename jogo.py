import random
import time


# CLASSE DO PERSONAGEM

class Personagem:

    def __init__(self, nome, classe):
        self.nome = nome
        self.classe = classe

        self.inventario = []
        self.limite_inventario = 100
        self.notas_explorador = []

        self.fome = 100
        self.sede = 100

        self.ouro = 0

        self.arca_atual = 1
        self.dragao_derrotado = False

        self.nivel = 1
        self.xp = 0
        self.xp_proximo_nivel = 100

        self.arma = "Arma principal"
        self.anel = None
        self.armadura = None
        self.escudo = None
        self.elemento_anel = None

        self.nivel_espada = 0
        self.nivel_anel = 0
        self.nivel_armadura = 0
        self.nivel_escudo = 0
        self.resistencia_escudo = 0

        self.criaturas = {
            "Raptor": {"domado": False, "quantidade": 0, "sela": False, "montado": False, "nivel_sela": 7},
            "T-Rex": {"domado": False, "quantidade": 0, "sela": False, "montado": False, "nivel_sela": 10},
            "Ictiossauro": {"domado": False, "quantidade": 0, "sela": False, "montado": False, "nivel_sela": 6},
            "Plesiossauro": {"domado": False, "quantidade": 0, "sela": False, "montado": False, "nivel_sela": 11},
            "Megalodonte": {"domado": False, "quantidade": 0, "sela": False, "montado": False, "nivel_sela": 13},
            "Liopleurodon": {"domado": False, "quantidade": 0, "sela": False, "montado": False, "nivel_sela": 14},
            "Mossassauro": {"domado": False, "quantidade": 0, "sela": False, "montado": False, "nivel_sela": 15},
            "Mamute": {"domado": False, "quantidade": 0, "sela": False, "montado": False, "nivel_sela": 12},
            "Rinoceronte lanudo": {"domado": False, "quantidade": 0, "sela": False, "montado": False, "nivel_sela": 14},
            "Smilodonte": {"domado": False, "quantidade": 0, "sela": False, "montado": False, "nivel_sela": 13},
            "Carnotauro": {"domado": False, "quantidade": 0, "sela": False, "montado": False, "nivel_sela": 12},
            "Yutirano": {"domado": False, "quantidade": 0, "sela": False, "montado": False, "nivel_sela": 18},
        }
        self.montaria_atual = None

        self.hipotermia = 0
        self.xp_boost_fim = 0
        self.estrutura_encontrada = 0
        self.criatura_na_jangada = None
        self.area_atual = "floresta obscura"

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

    # XP / NÍVEL

    def xp_multiplicador(self):
        return 2 if time.monotonic() < self.xp_boost_fim else 1

    def ativar_boost_xp(self, segundos=60):
        self.xp_boost_fim = time.monotonic() + segundos
        print("\n>>> NOTAS DE EXPLORADOR: XP 2X ATIVADO POR 1 MINUTO! <<<")

    def tempo_boost_xp(self):
        return max(0, int(self.xp_boost_fim - time.monotonic()))

    def ganhar_xp(self, quantidade):
        if quantidade <= 0:
            return

        multiplicador = self.xp_multiplicador()
        xp_recebido = quantidade * multiplicador
        self.xp += xp_recebido
        if multiplicador == 2:
            print(f"\n>>> +{xp_recebido} XP (2X DAS NOTAS DE EXPLORADOR) <<<")
        else:
            print(f"\n>>> +{xp_recebido} XP <<<")

        while self.xp >= self.xp_proximo_nivel:
            self.xp -= self.xp_proximo_nivel
            self.nivel += 1
            self.xp_proximo_nivel = 100 + (self.nivel - 1) * 50

            self.hp_max += 10
            self.hp = self.hp_max
            self.danobase += 3
            self.agilidadebase += 2

            print("\n" + "=" * 50)
            print(f"              NÍVEL {self.nivel}!")
            print("=" * 50)
            print("Você ficou mais forte!")
            print(f"HP máximo: {self.hp_max}")
            print(f"Dano: {self.danobase}")
            print(f"Agilidade: {self.agilidadebase}")

            self.verificar_desbloqueios()

    def verificar_desbloqueios(self):
        desbloqueios = {
            5: "Arco e Flecha",
            6: "Flecha sedativa e tranquilizante",
            7: "Sela de Raptor",
            8: "Boleadeira",
            10: "Armadilha de urso grande e Roupa de Mergulho",
            11: "Sela de Plesiossauro",
            12: "Picareta, Machado, Sela de Mamute e Sela de Carnotauro",
            13: "Besta e Sela de Smilodonte",
            14: "Sela de Rinoceronte lanudo e Sela de Liopleurodon",
            15: "Sela de Mossassauro",
            18: "Sela de Yutirano",
        }
        if self.nivel in desbloqueios:
            print("\n>>> NOVO DESBLOQUEIO <<<")
            print(f"Nível {self.nivel}: {desbloqueios[self.nivel]}")

    # INVENTÁRIO

    def adicionar_item(self, item, quantidade=1):
        adicionados = 0
        for _ in range(quantidade):
            if len(self.inventario) >= self.limite_inventario:
                print("\nSeu inventário está cheio!")
                break

            self.inventario.append(item)
            adicionados += 1

        if adicionados:
            if quantidade == 1:
                print(f"\n>>> {item} foi adicionado ao inventário!")
            else:
                print(f"\n>>> {adicionados}x {item} foram adicionados ao inventário!")
        return adicionados > 0

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
            contagem = {}
            for item in self.inventario:
                contagem[item] = contagem.get(item, 0) + 1

            numero = 1
            for item, quantidade in contagem.items():
                print(f"{numero} - {item} x{quantidade}")
                numero += 1

        print(f"\nEspaços: {len(self.inventario)}/{self.limite_inventario}")
        print(f"Ouro: {self.ouro}")
        self.mostrar_sobrevivencia()

        print(f"Notas de Explorador: {len(self.notas_explorador)}")

        print("\n--- XP ---")
        print(f"Nível: {self.nivel}")
        print(f"XP: {self.xp}/{self.xp_proximo_nivel}")

        print("\n--- EQUIPAMENTOS ---")
        print(f"Arma: {self.arma}")
        print(f"Anel: {self.anel or 'Nenhum'}")
        print(f"Armadura: {self.armadura or 'Nenhuma'}")
        print(f"Escudo: {self.escudo or 'Nenhum'}")
        print(f"Resistência do escudo: {self.resistencia_escudo}%")

        if self.anel == "Anel mágico":
            print(f"Elemento do Anel mágico: {self.elemento_anel}")

        print("\n--- CRIATURAS ---")
        encontrou = False
        for nome, dados in self.criaturas.items():
            if dados["domado"]:
                encontrou = True
                estado = "montada" if dados["montado"] else "não montada"
                sela = "sela instalada" if dados["sela"] else "sem sela"
                print(f"{nome}: DOMADO | {estado} | {sela}")

        if not encontrou:
            print("Nenhuma criatura domada.")

    # USAR / EQUIPAR ITEM

    def usar_item(self, numero):
        itens_unicos = []
        for item in self.inventario:
            if item not in itens_unicos:
                itens_unicos.append(item)

        if numero < 1 or numero > len(itens_unicos):
            print("\nItem inválido!")
            return

        item = itens_unicos[numero - 1]

        if item == "Poção de cura":
            if self.hp >= self.hp_max:
                print("\nSeu HP já está cheio!")
                return

            cura = 50
            self.hp = min(self.hp + cura, self.hp_max)
            self.remover_item(item)
            print(f"\nVocê recuperou {cura} de HP!")
            print(f"HP: {self.hp}/{self.hp_max}")

        elif item in ("Espada de ferro", "Espada de ferro reforçada", "Arco", "Besta"):
            if self.arma != "Arma principal":
                print("\nVocê já possui uma arma equipada!")
                print(f"Arma atual: {self.arma}")
                return

            self.arma = item
            self.remover_item(item)

            self.danobase += self.bonus_arma_atual()
            if item == "Arco":
                self.agilidadebase += 5
            elif item == "Besta":
                self.agilidadebase += 3
                print("\nBesta equipada! Ela causa mais dano que o arco.")

            print(f"\n{item} equipada!")
            print(f"Dano: {self.danobase}")

        elif item == "Anel mágico":
            if self.anel is not None:
                print("\nVocê já possui um anel equipado!")
                return

            self.anel = item
            self.remover_item(item)
            self.agilidadebase += 10 + self.nivel_anel * 5

            print("\nAnel mágico equipado!")
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

        elif item == "Anel de agilidade":
            if self.anel is not None:
                print("\nVocê já possui um anel equipado!")
                return

            self.anel = item
            self.remover_item(item)
            self.agilidadebase += 25 + self.nivel_anel * 10
            print("\nAnel de agilidade equipado!")
            print(f"Agilidade: {self.agilidadebase}")

        elif item in ("Armadura de ferro", "Armadura de ferro reforçada", "Roupa de pelo grosso"):
            if self.armadura is not None:
                print("\nVocê já possui uma armadura!")
                return

            self.armadura = item
            self.remover_item(item)

            aumento_hp = (25 if item == "Armadura de ferro" else 50 if item == "Armadura de ferro reforçada" else 20) + self.nivel_armadura * 40
            self.hp_max += aumento_hp
            self.hp += aumento_hp

            print(f"\n{item} equipada!")
            print(f"HP máximo: {self.hp_max}")

        elif item in ("Escudo de madeira", "Escudo de aço"):
            if self.escudo is not None:
                print("\nVocê já possui um escudo!")
                return

            self.escudo = item
            self.remover_item(item)

            self.resistencia_escudo = 15 if item == "Escudo de madeira" else 30

            print(f"\n{item} equipado!")
            print(f"Você agora recebe {self.resistencia_escudo}% menos dano.")

        elif item in ("Boleadeira", "Armadilha de urso grande", "Roupa de mergulho",
                      "Flecha", "Flecha sedativa", "Tranquilizante", "Carne crua",
                      "Carne podre", "Mejoberry", "Amarberry", "Azulberry", "Água", "Carne cozida", "Fogueira", "Sela de Raptor",
                      "Sela de T-Rex", "Sela de Mossassauro", "Sela de Ictiossauro",
                      "Sela de Plesiossauro", "Sela de Mamute", "Sela de Carnotauro",
                      "Sela de Smilodonte", "Sela de Megalodonte", "Sela de Rinoceronte lanudo",
                      "Sela de Liopleurodon", "Sela de Yutirano", "Aço reforçado", "Metal",
                      "Madeira", "Fibra", "Pele", "Pelo grosso", "Picareta", "Machado",
                      "Besta", "Jangada", "Roupa de pelo grosso"):
            print("\nEsse item precisa ser usado em uma atividade específica.")
            print("Use-o durante a exploração, na domesticação ou no craft.")

        else:
            print("\nEsse item não pode ser usado aqui.")

    # SOBREVIVÊNCIA E COLETA

    def verificar_frio(self, area):
        if area != "gelo":
            return True
        if self.armadura == "Roupa de pelo grosso":
            self.hipotermia = max(0, self.hipotermia - 10)
            print("\nA roupa de couro peludo protege você do frio extremo.")
            return True
        self.hipotermia += 25
        print(f"\n!!! FRIO EXTREMO !!! Hipotermia: {self.hipotermia}%")
        if self.hipotermia >= 100:
            self.hp = 0
            print("\nVocê morreu de hipotermia!")
            return False
        return True

    def estado_xp(self):
        restante = self.tempo_boost_xp()
        if restante:
            print(f"XP 2X ativo: {restante}s restantes")

    def atualizar_sobrevivencia(self, passos=1):
        self.fome = max(0, self.fome - 3 * passos)
        self.sede = max(0, self.sede - 4 * passos)

        if self.fome == 0:
            self.hp = max(0, self.hp - 5 * passos)
            print("\n!!! FOME EXTREMA: você perdeu vida! !!!")
        if self.sede == 0:
            self.hp = max(0, self.hp - 7 * passos)
            print("\n!!! SEDE EXTREMA: você perdeu vida! !!!")

    def comer_carne_cozida(self):
        if self.quantidade_item("Carne cozida") <= 0:
            print("\nVocê não possui Carne cozida.")
            return
        self.remover_item("Carne cozida")
        self.fome = min(100, self.fome + 25)
        self.hp = min(self.hp_max, self.hp + 10)
        print("\nVocê comeu 1 Carne cozida.")
        print("+10 HP e +25 de Fome!")

    def beber_agua(self):
        if self.quantidade_item("Água") <= 0:
            print("\nVocê não possui Água.")
            return
        self.remover_item("Água")
        self.sede = min(100, self.sede + 40)
        print("\nVocê bebeu água limpa. +40 de Sede!")

    def cozinhar_carne(self):
        if self.quantidade_item("Fogueira") <= 0:
            print("\nVocê precisa ter uma Fogueira para cozinhar.")
            return
        if self.quantidade_item("Carne crua") <= 0:
            print("\nVocê não possui Carne crua.")
            return
        try:
            qtd = int(input("\nQuantas carnes deseja cozinhar? "))
        except ValueError:
            print("\nDigite um número!")
            return
        qtd = max(1, qtd)
        qtd = min(qtd, self.quantidade_item("Carne crua"))
        self.remover_item("Carne crua", qtd)
        self.adicionar_item("Carne cozida", qtd)
        print(f"\nA Fogueira cozinhou {qtd}x Carne crua. Agora você tem Carne cozida!")

    def mostrar_sobrevivencia(self):
        print("\n--- SOBREVIVÊNCIA ---")
        print(f"Fome: {self.fome}/100")
        print(f"Sede: {self.sede}/100")

    def embarcar_na_jangada(self):
        if self.quantidade_item("Jangada") <= 0:
            print("\nVocê não possui uma Jangada.")
            return
        terrestres = [
            nome for nome, dados in self.criaturas.items()
            if dados["domado"] and nome not in {
                "Ictiossauro", "Plesiossauro", "Megalodonte",
                "Liopleurodon", "Mossassauro"
            }
        ]
        if not terrestres:
            print("\nVocê ainda não possui uma criatura terrestre para levar na Jangada.")
            return
        print("\n--- CRIATURA PARA A JANGADA ---")
        for i, nome in enumerate(terrestres, 1):
            print(f"{i} - {nome} x{self.criaturas[nome].get('quantidade', 1)}")
        try:
            escolha = int(input("\nEscolha: "))
        except ValueError:
            print("\nDigite um número.")
            return
        if 1 <= escolha <= len(terrestres):
            self.criatura_na_jangada = terrestres[escolha - 1]
            print(f"\n>>> {self.criatura_na_jangada} embarcou na Jangada! <<<")
            print("Você poderá levá-la pelo oceano antes de possuir uma montaria marinha.")
        else:
            print("\nOpção inválida.")

    # CRAFT

    def receitas_disponiveis(self):
        return {
            "Fogueira": {"nivel": 1, "materiais": {"Madeira": 3, "Fibra": 2}, "quantidade": 1},
            "Arco": {"nivel": 5, "materiais": {"Madeira": 3, "Fibra": 4}, "quantidade": 1},
            "Flecha": {"nivel": 5, "materiais": {"Madeira": 1, "Fibra": 2}, "quantidade": 5},
            "Tranquilizante": {"nivel": 6, "materiais": {"Carne podre": 2, "Mejoberry": 3}, "quantidade": 1},
            "Flecha sedativa": {"nivel": 6, "materiais": {"Flecha": 1, "Tranquilizante": 1}, "quantidade": 1},
            "Boleadeira": {"nivel": 8, "materiais": {"Fibra": 6, "Madeira": 3}, "quantidade": 1},
            "Armadilha de urso grande": {"nivel": 10, "materiais": {"Madeira": 5, "Metal": 4}, "quantidade": 1},
            "Roupa de mergulho": {"nivel": 10, "materiais": {"Fibra": 10, "Metal": 4}, "quantidade": 1},
            "Picareta": {"nivel": 12, "materiais": {"Madeira": 2, "Metal": 3}, "quantidade": 1},
            "Machado": {"nivel": 12, "materiais": {"Madeira": 2, "Metal": 3}, "quantidade": 1},
            "Besta": {"nivel": 13, "materiais": {"Madeira": 4, "Fibra": 5, "Metal": 6}, "quantidade": 1},
            "Roupa de pelo grosso": {"nivel": 10, "materiais": {"Fibra": 8, "Pele": 4, "Pelo grosso": 8}, "quantidade": 1},
            "Jangada": {"nivel": 10, "materiais": {"Madeira": 15, "Fibra": 12}, "quantidade": 1},
            "Sela de Ictiossauro": {"nivel": 6, "materiais": {"Madeira": 5, "Fibra": 6, "Metal": 2}, "quantidade": 1},
            "Sela de Raptor": {"nivel": 7, "materiais": {"Madeira": 6, "Fibra": 8, "Metal": 2}, "quantidade": 1},
            "Sela de T-Rex": {"nivel": 10, "materiais": {"Madeira": 10, "Fibra": 12, "Metal": 6}, "quantidade": 1},
            "Sela de Plesiossauro": {"nivel": 11, "materiais": {"Madeira": 8, "Fibra": 10, "Metal": 4}, "quantidade": 1},
            "Sela de Mamute": {"nivel": 12, "materiais": {"Madeira": 12, "Fibra": 14, "Pele": 6}, "quantidade": 1},
            "Sela de Carnotauro": {"nivel": 12, "materiais": {"Madeira": 8, "Fibra": 10, "Metal": 4}, "quantidade": 1},
            "Sela de Smilodonte": {"nivel": 13, "materiais": {"Madeira": 7, "Fibra": 9, "Pele": 4}, "quantidade": 1},
            "Sela de Megalodonte": {"nivel": 13, "materiais": {"Madeira": 10, "Fibra": 12, "Metal": 6}, "quantidade": 1},
            "Sela de Rinoceronte lanudo": {"nivel": 14, "materiais": {"Madeira": 12, "Fibra": 14, "Pele": 8}, "quantidade": 1},
            "Sela de Liopleurodon": {"nivel": 14, "materiais": {"Madeira": 12, "Fibra": 14, "Metal": 8}, "quantidade": 1},
            "Sela de Mossassauro": {"nivel": 15, "materiais": {"Madeira": 14, "Fibra": 16, "Metal": 10}, "quantidade": 1},
            "Sela de Yutirano": {"nivel": 18, "materiais": {"Madeira": 15, "Fibra": 18, "Pele": 8, "Metal": 8}, "quantidade": 1},
            "Escudo de madeira": {"nivel": 1, "materiais": {"Madeira": 4}, "quantidade": 1},
            "Escudo de aço": {"nivel": 1, "materiais": {"Madeira": 2, "Metal": 3}, "quantidade": 1},
        }

    def mostrar_recursos(self):
        materiais = [
            "Madeira", "Fibra", "Metal", "Carne crua", "Carne podre",
            "Mejoberry", "Amarberry", "Azulberry", "Pele", "Pelo grosso", "Água", "Carne cozida", "Fogueira", "Flecha", "Tranquilizante"
        ]
        print("\n--- RECURSOS ---")
        for material in materiais:
            qtd = self.quantidade_item(material)
            if qtd > 0:
                print(f"{material}: {qtd}")

    def craftar(self, item):
        receitas = self.receitas_disponiveis()
        if item not in receitas:
            print("\nItem de craft inválido!")
            return

        receita = receitas[item]
        if self.nivel < receita["nivel"]:
            print(
                f"\nVocê precisa estar no nível {receita['nivel']} "
                f"para fabricar {item}."
            )
            print(f"Seu nível atual: {self.nivel}")
            return

        for material, quantidade in receita["materiais"].items():
            if self.quantidade_item(material) < quantidade:
                print(f"\nMateriais insuficientes para fabricar {item}!")
                for nome, qtd in receita["materiais"].items():
                    print(f"- {qtd}x {nome}")
                self.mostrar_recursos()
                return

        quantidade_final = receita["quantidade"]

        if len(self.inventario) + quantidade_final > self.limite_inventario:
            print("\nNão há espaço suficiente no inventário!")
            return

        for material, quantidade in receita["materiais"].items():
            self.remover_item(material, quantidade)
        self.adicionar_item(item, quantidade_final)
        print("ITEM FABRICADO!")
        print(f"\n>>> {item} x{quantidade_final} <<<")

    def sistema_craft(self):
        while True:
            print("CONSTRUÇÃO / CRAFT")
            print(f"Nível atual: {self.nivel}")

            receitas = self.receitas_disponiveis()

            print("\nReceitas:")
            numero = 1
            nomes = []

            for nome, dados in receitas.items():
                nomes.append(nome)
                materiais = " + ".join(
                    f"{qtd} {mat}" for mat, qtd in dados["materiais"].items()
                )
                print(f"\n{numero} - {nome}")
                print(f"Nível: {dados['nivel']}")
                print(f"{materiais}")
                print(f"Produz: {dados['quantidade']}")

                if self.nivel >= dados["nivel"]:
                    print("STATUS: DESBLOQUEADO")
                else:
                    print("STATUS: BLOQUEADO")

                numero += 1

            print(f"\n{numero} - Voltar")
            escolha = input("\nEscolha: ")
            try:
                opcao = int(escolha)
                if 1 <= opcao <= len(nomes):
                    self.craftar(nomes[opcao - 1])
                elif opcao == len(nomes) + 1:
                    break
                else:
                    print("\nOpção inválida!")
            except ValueError:
                print("\nDigite um número!")

    # MELHORAR EQUIPAMENTOS

    def melhorar_equipamentos(self):
        while True:
            print("\n==============================")
            print("     MELHORAR EQUIPAMENTOS")
            print("==============================")
            print(f"Ouro disponível: {self.ouro}")

            print("\n1 - Melhorar arma")
            print("2 - Melhorar anel")
            print("3 - Melhorar armadura")
            print("4 - Melhorar escudo")
            print("5 - Voltar")

            escolha = input("\nEscolha: ")

            if escolha == "1":
                if self.arma == "Arma principal":
                    print("\nVocê não possui uma arma equipada.")
                    continue

                custo = 100 + self.nivel_espada * 100

                if self.ouro < custo:
                    print("\nOuro insuficiente!")
                    continue

                self.ouro -= custo
                self.nivel_espada += 1
                if self.arma == "Espada de ferro":
                    self.danobase += 10
                elif self.arma == "Espada de ferro reforçada":
                    self.danobase += 15
                elif self.arma == "Arco":
                    self.danobase += 12

                print(f"\n>>> {self.arma.upper()} MELHORADA! <<<")
                print(f"Nível: {self.nivel_espada}")
                print(f"Dano: {self.danobase}")

            elif escolha == "2":
                if self.anel is None:
                    print("\nVocê não possui um anel.")
                    continue

                custo = 100 + self.nivel_anel * 100

                if self.ouro < custo:
                    print("\nOuro insuficiente!")
                    continue

                self.ouro -= custo
                self.nivel_anel += 1
                if self.anel == "Anel mágico":
                    self.agilidadebase += 5
                elif self.anel == "Anel de agilidade":
                    self.agilidadebase += 10
                print(f"\n>>> {self.anel.upper()} MELHORADO! <<<")
                print(f"Agilidade: {self.agilidadebase}")

            elif escolha == "3":
                if self.armadura is None:
                    print("\nVocê não possui uma armadura.")
                    continue

                custo = 150 + self.nivel_armadura * 150
                if self.ouro < custo:
                    print("\nOuro insuficiente!")
                    continue

                self.ouro -= custo
                self.nivel_armadura += 1
                aumento_hp = 25 if self.armadura == "Armadura de ferro" else 40
                self.hp_max += aumento_hp
                self.hp += aumento_hp

                print(f"\n>>> {self.armadura.upper()} MELHORADA! <<<")
                print(f"HP máximo: {self.hp_max}")

            elif escolha == "4":
                if self.escudo is None:
                    print("\nVocê não possui um escudo.")
                    continue

                custo = 150 + self.nivel_escudo * 100

                if self.ouro < custo:
                    print("\nOuro insuficiente!")
                    continue

                self.ouro -= custo
                self.nivel_escudo += 1
                self.resistencia_escudo += 5

                print(f"\n>>> {self.escudo.upper()} MELHORADO! <<<")
                print(f"Resistência: {self.resistencia_escudo}%")

            elif escolha == "5":
                break

            else:
                print("\nOpção inválida!")

    # LOJA

    def loja(self):
        print("\n" + "=" * 58)
        print("                HELENA - IA")
        print("=" * 58)
        print('\n"Olá, consciência holográfica. Sou HELENA, a inteligência artificial da RAGNAROCK I."')
        print('"Não há nenhum humano vivo nesta Arca. Eu sou a única voz que ainda responde a você."')
        print('"Posso vender equipamentos e materiais recuperados dos sistemas da Arca."')

        itens_loja = [
            ("Espada de ferro reforçada", 300),
            ("Anel de agilidade", 300),
            ("Armadura de ferro reforçada", 400),
            ("Poção de cura", 50),
            ("Aço reforçado", 60),
            ("Metal", 80),
            ("Pele", 70),
        ]

        while True:
            print("\n--------------------------------")
            print(f"HELENA | Ouro disponível: {self.ouro}")
            print("--------------------------------")
            for i, (nome, preco) in enumerate(itens_loja, start=1):
                print(f"{i} - {nome} - {preco} ouro")
            print(f"{len(itens_loja)+1} - Melhorar equipamentos")
            print(f"{len(itens_loja)+2} - Sair")

            try:
                escolha = int(input("\nEscolha: "))
            except ValueError:
                print("\nHELENA: Digite um número válido.")
                continue

            if 1 <= escolha <= len(itens_loja):
                item, preco = itens_loja[escolha - 1]
                if self.ouro < preco:
                    print("\nHELENA: Seus créditos não são suficientes.")
                    continue
                if item == "Espada de ferro reforçada" and self.arma != "Arma principal":
                    print("\nHELENA: Você já possui uma arma equipada.")
                    continue
                if item == "Anel de agilidade" and self.anel is not None:
                    print("\nHELENA: Você já possui um anel equipado.")
                    continue
                if item == "Armadura de ferro reforçada" and self.armadura is not None:
                    print("\nHELENA: Você já possui uma armadura equipada.")
                    continue
                if len(self.inventario) >= self.limite_inventario:
                    print("\nHELENA: Seu inventário está cheio.")
                    continue
                self.ouro -= preco
                self.adicionar_item(item)
                print(f"\nHELENA: Transação concluída. {item} entregue.")
            elif escolha == len(itens_loja) + 1:
                self.melhorar_equipamentos()
            elif escolha == len(itens_loja) + 2:
                print("\nHELENA: Encerrando o terminal comercial.")
                break
            else:
                print("\nHELENA: Opção inexistente.")

    # CRIATURAS / MONTARIA

    def mostrar_criaturas(self):
        print("\n==============================")
        print("       CRIATURAS DOMADAS")
        print("==============================")
        possui = False
        for nome, dados in self.criaturas.items():
            if dados["domado"]:
                possui = True
                quantidade = dados.get("quantidade", 1)
                pode_montar = dados["sela"] and self.nivel >= dados["nivel_sela"]
                print(f"\n{nome} x{quantidade}")
                print("  Domado: SIM")
                print(f"  Sela colocada: {'SIM' if dados['sela'] else 'NÃO'}")
                print(f"  Nível da sela: {dados['nivel_sela']}")
                print(f"  Pode montar: {'SIM' if pode_montar else 'NÃO'}")
                if nome == "Raptor" and quantidade >= 2:
                    print(f"  BÔNUS DE BANDO: +{10 + (quantidade-2)*5}% dano")
                if nome == "Mamute" and quantidade >= 2:
                    print("  RUGIDO DO MAMUTE: resistência do bando aumentada")
                if nome in ("T-Rex", "Smilodonte"):
                    print("  BÔNUS: ataques com sangramento")
        if not possui:
            print("\nVocê ainda não domou nenhuma criatura.")

    def montar_criatura(self):
        self.mostrar_criaturas()
        domadas = [nome for nome, dados in self.criaturas.items() if dados["domado"]]
        if not domadas:
            return

        print("\nEscolha uma criatura:")
        for i, nome in enumerate(domadas, start=1):
            print(f"{i} - {nome} x{self.criaturas[nome].get('quantidade', 1)}")
        print(f"{len(domadas)+1} - Desmontar")

        try:
            escolha = int(input("\nEscolha: "))
        except ValueError:
            print("\nDigite um número!")
            return

        if escolha == len(domadas) + 1:
            if self.montaria_atual:
                self.criaturas[self.montaria_atual]["montado"] = False
            self.montaria_atual = None
            print("\nVocê desmontou.")
            return

        if not 1 <= escolha <= len(domadas):
            print("\nOpção inválida!")
            return

        nome = domadas[escolha - 1]
        dados = self.criaturas[nome]

        if self.nivel < dados["nivel_sela"]:
            print(f"\nVocê precisa do nível {dados['nivel_sela']} para usar a sela de {nome}.")
            return

        sela_nome = f"Sela de {nome}"
        if self.quantidade_item(sela_nome) > 0:
            self.remover_item(sela_nome)
            dados["sela"] = True

        if not dados["sela"]:
            print(f"\nVocê precisa da {sela_nome}.")
            return

        if self.montaria_atual:
            self.criaturas[self.montaria_atual]["montado"] = False
        dados["montado"] = True
        self.montaria_atual = nome
        print(f"\n>>> Você montou o {nome}! <<<")
        if nome == "Ictiossauro":
            print("Bônus: grande velocidade no oceano e habilidade CHACOALHAR.")
        elif nome == "Raptor":
            print("Bônus: velocidade e dano do bando.")
        elif nome == "T-Rex":
            print("Bônus: sangramento.")
        elif nome == "Smilodonte":
            print("Bônus: sangramento.")
        elif nome == "Mamute":
            print("Bônus: RUGIDO DO MAMUTE melhora a resistência do bando.")
        elif nome == "Yutirano":
            print("Bônus: RUGIDO DE GUERRA fortalece aliados.")
        elif nome == "Mossassauro":
            print("Bônus: exploração profunda do oceano.")

    # MENU DO PERSONAGEM

    def bonus_arma_atual(self):
        if self.arma == "Espada de ferro":
            return 10 + self.nivel_espada * 10
        if self.arma == "Espada de ferro reforçada":
            return 25 + self.nivel_espada * 15
        if self.arma == "Arco":
            return 20 + self.nivel_espada * 12
        if self.arma == "Besta":
            return 35 + self.nivel_espada * 12
        return 0

    def desequipar_arma(self):
        if self.arma == "Arma principal":
            print("\nVocê não possui uma arma equipada.")
            return
        item = self.arma
        self.danobase -= self.bonus_arma_atual()
        self.danobase = max(1, self.danobase)
        if item == "Arco":
            self.agilidadebase = max(1, self.agilidadebase - 5)
        if item == "Besta":
            self.agilidadebase = max(1, self.agilidadebase - 3)
        self.arma = "Arma principal"
        self.adicionar_item(item)
        print(f"\n{item} desequipada e devolvida ao inventário.")

    def desequipar_armadura(self):
        if self.armadura is None:
            print("\nVocê não possui uma armadura equipada.")
            return
        item = self.armadura
        bonus = (25 if item == "Armadura de ferro" else 50 if item == "Armadura de ferro reforçada" else 20) + self.nivel_armadura * 40
        self.hp_max = max(1, self.hp_max - bonus)
        self.hp = min(self.hp, self.hp_max)
        self.armadura = None
        self.adicionar_item(item)
        print(f"\n{item} desequipada e devolvida ao inventário.")

    def desequipar_anel(self):
        if self.anel is None:
            print("\nVocê não possui um anel equipado.")
            return
        item = self.anel
        self.agilidadebase -= (10 if item == "Anel mágico" else 25) + self.nivel_anel * (5 if item == "Anel mágico" else 10)
        self.agilidadebase = max(1, self.agilidadebase)
        self.anel = None
        self.elemento_anel = None
        self.adicionar_item(item)
        print(f"\n{item} desequipado e devolvido ao inventário.")

    def desequipar_escudo(self):
        if self.escudo is None:
            print("\nVocê não possui um escudo equipado.")
            return
        item = self.escudo
        self.resistencia_escudo = 0
        self.escudo = None
        self.adicionar_item(item)
        print(f"\n{item} desequipado e devolvido ao inventário.")

    def remover_item_menu(self):
        if not self.inventario:
            print("\nO inventário está vazio.")
            return
        unicos = list(dict.fromkeys(self.inventario))
        print("\n--- REMOVER ITEM ---")
        for i, item in enumerate(unicos, 1):
            print(f"{i} - {item} x{self.quantidade_item(item)}")
        try:
            numero = int(input("\nNúmero do item: "))
            if not 1 <= numero <= len(unicos):
                print("\nItem inválido!")
                return
            item = unicos[numero - 1]
            quantidade = int(input(f"Quantidade de {item} para remover: "))
            if quantidade <= 0:
                print("\nA quantidade deve ser maior que zero.")
                return
            if quantidade > self.quantidade_item(item):
                print("\nVocê não possui essa quantidade.")
                return
            self.remover_item(item, quantidade)
            print(f"\n>>> {quantidade}x {item} removido(s) do inventário. <<<")
        except ValueError:
            print("\nDigite números válidos!")

    def menu_equipamentos(self):
        while True:
            print("\n==============================")
            print("      EQUIPAR / DESEQUIPAR")
            print("==============================")
            print(f"Arma: {self.arma}")
            print(f"Anel: {self.anel or 'Nenhum'}")
            print(f"Armadura: {self.armadura or 'Nenhuma'}")
            print(f"Escudo: {self.escudo or 'Nenhum'}")
            print("\n1 - Equipar item do inventário")
            print("2 - Desequipar arma")
            print("3 - Desequipar anel")
            print("4 - Desequipar armadura")
            print("5 - Desequipar escudo")
            print("6 - Voltar")
            op = input("\nEscolha: ")
            if op == "1":
                self.mostrar_inventario()
                unicos = list(dict.fromkeys(self.inventario))
                if unicos:
                    try:
                        n = int(input("\nNúmero do item para equipar: "))
                        self.usar_item(n)
                    except ValueError:
                        print("\nDigite um número!")
            elif op == "2": self.desequipar_arma()
            elif op == "3": self.desequipar_anel()
            elif op == "4": self.desequipar_armadura()
            elif op == "5": self.desequipar_escudo()
            elif op == "6": break
            else: print("\nOpção inválida!")

    def menu_sobrevivencia(self):
        while True:
            self.mostrar_sobrevivencia()
            print("\n1 - Comer Carne cozida (+10 HP, +25 Fome)")
            print("2 - Beber Água (+40 Sede)")
            print("3 - Voltar")
            op = input("\nEscolha: ")
            if op == "1": self.comer_carne_cozida()
            elif op == "2": self.beber_agua()
            elif op == "3": self.cozinhar_carne()
            elif op == "4": break
            else: print("\nOpção inválida!")

    def menu_inventario(self):
        while True:
            print("\n==============================")
            print("       MENU DO PERSONAGEM")
            print("==============================")

            print("1 - Inventário")
            print("2 - Remover item do inventário")
            print("3 - Usar equipamento/item")
            print("4 - Equipar / desequipar")
            print("5 - Craft / Construir itens")
            print("6 - Loja")
            print("7 - Melhorar equipamentos")
            print("8 - Criaturas e montarias")
            print("9 - Ler notas de explorador")
            print("10 - Sobrevivência / comer / beber")
            print("11 - Voltar")

            escolha = input("\nEscolha: ")

            if escolha == "1":
                self.mostrar_inventario()

            elif escolha == "2":
                self.remover_item_menu()

            elif escolha == "3":
                self.mostrar_inventario()
                itens_unicos = list(dict.fromkeys(self.inventario))
                if itens_unicos:
                    try:
                        numero = int(input("\nNúmero do item: "))
                        self.usar_item(numero)
                    except ValueError:
                        print("\nDigite um número!")

            elif escolha == "4":
                self.menu_equipamentos()

            elif escolha == "5":
                self.sistema_craft()

            elif escolha == "6":
                self.loja()

            elif escolha == "7":
                self.melhorar_equipamentos()

            elif escolha == "8":
                while True:
                    print("\n==============================")
                    print("     CRIATURAS E MONTARIAS")
                    print("==============================")
                    print("1 - Ver criaturas")
                    print("2 - Montar criatura")
                    print("3 - Embarcar criatura na Jangada")
                    print("4 - Voltar")

                    op = input("\nEscolha: ")

                    if op == "1":
                        self.mostrar_criaturas()
                    elif op == "2":
                        self.montar_criatura()
                    elif op == "3":
                        self.embarcar_na_jangada()
                    elif op == "4":
                        break
                    else:
                        print("\nOpção inválida!")

            elif escolha == "9":
                ler_notas_explorador(self)

            elif escolha == "10":
                self.menu_sobrevivencia()

            elif escolha == "11":
                break

            else:
                print("\nOpção inválida!")



# CLASSE INIMIGO


class Inimigo:

    def __init__(self, nome, hp, dano, agilidade, ouro, xp):
        self.nome = nome
        self.hp = hp
        self.dano = dano
        self.agilidade = agilidade
        self.ouro = ouro
        self.xp = xp
        self.sangramento = False
        self.defesa = 0
        self.servos = 0
        self.rugido_ativo = False
        self.atordoado = False



# CLASSE CRIATURA


class Criatura:

    def __init__(self, nome, hp, dano, agilidade, xp, alimento, quantidade_domar):
        self.nome = nome
        self.hp = hp
        self.dano = dano
        self.agilidade = agilidade
        self.xp = xp
        self.alimento = alimento
        self.quantidade_domar = quantidade_domar



# HISTÓRIA


def historia():
    print("\n" + "=" * 58)
    print("                    RAGNAROCK")
    print("              CRÔNICAS DO FIM DA TERRA")
    print("=" * 58)

    input("\nAperte ENTER para iniciar a transmissão...")

 cenas = [
        ("ANO 3500",
         "A umanidade estava sem salvação, recuros naturais estavame se esgotando e a maior parte da vida animal ja havia sido extinta a muito tempo, se nao fizecem algo rapido o planeta terra estaria condenado."),
        ("O ELEMENTO",
         "em um observatorio, cientistas avistararam um elemento misterioso entrando na atmosfera da terra, apos cair, cientistas de todo o mundo e governos começarama estudar."),
        ("O NÚCLEO",
         "o nucleo deste elemento misterioso é capaz de mudar a propria materia, podendo ser usado para poder e conquistação mundial, sendo possivel usar esta força como arma."),
        ("A GUERRA",
         "Duas grandes nações, ragnar e valgueiro, começaram uma guerra para decidir quem ficara com o elemento misterioso."),
        ("A QUEDA",
         "As armas alimentadas pelo elemento destruíram cidades, oceanos e continentes, acabando por vez a posibilidade de vidas existirem no planeta terra."),
        ("AS QUATRO ARCAS",
         "Os últimos cientistas construíram quatro arcas espaciais chamadas RAGNAROCK."),
        ("OS CLONES",
         "Cada arca carregava recursos, tecnologia e clones humanos para reconstruir a espécie."),
        ("O HOLOGRAMA",
         "Para preservar as memórias, consciências holográficas foram copiadas de pessoas que já existiram."),
        ("O DESPERTAR",
         "Você desperta na RAGNAROCK I, dentro de um holograma humano."),
        ("A SOLIDÃO",
         "Não há outros humanos vivos nesta Arca. Só você, as criaturas alteradas com o elemento misterioso, e a inteligência artificial HELENA."),
        ("HELENA",
         "HELENA controla os sistemas da Arca, vende equipamentos e preserva registros deixados pelos antigos exploradores."),
        ("A VIDA SELVAGEM",
         "a energia do Núcleo alterou a vida da Terra. Criaturas antigas e novas espécies agora dominam as ruínas."),
        ("A MISSÃO",
         "Explore, evolua, domestique criaturas e descubra como chegar à próxima Arca."),
        ("O GUARDIÃO",
         "um Dragão carregado de energia do Núcleo protege a saída da RAGNAROCK I."),
        ("O FUTURO",
         "derrotar o Dragão liberará o caminho para a RAGNAROCK II."),
    ]

    for titulo, texto in cenas:
        print("\n" + "-" * 58)
        print(f"                  {titulo}")
        print("-" * 58)
        print(texto)
        time.sleep(0.9)

    print("\n" + "=" * 58)
    print("                 TRANSMISSÃO ENCERRADA")
    print("=" * 58)
    input("\nAperte ENTER para despertar na RAGNAROCK I...")



# MENU PRINCIPAL


def jogar():
    while True:
        print("\n==============================")
        print("        RAGNAROCK")
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



# INÍCIO


def inicio():
    historia()

    print("\nBem-vindo à RAGNAROCK I.")

    nome = input("\nDigite o nome da consciência holográfica: ")

    classes = ["guerreiro", "arqueiro", "escudeiro"]

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
    personagem.adicionar_item("Carne crua", 4)
    personagem.adicionar_item("Madeira", 5)
    personagem.adicionar_item("Fibra", 8)
    personagem.adicionar_item("Aço reforçado", 2)

    print("\n==============================")
    print("        PERSONAGEM")
    print("==============================")

    print(f"\nConsciência holográfica: {personagem.nome}")
    print("Origem: clone humano da RAGNAROCK I")
    print(f"Arca atual: RAGNAROCK {personagem.arca_atual}")
    print(f"Classe: {personagem.classe}")
    print(f"Nível: {personagem.nivel}")
    print(f"HP: {personagem.hp}")
    print(f"Dano: {personagem.danobase}")
    print(f"Agilidade: {personagem.agilidadebase}")

    input("\nAperte ENTER para continuar...")

    mundo(personagem)


# MUNDO / MAPA

def mundo(personagem):
    while True:
        print("\n========================================")
        print("              MAPA")
        print("========================================")
        print(f"          RAGNAROCK {personagem.arca_atual} - SETOR EXTERNO")

        print(f"\nNível: {personagem.nivel}")
        print(f"XP: {personagem.xp}/{personagem.xp_proximo_nivel}")
        print(f"HP: {personagem.hp}/{personagem.hp_max}")
        print(f"Dano: {personagem.danobase}")
        print(f"Ouro: {personagem.ouro}")
        print(f"Montaria: {personagem.montaria_atual or 'Nenhuma'}")

        print("\nÁreas disponíveis:")
        print("1 - Floresta obscura")
        print("2 - Vilarejo abandonado")
        print("3 - Ruínas da antiga Aetéria")
        print("4 - Covil do Dragão")
        print("5 - Oceano")
        print("6 - Região de gelo extremo")
        print("7 - Abrir inventário")
        print("8 - Sair do jogo")

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
            fim = explorar("ruínas da antiga Aetéria", personagem)
            if fim:
                return

        elif escolha == "4":
            print("\nVocê está entrando no Covil do Dragão...")
            time.sleep(1)
            fim = explorar("covil do dragão", personagem)
            if fim:
                return

        elif escolha == "5":
            fim = explorar("oceano", personagem)
            if fim:
                return

        elif escolha == "6":
            fim = explorar("gelo", personagem)
            if fim:
                return

        elif escolha == "7":
            personagem.menu_inventario()

        elif escolha == "8":
            print("\nSaindo do jogo...")
            return

        else:
            print("\nOpção inválida!")


# EXPLORAÇÃO

def clima_aleatorio(personagem, local):
    evento = random.randint(1, 100)
    if local == "gelo" and evento <= 30:
        print("\n!!! TEMPESTADE DE GELO !!!")
        print("A neve congela o ar ao seu redor e a visibilidade cai drasticamente.")
        if personagem.armadura != "Roupa de pelo grosso":
            personagem.hipotermia += 15
            print(f"Hipotermia aumentou para {personagem.hipotermia}%.")
    elif local != "oceano" and evento <= 25:
        print("\n>>> CHUVA <<<")
        print("Uma chuva forte começa a cair sobre a região.")
    else:
        print("\nO clima permanece estável por enquanto.")


def encontrar_riacho(personagem):
    print("RIACHO")
    print("Você encontrou um riacho de água aparentemente limpa.")
    escolha = input("\nDeseja coletar água? (s/n): ").lower()
    if escolha == "s":
        qtd = random.randint(1, 3)
        personagem.adicionar_item("Água", qtd)
        print(f"Você coletou {qtd}x Água.")
    else:
        print("Você decidiu não coletar água.")


def explorar(local, personagem):
    print("EXPLORAÇÃO")
    personagem.area_atual = local
    print(f"\nVocê está explorando: {local}...")
    personagem.atualizar_sobrevivencia(1)
    clima_aleatorio(personagem, local)
    time.sleep(0.5)

    if personagem.hp <= 0:
        print("\nVocê não consegue continuar por causa das condições de sobrevivência.")
        return True

    if local == "covil do dragão" and personagem.nivel < 30:
        print("\nHELENA: você não está pronto para a batalha final.")
        print(f"Nível atual: {personagem.nivel}/30.")
        print("O combate contra o Dragão será liberado somente a partir do nível 30.")
        return False

    if local == "covil do dragão" and not personagem.criaturas["Yutirano"]["domado"]:
        print("\nHELENA: acesso bloqueado. Um Yutirano domado é necessário para enfrentar o Dragão.")
        return False

    if local == "gelo" and not personagem.verificar_frio("gelo"):
        return True

    if local != "oceano" and random.randint(1, 100) <= 20:
        encontrar_riacho(personagem)

    if random.randint(1, 100) <= 22:
        encontrar_estrutura_abandonada(personagem, local)

    if random.randint(1, 100) <= 55:
        encontrar_recurso(local, personagem)

    if local == "oceano":
        if random.randint(1, 100) <= 20:
            encontrar_caverna_oceano(personagem)
        montarias_marinhas = {"Ictiossauro", "Plesiossauro", "Megalodonte", "Liopleurodon", "Mossassauro"}
        if personagem.montaria_atual not in montarias_marinhas:
            if personagem.quantidade_item("Jangada") <= 0:
                print("\nSem Jangada ou montaria marinha, você só consegue explorar águas rasas.")
            else:
                print("\nVocê coloca a Jangada no oceano e consegue avançar.")
                if personagem.criatura_na_jangada:
                    print(f"Você está levando {personagem.criatura_na_jangada} como passageiro.")

    if random.randint(1, 100) <= 70:
        resultado = encontro_criatura(local, personagem)
        if resultado:
            return resultado

    if local not in ("gelo", "oceano", "covil do dragão") and random.randint(1, 100) <= 60:
        return adversario(local, personagem)

    if local == "gelo" and random.randint(1, 100) <= 40:
        return adversario(local, personagem)

    print("\nA região ficou silenciosa. Você não encontrou nenhuma ameaça.")
    caminhar(personagem)
    return False


def encontrar_recurso(local, personagem):
    print("RECURSOS ENCONTRADOS")

    if local == "oceano":
        item = random.choice(["Fibra", "Pele", "Carne crua", "Metal"])
        if item == "Metal":
            minerar_rocha(personagem)
        else:
            personagem.adicionar_item(item)
            print(f"\nVocê encontrou: {item}!")
        return

    if local in ("floresta obscura", "vilarejo", "ruínas da antiga Aetéria", "gelo"):
        evento = random.randint(1, 100)
        if local == "floresta obscura" and evento <= 45:
            if evento <= 25:
                coletar_planta(personagem)
            else:
                cortar_arvore(personagem)
            return
        if local == "gelo" and evento <= 25:
            minerar_rocha(personagem)
            return
        if evento <= 45:
            minerar_rocha(personagem)
            return

    item = random.choice(["Fibra", "Pele", "Metal", "Aço reforçado"] if local != "gelo" else ["Fibra", "Pele", "Pelo grosso"])
    personagem.adicionar_item(item)
    print(f"\nVocê encontrou: {item}!")


def coletar_planta(personagem):
    print("\n================================")
    print("           ARBUSTO")
    print("================================")
    escolha = input("\nVocê encontrou um arbusto com frutos. Deseja coletá-lo? (s/n): ").lower()
    if escolha != "s":
        print("Você deixou o arbusto intacto.")
        return

    frutas = [("Mejoberry", 50), ("Amarberry", 25), ("Azulberry", 25)]
    fruta = random.choices([x[0] for x in frutas], weights=[x[1] for x in frutas], k=1)[0]
    personagem.adicionar_item(fruta, random.randint(2, 5))
    if random.randint(1, 100) <= 60:
        personagem.adicionar_item("Fibra", random.randint(2, 6))
    print("\nO arbusto também forneceu algumas fibras.")


def socar_arvore(personagem):
    print("\nVocê decidiu usar as próprias mãos para quebrar a árvore.")
    while personagem.hp > 0:
        personagem.hp = max(0, personagem.hp - 1)
        personagem.adicionar_item("Madeira", 1)
        print(f"Você socou a árvore: -1 HP, +1 Madeira. HP: {personagem.hp}/{personagem.hp_max}")
        if input("Deseja dar outro soco? (s/n): ").lower() != "s":
            break


def cortar_arvore(personagem):
    print("\n================================")
    print("            ÁRVORE")
    print("================================")
    escolha = input("\nDeseja quebrar a árvore para conseguir Madeira? (s/n): ").lower()
    if escolha != "s":
        print("Você decidiu não quebrar a árvore.")
        return
    if personagem.quantidade_item("Machado") <= 0:
        print("\nVocê não possui Machado. Poderá quebrar a árvore com os punhos, sofrendo 1 dano por batida.")
        socar_arvore(personagem)
        return
    qtd = random.randint(4, 7)
    personagem.adicionar_item("Madeira", qtd)
    print(f"\nO Machado rendeu {qtd}x Madeira.")


def minerar_rocha(personagem):
    print("\n================================")
    print("            ROCHA")
    print("================================")
    escolha = input("\nDeseja quebrar a rocha para coletar Metal? (s/n): ").lower()
    if escolha != "s":
        print("Você deixou a rocha para trás.")
        return
    if personagem.quantidade_item("Picareta") <= 0:
        print("\nVocê não possui uma Picareta e não consegue quebrar esta rocha.")
        return
    qtd = random.randint(2, 5)
    personagem.adicionar_item("Metal", qtd)
    print(f"\nVocê extraiu {qtd}x Metal de uma rocha.")


def encontrar_estrutura_abandonada(personagem, local):
    print("ESTRUTURA ABANDONADA")

    estruturas = {
        "floresta obscura": "um posto de observação coberto por raízes",
        "vilarejo": "uma estação médica abandonada",
        "ruínas da antiga Aetéria": "um laboratório destruído",
        "oceano": "um observatório costeiro inundado",
        "gelo": "uma estação científica congelada",
    }
    print(f"\nVocê encontrou {estruturas.get(local, 'uma estrutura esquecida')}.")
    if random.randint(1, 100) <= 75:
        nota = random.choice([
            "Nota de Explorador #01", "Nota de Explorador #02",
            "Nota de Explorador #03", "Nota de Explorador #04",
            "Nota de Explorador #05"
        ])
        if nota not in personagem.notas_explorador:
            personagem.notas_explorador.append(nota)
            print(f"\n>>> {nota} adicionada às suas Notas de Explorador! <<<")
        personagem.estrutura_encontrada += 1
        personagem.ativar_boost_xp(60)
    else:
        print("A estrutura estava vazia, mas havia materiais úteis.")
        personagem.adicionar_item("Fibra", 3)


def ler_notas_explorador(personagem):
    notas = personagem.notas_explorador
    if not notas:
        print("\nVocê não possui notas de explorador.")
        return
    textos = {
        "Nota de Explorador #01": "Os Raptores caçam em bando. Quanto maior o bando, melhor a coordenação e maior o dano.",
        "Nota de Explorador #02": "O T-Rex provoca ferimentos profundos. O sangramento pode continuar depois da mordida.",
        "Nota de Explorador #03": "O oceano possui criaturas rápidas e predadores gigantes. O Ictiossauro é veloz e seu CHACOALHAR pode atordoar uma criatura marinha.",
        "Nota de Explorador #04": "Mamutes, rinocerontes lanudos e Yutiranos dominam o gelo. O pelo grosso dessas criaturas pode ser usado para fabricar uma roupa capaz de proteger contra o frio extremo.",
        "Nota de Explorador #05": "O Yutirano lidera Carnotauros. Seu rugido aumenta o poder dos servos. Uma anotação diz: 'O Dragão parece ser vulnerável à mesma força.'",
    }
    print("\n==============================")
    print("       NOTAS DE EXPLORADOR")
    print("==============================")
    for nota in notas:
        print(f"\n{nota}:\n{textos.get(nota, 'Trechos apagados pelo tempo.')}")

# ENCONTRO COM CRIATURAS

def criaturas_da_area(local):
    if local == "floresta obscura":
        if random.randint(1, 100) <= 40:
            return [Criatura("Raptor", 150, 28, 40, 180, "Carne crua", 3)
                    for _ in range(random.randint(2, 4))]
        return [Criatura("Raptor", 150, 28, 40, 180, "Carne crua", 3)]

    if local == "vilarejo":
        return [Criatura("T-Rex", 450, 55, 10, 420, "Carne crua", 6)]

    if local == "oceano":
        opcoes = [
            Criatura("Ictiossauro", 110, 14, 65, 100, "Carne crua", 2),
            Criatura("Plesiossauro", 170, 22, 38, 150, "Carne crua", 3),
            Criatura("Megalodonte", 240, 32, 32, 230, "Carne crua", 4),
            Criatura("Liopleurodon", 300, 38, 28, 300, "Carne crua", 5),
            Criatura("Mossassauro", 650, 70, 22, 750, "Carne crua", 10),
        ]
        if random.randint(1, 100) <= 12:
            return [opcoes[-1]]
        return [random.choice(opcoes)]

    if local == "gelo":
        if random.randint(1, 100) <= 15:
            return [Criatura("Yutirano", 700, 70, 15, 900, "Carne crua", 12)]
        rolagem = random.randint(1, 100)
        if rolagem <= 35:
            return [Criatura("Mamute", 380, 45, 10, 350, "Mejoberry", 8)]
        if rolagem <= 65:
            return [Criatura("Rinoceronte lanudo", 420, 55, 12, 420, "Mejoberry", 10)]
        return [Criatura("Smilodonte", 230, 38, 45, 300, "Carne crua", 5)]

    if local == "ruínas da antiga Aetéria":
        return [Criatura("Carnotauro", 320, 40, 30, 350, "Carne crua", 5)]

    return []


def encontro_criatura(local, personagem):
    criaturas = criaturas_da_area(local)
    if not criaturas:
        return False

    principal = criaturas[0]
    nome = principal.nome
    bando = len(criaturas)

    print("CRIATURA SELVAGEM ENCONTRADA")
    print(f"\nCriatura: {nome}")
    print(f"Quantidade no encontro: {bando}")
    print(f"HP individual: {principal.hp}")
    print(f"Dano individual: {principal.dano}")

    if nome == "Raptor" and bando >= 2:
        bonus = 10 + (bando - 2) * 5
        print(f"\nBÔNUS DE BANDO: +{bonus}% dano para o grupo de Raptores.")

    if nome == "Yutirano":
        return encontro_yutirano(personagem, principal)

    print("\n1 - Tentar domesticar")
    print("2 - Enfrentar")
    print("3 - Fugir")
    escolha = input("\nEscolha: ")

    if escolha == "1":
        resultado = tentar_domesticar(personagem, principal, bando=bando)
        if resultado == "domado":
            for _ in range(bando - 1):
                print("\nOutro Raptor do bando continua selvagem...")
            return True
        if resultado == "fugiu":
            return False
        escolha = input("\nDeseja enfrentar? (s/n): ").lower()
        if escolha != "s":
            return False
    elif escolha == "3":
        print("\nVocê fugiu.")
        return False
    elif escolha != "2":
        print("\nOpção inválida.")
        return False

    multiplicador_bando = 1 + max(0, bando - 1) * 0.10
    inimigo = Inimigo(
        nome,
        principal.hp * bando,
        round(principal.dano * multiplicador_bando),
        principal.agilidade,
        0,
        principal.xp * bando
    )
    inimigo.sangramento = nome in ("T-Rex", "Smilodonte")
    venceu = batalha(personagem, inimigo)
    return venceu


def encontro_yutirano(personagem, criatura):
    print("YUTIRANO + 3 CARNOTAUROS")
    print("\nO Yutirano solta um rugido de guerra!")
    print("Os 3 Carnotauros servos recebem DOBRO de dano e DOBRO de defesa.")
    print("\n1 - Enfrentar o grupo")
    print("2 - Fugir")
    escolha = input("\nEscolha: ")
    if escolha != "1":
        return False

    inimigo = Inimigo("Yutirano", 900, 75, 15, 700, 900)
    inimigo.defesa = 30
    inimigo.servos = 3
    inimigo.rugido_ativo = True
    return batalha(personagem, inimigo)


def requisitos_domesticar(personagem, nome):
    dados = personagem.criaturas.get(nome, {})
    if nome == "Raptor":
        return (
            personagem.nivel >= 8,
            personagem.quantidade_item("Boleadeira") > 0,
            personagem.quantidade_item("Flecha sedativa") > 0,
            personagem.quantidade_item("Carne crua") >= 3,
        )
    if nome == "T-Rex":
        return (
            personagem.nivel >= 10,
            personagem.quantidade_item("Armadilha de urso grande") > 0,
            personagem.quantidade_item("Flecha sedativa") > 0,
            personagem.quantidade_item("Carne crua") >= 6,
        )
    if nome == "Ictiossauro":
        return (personagem.nivel >= 6, personagem.quantidade_item("Carne crua") >= 2)
    if nome == "Mossassauro":
        return (
            personagem.nivel >= 15,
            personagem.quantidade_item("Roupa de mergulho") > 0,
            personagem.criaturas["Ictiossauro"]["domado"],
            personagem.quantidade_item("Flecha sedativa") > 0,
            personagem.quantidade_item("Carne crua") >= 10,
        )
    if nome in ("Plesiossauro", "Megalodonte", "Liopleurodon"):
        return (
            personagem.nivel >= dados.get("nivel_sela", 99),
            personagem.quantidade_item("Flecha sedativa") > 0,
            personagem.quantidade_item("Carne crua") >= 3,
        )
    if nome in ("Mamute", "Rinoceronte lanudo"):
        possui_fruta = any(
            personagem.quantidade_item(fruta) >= 5
            for fruta in ("Mejoberry", "Amarberry", "Azulberry")
        )
        return (personagem.nivel >= 10, possui_fruta)
    if nome == "Smilodonte":
        return (personagem.nivel >= 11, personagem.quantidade_item("Flecha sedativa") > 0, personagem.quantidade_item("Carne crua") >= 5)
    if nome == "Carnotauro":
        return (personagem.nivel >= 10, personagem.quantidade_item("Flecha sedativa") > 0, personagem.quantidade_item("Carne crua") >= 5)
    if nome == "Yutirano":
        return (personagem.nivel >= 16, personagem.quantidade_item("Flecha sedativa") > 0, personagem.quantidade_item("Carne crua") >= 12)
    return (False,)


def atirar_flecha_sedativa(personagem, nome):
    if personagem.arma not in ("Arco", "Besta"):
        print("\nVocê precisa estar com Arco ou Besta equipada.")
        return False
    if personagem.quantidade_item("Flecha sedativa") <= 0:
        print("\nVocê não possui Flecha sedativa.")
        return False
    personagem.remover_item("Flecha sedativa")
    impacto = 45 if personagem.arma == "Arco" else 75
    print(f"\nVocê disparou uma Flecha Sedativa com a {personagem.arma}.")
    print(f"Impacto da arma: {impacto}. A criatura caiu inconsciente.")
    return True


def tentar_domesticar(personagem, criatura, bando=1):
    nome = criatura.nome
    dados = personagem.criaturas.get(nome)
    if not dados:
        print("\nEssa criatura não pode ser domesticada.")
        return "nao_preparado"

    print("\n================================")
    print("      PREPARANDO DOMESTICAÇÃO")
    print("================================")

    requisitos = requisitos_domesticar(personagem, nome)
    if not all(requisitos):
        print("\nVocê ainda não possui todos os requisitos.")
        return "nao_preparado"

    if nome == "Raptor":
        personagem.remover_item("Boleadeira")
        print("\nA Boleadeira prendeu o Raptor.")
    elif nome == "T-Rex":
        personagem.remover_item("Armadilha de urso grande")
        print("\nA Armadilha de Urso Grande prendeu o T-Rex.")
    elif nome == "Mossassauro":
        print("\nVocê veste a roupa de mergulho e entra na água com seu Ictiossauro.")
    elif nome in ("Mamute", "Rinoceronte lanudo"):
        print("\nVocê se aproxima devagar e oferece frutos.")
        frutas = [fruta for fruta in ("Mejoberry", "Amarberry", "Azulberry") if personagem.quantidade_item(fruta) >= 5]
        if not frutas:
            print("Você precisa de pelo menos 5 frutos para domesticar.")
            return "nao_preparado"
        print("Escolha a fruta para a domesticação:")
        for i, fruta in enumerate(frutas, 1):
            print(f"{i} - {fruta} ({personagem.quantidade_item(fruta)} disponíveis)")
        try:
            escolha_fruta = int(input("Escolha: "))
            fruta_escolhida = frutas[escolha_fruta - 1]
        except (ValueError, IndexError):
            print("Opção inválida.")
            return "nao_preparado"
        return processo_domesticacao(personagem, criatura, fruta_escolhida, 5)

    if nome == "Ictiossauro":
        return processo_domesticacao(personagem, criatura, "Carne crua", 2)

    if not atirar_flecha_sedativa(personagem, nome):
        return "nao_preparado"

    quantidade = criatura.quantidade_domar
    if nome == "Raptor":
        quantidade = 3
    elif nome == "T-Rex":
        quantidade = 6
    elif nome == "Mossassauro":
        quantidade = 10
    elif nome == "Yutirano":
        quantidade = 12
    elif bando > 1:
        quantidade = criatura.quantidade_domar

    return processo_domesticacao(personagem, criatura, "Carne crua", quantidade)


def processo_domesticacao(personagem, criatura, alimento, quantidade):
    nome = criatura.nome
    print("\n================================")
    print(f"      {nome.upper()} INCONSCIENTE")
    print("================================")
    print(f"\nVocê precisa fornecer {quantidade}x {alimento}.")
    print("A criatura permanecerá inconsciente por 5 ações.")

    tempo_restante = 5
    colocados = 0
    while tempo_restante > 0 and colocados < quantidade:
        print(f"\nTempo restante: {tempo_restante} ações")
        print(f"Alimento fornecido: {colocados}/{quantidade}")
        print("1 - Colocar alimento")
        print("2 - Esperar")
        print("3 - Desistir")
        escolha = input("\nEscolha: ")

        if escolha == "1":
            if personagem.quantidade_item(alimento) <= 0:
                print(f"\nVocê não possui {alimento}.")
                continue
            personagem.remover_item(alimento)
            colocados += 1
            tempo_restante -= 1
        elif escolha == "2":
            tempo_restante -= 1
            print("\nVocê espera...")
        elif escolha == "3":
            print("\nVocê abandonou a domesticação.")
            return "fugiu"
        else:
            print("\nOpção inválida!")

    if colocados < quantidade:
        print("\nA criatura acordou antes de ser domada!")
        return "fugiu"

    dados = personagem.criaturas[nome]
    dados["domado"] = True
    dados["quantidade"] = dados.get("quantidade", 0) + 1
    print("\n" + "=" * 50)
    print(f"       {nome.upper()} DOMADO!")
    print("=" * 50)
    print(f"Você agora possui {dados['quantidade']} {nome}(s) domado(s).")
    if nome == "Raptor" and dados["quantidade"] >= 2:
        print("BÔNUS DE BANDO DOS RAPTORES ATIVO: dano aumentado.")
    if nome == "Mamute" and dados["quantidade"] >= 2:
        print("RUGIDO DO MAMUTE: resistência do bando aumentada.")
    personagem.ganhar_xp(180 if nome not in ("Mossassauro", "Yutirano") else 600)
    return "domado"

# INIMIGOS NORMAIS

def adversario(local, personagem):
    if local == "floresta obscura":
        inimigo = Inimigo("Lobo mutante", 80, 15, 25, 75, 70)
    elif local == "vilarejo":
        inimigo = Inimigo("Goblin scavenger", 100, 20, 35, 100, 90)
    elif local == "ruínas da antiga Aetéria":
        inimigo = Inimigo("Guardião das Ruínas", 180, 30, 15, 150, 150)
    elif local == "gelo":
        if random.randint(1, 100) <= 60:
            inimigo = Inimigo("Carnotauro", 320, 45, 30, 180, 280)
        else:
            inimigo = Inimigo("Tempestade de Gelo", 120, 25, 10, 50, 100)
    elif local == "covil do dragão":
        if personagem.nivel < 30:
            print("\nHELENA: você não está pronto para a batalha final. Alcance o nível 30.")
            return False
        if not personagem.criaturas["Yutirano"]["domado"]:
            print("\nHELENA: o guardião final exige um Yutirano domado.")
            return False
        inimigo = Inimigo("DRAGÃO", 300, 40, 10, 500, 600)
    else:
        return False

    print("INIMIGO ENCONTRADO")
    print(f"\nInimigo: {inimigo.nome}")
    print(f"HP: {inimigo.hp}")
    print(f"Dano: {inimigo.dano}")
    print(f"XP: {inimigo.xp}")
    input("\nAperte ENTER para lutar...")
    return batalha(personagem, inimigo)

# BATALHA

def batalha(personagem, inimigo):
    if inimigo.nome == "DRAGÃO" and not personagem.criaturas["Yutirano"]["domado"]:
        print("\nSem um Yutirano domado, você não consegue sobreviver à energia do Dragão.")
        return False

    while personagem.hp > 0 and inimigo.hp > 0:
        print("BATALHA")
        print(f"\n{personagem.nome}")
        print(f"HP: {personagem.hp}/{personagem.hp_max}")
        print(f"Dano: {personagem.danobase}")
        print(f"Nível: {personagem.nivel}")
        if personagem.montaria_atual:
            print(f"Montaria: {personagem.montaria_atual}")
        print(f"\n{inimigo.nome}")
        print(f"HP: {inimigo.hp}")
        if inimigo.servos:
            print(f"Carnotauros servos restantes: {inimigo.servos}")

        print("\n1 - Atacar")
        print("2 - Recuar")
        print("3 - Inventário")
        if personagem.montaria_atual == "Ictiossauro" and inimigo.nome != "DRAGÃO":
            print("4 - Chacoalhar")

        escolha = input("\nEscolha: ")

        if escolha == "1":
            atacar(personagem, inimigo)
            if inimigo.hp > 0:
                if inimigo.servos > 0:
                    inimigo.servos -= 1
                    print("\nUm Carnotauro servo caiu!")
                if not inimigo.atordoado:
                    ataque_inimigo(personagem, inimigo)
        elif escolha == "2":
            print("\nVocê recuou!")
            return False
        elif escolha == "3":
            personagem.menu_inventario()
        elif escolha == "4" and personagem.montaria_atual == "Ictiossauro":
            inimigo.atordoado = True
            print("\nCHACOALHAR! A criatura fica atordoada e perde o próximo turno.")
        else:
            print("\nOpção inválida!")

        if inimigo.atordoado:
            inimigo.atordoado = False

    if personagem.hp <= 0:
        print("VOCÊ MORREU")
        if inimigo.nome == "DRAGÃO":
            print("O Dragão venceu. A passagem para a próxima Arca continua bloqueada.")
        return True

    if inimigo.hp <= 0:
        print("VOCÊ VENCEU!")
        print(f"\nVocê derrotou {inimigo.nome}!")
        personagem.ouro += inimigo.ouro
        personagem.ganhar_xp(inimigo.xp)

        if inimigo.nome != "DRAGÃO":
            pegar_carne = input("\nDeseja coletar a carne da criatura? (s/n): ").lower()
            if pegar_carne == "s":
                personagem.adicionar_item("Carne crua", random.randint(1, 3))
                if random.randint(1, 100) <= 45:
                    personagem.adicionar_item("Carne podre")
            else:
                print("Você deixou a carne para trás.")

            if inimigo.nome in ("Mamute", "Rinoceronte lanudo", "Yutirano"):
                qtd_pelo = random.randint(3, 6)
                personagem.adicionar_item("Pelo grosso", qtd_pelo)
                personagem.adicionar_item("Pele", random.randint(1, 3))
                print(f"\nA criatura possuía pelo grosso. Você conseguiu {qtd_pelo}x Pelo grosso!")

        if inimigo.nome == "DRAGÃO":
            personagem.dragao_derrotado = True
            print("\n" + "=" * 58)
            print("                 DRAGÃO DERROTADO!")
            print("=" * 58)
            print("\nO Yutirano rugiu ao seu lado.")
            print("[HELENA] GUARDIÃO ELIMINADO.")
            print("[HELENA] ACESSO À RAGNAROCK II: LIBERADO.")
            print("\n" + "=" * 58)
            print("                 TO BE CONTINUED...")
            print("=" * 58)
            print("\nA RAGNAROCK II aguarda.")
            return True

        caminhar(personagem)
    return False

# ATAQUE

def atacar(personagem, inimigo):
    dano = personagem.danobase
    if personagem.arma == "Besta":
        dano += 35
    elif personagem.arma == "Arco":
        dano += 20

    if personagem.montaria_atual == "Raptor":
        qtd = personagem.criaturas["Raptor"].get("quantidade", 0)
        dano += 15
        if qtd >= 2:
            dano = round(dano * (1 + 0.10 + max(0, qtd - 2) * 0.05))
            print("\nBÔNUS DE BANDO DOS RAPTORES!")
    elif personagem.montaria_atual == "T-Rex":
        dano += 25
        print("\nMordida do T-Rex: efeito de sangramento.")
    elif personagem.montaria_atual == "Smilodonte":
        dano += 18
        print("\nAs presas do Smilodonte: efeito de sangramento.")
    elif personagem.montaria_atual == "Mossassauro":
        dano += 35
    elif personagem.montaria_atual == "Ictiossauro":
        dano += 8
    elif personagem.montaria_atual == "Mamute":
        dano += 25
    elif personagem.montaria_atual == "Rinoceronte lanudo":
        dano += 30
    elif personagem.montaria_atual == "Yutirano":
        dano += 30

    if random.randint(1, 100) <= 20:
        dano *= 2
        print("\n!!! ATAQUE CRÍTICO !!!")

    dano = max(1, dano - getattr(inimigo, "defesa", 0))
    inimigo.hp = max(0, inimigo.hp - dano)
    print(f"\nVocê causou {dano} de dano!")
    print(f"HP do {inimigo.nome}: {inimigo.hp}")

# ATAQUE DO INIMIGO

def ataque_inimigo(personagem, inimigo):
    desvio = random.randint(1, 100)
    if desvio <= min(personagem.agilidadebase, 80):
        print("\nVocê desviou do ataque!")
        return

    dano_original = inimigo.dano
    if inimigo.nome == "Yutirano" and inimigo.rugido_ativo:
        dano_original *= 2
        print("\nO rugido do Yutirano aumenta o dano dos aliados!")
    if personagem.montaria_atual == "Mamute" and personagem.criaturas["Mamute"].get("quantidade", 0) >= 2:
        dano_original = round(dano_original * 0.75)
        print("\nRUGIDO DO MAMUTE: resistência do bando ativa!")
    dano_reduzido = dano_original * (1 - personagem.resistencia_escudo / 100)
    dano_final = max(1, round(dano_reduzido))
    personagem.hp = max(0, personagem.hp - dano_final)
    if inimigo.sangramento:
        personagem.hp = max(0, personagem.hp - 5)
        print("\nSANGRAMENTO! -5 HP adicional.")
    print(f"\n{inimigo.nome} causou {dano_final} de dano!")
    print(f"Seu HP: {personagem.hp}/{personagem.hp_max}")

# CAMINHADA

def caminhar(personagem):
    print("CAMINHANDO")
    tempo = random.randint(1, 3)
    if personagem.montaria_atual:
        print(f"\nVocê avança montado em {personagem.montaria_atual}.")
    else:
        print("\nVocê continua sua jornada a pé.")
    for i in range(tempo):
        print(f"\nCaminhando... {i+1}/{tempo}")
        personagem.atualizar_sobrevivencia(1)
        personagem.estado_xp()
        if personagem.hp <= 0:
            print("\nVocê caiu durante a caminhada por falta de comida ou água.")
            return
        time.sleep(0.4)
    
    clima_aleatorio(personagem, personagem.area_atual)
    if personagem.area_atual != "oceano" and random.randint(1, 100) <= 15:
        encontrar_riacho(personagem)
    if random.randint(1, 100) <= 55:
        encontrar_recurso(personagem.area_atual, personagem)
    evento = random.randint(1, 100)
    if evento <= 15:
        encontrar_loja(personagem)
    elif evento <= 30:
        encontrar_estrutura_abandonada(personagem, personagem.area_atual)
    if random.randint(1, 100) <= 60:
        encontrar_bau(personagem)

    print("\nVocê terminou sua caminhada.")


def encontrar_loja(personagem):
    print("LOJA ENCONTRADA!")
    print("Um terminal abandonado acende. Uma voz sintética surge dos alto-falantes.")
    print("HELENA: Conexão comercial restaurada.")

    while True:
        escolha = input("\nDeseja entrar na loja? (s/n): ")

        if escolha == "s":
            personagem.loja()
            break

        elif escolha == "n":
            print("\nVocê continuou caminhando.")
            break

        else:
            print("\nDigite S ou N.")


# CAVERNA DO OCEANO

def encontrar_caverna_oceano(personagem):
    print("\n========================================")
    print("          CAVERNA SUBMERSA")
    print("========================================")
    print("\nUma caverna escura aparece sob as águas.")
    if personagem.quantidade_item("Roupa de mergulho") <= 0 and personagem.montaria_atual != "Ictiossauro":
        print("Você precisa de Roupa de Mergulho ou Ictiossauro para entrar.")
        return
    print("Você encontra Metal e uma antiga nota.")
    personagem.adicionar_item("Metal", random.randint(2, 5))
    personagem.adicionar_item("Fibra", random.randint(3, 6))
    if random.randint(1, 100) <= 50:
        if "Nota de Explorador #03" not in personagem.notas_explorador:
            personagem.notas_explorador.append("Nota de Explorador #03")
            print("\n>>> Nota de Explorador #03 adicionada às suas notas! <<<")

# BAÚ

def encontrar_bau(personagem):
    print("BAÚ!")

    print("\nVocê encontrou um baú no caminho!")

    escolha = input("\nDeseja abrir o baú? (s/n): ").lower()

    if escolha == "s":
        abrir_bau(personagem)
    else:
        print("\nVocê deixou o baú para trás.")

# ABRIR BAÚ

def abrir_bau(personagem):
    print("ABRINDO BAÚ...")
    time.sleep(1.0)

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
        "Carne crua",
        "Carne podre",
        "Mejoberry",
        "Flecha",
    ]

    chance_bom_ruim = random.randint(1, 100)
    if chance_bom_ruim <= 80:
        item = random.choice(itens)

        print("\n!!! VOCÊ ENCONTROU !!!")
        print(f"\n>>> {item} <<<")

        personagem.adicionar_item(item)

        print("\nO item foi guardado no seu inventário!")

    else:
        print("\nO tesouro parece estranho...")
        time.sleep(1.0)
        print("\nVocê abre o baú e uma armadilha é acionada!")
        personagem.hp = max(0, personagem.hp - 50)
        print("\nQue azar!")

# INICIAR

def iniciar_jogo():
    jogar()

if __name__ == "__main__":
    iniciar_jogo()
