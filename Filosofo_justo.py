# SISTEMA JUSTO (starvation)
# O sistema se torna justo trocando o a f

import threading  # permite criar execuções paralelas (cada filósofo é uma thread)
import time       # controla os tempos de pensar/comer
import os         # usado para limpar a tela na exibição em tempo real

# Lista com os nomes dos filósofos
nomes = ["Platão", "Aristóteles", "Sócrates", "Descartes", "Kant"]

# Dicionários de estado e contagem
estado_filosofo = {nome: "Pensando 🧠" for nome in nomes}
contador_por_filosofo = {nome: 0 for nome in nomes}
garfos_usados = {nome: "" for nome in nomes}

# Lock para proteger seções críticas
lock = threading.Lock()

# Classe que representa um filósofo (uma thread)
class Filosofo(threading.Thread):
    def __init__(self, nome, garfo_esquerdo, garfo_direito, idx_esq, idx_dir):
        super().__init__()
        self.nome = nome
        self.garfo_esquerdo = garfo_esquerdo
        self.garfo_direito = garfo_direito
        self.idx_esq = idx_esq
        self.idx_dir = idx_dir

    def run(self):
        while True:
            self.atualizar_estado("Pensando 🧠", "")
            time.sleep(1)
            self.comer()

    def atualizar_estado(self, estado, garfos):
        with lock:
            estado_filosofo[self.nome] = estado
            garfos_usados[self.nome] = garfos

    def pode_comer(self):
        with lock:
            min_refeicoes = min(contador_por_filosofo.values())
            return contador_por_filosofo[self.nome] <= min_refeicoes + 1

    def comer(self):
        # Espera até que esteja equilibrado
        while not self.pode_comer():
            time.sleep(0.1)

        # Estratégia para evitar deadlock
        if nomes.index(self.nome) % 2 == 0:
            self.garfo_esquerdo.acquire()
            self.garfo_direito.acquire()
        else:
            self.garfo_direito.acquire()
            self.garfo_esquerdo.acquire()

        # Atualiza o estado para "comendo" com os números dos garfos
        self.atualizar_estado("Comendo 🍝", f"(Garfos {self.idx_esq+1} e {self.idx_dir+1})")
        time.sleep(1)

        with lock:
            contador_por_filosofo[self.nome] += 1

        self.atualizar_estado("Pensando 🧠", "")
        self.garfo_esquerdo.release()
        self.garfo_direito.release()

# Thread de exibição em tempo real
def exibir_estados():
    while True:
        time.sleep(0.5)
        with lock:
            os.system("cls" if os.name == "nt" else "clear")

            print("🧾 Estado atual dos filósofos:")
            for nome in nomes:
                print(f"- {nome:<10}: {estado_filosofo[nome]} {garfos_usados[nome]}")

            print("\n📊 Total de refeições:")
            for nome in nomes:
                print(f"- {nome:<10}: {contador_por_filosofo[nome]} vez(es)")

            print("\n(Atualizado a cada 0.5s)")

# Cria 5 garfos (semáforos)
garfos = [threading.Semaphore(1) for _ in range(5)]

# Cria os 5 filósofos com seus respectivos garfos
filosofos = [
    Filosofo(nomes[i], garfos[i], garfos[(i + 1) % 5], i, (i + 1) % 5)
    for i in range(5)
]

# Inicia a thread de visualização
thread_visualizacao = threading.Thread(target=exibir_estados, daemon=True)
thread_visualizacao.start()

# Inicia os filósofos
for f in filosofos:
    f.start()
