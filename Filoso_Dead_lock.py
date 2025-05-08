#Dead Lock

import threading#permite criar execuções paralelas (cada filósofo é uma thread)
import time #controla os tempos de pensar/comer

# Lista com o nome dos filósofos
nomes = ["Platão", "Aristóteles", "Sócrates", "Descartes", "Kant"]

# Cria uma lista com 5 objetos Lock, representando os 5 garfos
garfos = [threading.Lock() for _ in range(5)]

# Dicionário para contar quantas vezes cada filósofo comeu
contador = {nome: 0 for nome in nomes}

# Classe Filosofo que herda de Thread
class Filosofo(threading.Thread):
    def __init__(self, nome, idx, esquerda, direita, idx_esq, idx_dir):
        super().__init__()
        self.nome = nome                  # Nome do filósofo
        self.idx = idx                   # Índice do filósofo (posição na mesa)
        self.esquerda = esquerda         # Garfo à esquerda (objeto Lock)
        self.direita = direita           # Garfo à direita (objeto Lock)
        self.idx_esq = idx_esq           # Índice do garfo esquerdo
        self.idx_dir = idx_dir           # Índice do garfo direito

    def run(self):
        while True:
            print(f"{self.nome} está pensando.")  # Filósofo pensa por 1 segundo
            time.sleep(1)

            # Tenta pegar o garfo à esquerda
            print(f"{self.nome} tenta pegar o garfo 🥄 {self.idx_esq + 1} (esquerdo).")
            self.esquerda.acquire()  # Trava o garfo esquerdo
            print(f"{self.nome} pegou o garfo 🥄 {self.idx_esq + 1}.")

            time.sleep(0.1)  # Pequena pausa para simular o tempo entre pegar os garfos

            # Tenta pegar o garfo à direita
            print(f"{self.nome} tenta pegar o garfo 🥄 {self.idx_dir + 1} (direito).")
            self.direita.acquire()  # Trava o garfo direito
            print(f"{self.nome} pegou o garfo 🥄 {self.idx_dir + 1}.")

            # Come por 1 segundo
            print(f"{self.nome} está comendo 🍝.")
            time.sleep(1)

            # Incrementa o contador de refeições do filósofo
            contador[self.nome] += 1

            # Libera os dois garfos após comer
            print(f"{self.nome} terminou de comer e soltou os garfos 🥄 {self.idx_esq + 1} e 🥄 {self.idx_dir + 1}.\n")
            self.direita.release()
            self.esquerda.release()

# Thread auxiliar que mostra o resultado após 10 segundos de simulação
def exibir_resultado():
    time.sleep(10)
    print("\n📊 Resultado após 10 segundos:")
    for nome in nomes:
        print(f"- {nome}: {contador[nome]} vez(es)")

# Inicia a thread que mostra o resultado (como daemon para não bloquear o programa)
threading.Thread(target=exibir_resultado, daemon=True).start()

# Cria uma lista com 5 filósofos, cada um com os garfos ao lado
filosofos = [
    Filosofo(
        nomes[i],                  # Nome do filósofo
        i,                         # Índice (posição)
        garfos[i],                 # Garfo à esquerda
        garfos[(i + 1) % 5],       # Garfo à direita (com % para "circular")
        i,                         # Índice do garfo esquerdo
        (i + 1) % 5                # Índice do garfo direito
    )
    for i in range(5)
]

# Inicia a execução de cada filósofo (thread)
for f in filosofos:
    f.start()
