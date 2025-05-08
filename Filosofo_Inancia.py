#inancia (starvation)
# Isso acontece porque o agendamento das threads pelo sistema operacional não é justo por padrão — ele não garante que todos rodem com a mesma frequência.

import threading #permite criar execuções paralelas (cada filósofo é uma thread)
import time #controla os tempos de pensar/comer
import os #usado para limpar a tela na exibição em tempo real

# Lista com os nomes dos filósofos
nomes = ["Platão", "Aristóteles", "Sócrates", "Descartes", "Kant"]

# Dicionário que guarda o estado atual de cada filósofo
# Pode ser: "Pensando 🧠" ou "Comendo 🍝"
estado_filosofo = {nome: "Pensando 🧠" for nome in nomes}

# Dicionário que conta quantas vezes cada filósofo comeu
contador_por_filosofo = {nome: 0 for nome in nomes}

# Lock para evitar que duas threads modifiquem os dados ao mesmo tempo
lock = threading.Lock()

# Classe que representa um filósofo (uma thread)
class Filosofo(threading.Thread):
    def __init__(self, nome, garfo_esquerdo, garfo_direito):
        super().__init__()
        self.nome = nome
        self.garfo_esquerdo = garfo_esquerdo
        self.garfo_direito = garfo_direito

    def run(self):
        # Ciclo infinito: pensar → comer → repetir
        while True:
            self.atualizar_estado("Pensando 🧠")
            time.sleep(1)  # Tempo de pensamento
            self.comer()

    # Atualiza o estado atual do filósofo (pensando ou comendo)
    def atualizar_estado(self, estado):
        with lock:
            estado_filosofo[self.nome] = estado

    # Lógica de comer (pegar garfos, comer, liberar garfos)
    def comer(self):
        # Estratégia para evitar deadlock:
        # filósofos em posições pares pegam primeiro o garfo esquerdo
        if nomes.index(self.nome) % 2 == 0:
            self.garfo_esquerdo.acquire()
            self.garfo_direito.acquire()
        else:
            self.garfo_direito.acquire()
            self.garfo_esquerdo.acquire()

        self.atualizar_estado("Comendo 🍝")
        time.sleep(1)  # Tempo comendo

        with lock:
            contador_por_filosofo[self.nome] += 1  # Conta mais uma refeição

        self.atualizar_estado("Pensando 🧠")

        # Libera os garfos
        self.garfo_esquerdo.release()
        self.garfo_direito.release()

# Thread que exibe o estado de todos os filósofos a cada 0.5 segundo
def exibir_estados():
    while True:
        time.sleep(0.5)
        with lock:
            # Limpa a tela (Windows ou Linux)
            os.system("cls" if os.name == "nt" else "clear")

            print("🧾 Estado atual dos filósofos:")
            for nome in nomes:
                print(f"- {nome:<10}: {estado_filosofo[nome]}")

            print("\n📊 Total de refeições:")
            for nome in nomes:
                print(f"- {nome:<10}: {contador_por_filosofo[nome]} vez(es)")

            print("\n(Atualizado a cada 0.5s)")

# Cria 5 garfos (semáforos com 1 permissão cada)
garfos = [threading.Semaphore(1) for _ in range(5)]

# Cria os 5 filósofos, cada um com um garfo à esquerda e outro à direita
filosofos = [
    Filosofo(nomes[i], garfos[i], garfos[(i + 1) % 5])
    for i in range(5)
]

# Inicia a thread que exibe os estados em tempo real
thread_visualizacao = threading.Thread(target=exibir_estados, daemon=True)
thread_visualizacao.start()

# Inicia as threads dos filósofos (começam a pensar e comer)
for f in filosofos:
    f.start()
